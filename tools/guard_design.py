#!/usr/bin/env python3
"""样式护栏 —— 防止改内容时顺手改掉颜色、字体、间距。

只关心"视觉契约"这一层，不关心文案。三类东西被盯住：

  1. 样式层文件      assets/site.css / catalog.css / fonts.css、字体二进制
  2. 设计令牌        site.css 里 :root 的每一个 --变量 及其值
  3. 页面内联样式    8 个页面 <style> 块里的内容（哈希比对，正文改动不触发）

用法：
    python tools/guard_design.py check     # 对比基线，有漂移 -> 退出码 1
    python tools/guard_design.py init      # 首次建立基线
    python tools/guard_design.py accept    # 确认改动是有意的，刷新基线

基线文件：_design/baseline.json（随仓库提交，换机器也能用）
"""
import glob
import hashlib
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASELINE = os.path.join(ROOT, '_design', 'baseline.json')

STYLE_FILES = [
    'assets/site.css',
    'assets/catalog.css',
    'assets/fonts.css',
]
BEHAVIOUR_FILES = [
    'assets/site.js',
    'assets/catalog.js',
]
FONT_GLOB = 'assets/fonts/*.woff2'

TOKEN_SOURCE = 'assets/site.css'


def read(path):
    with open(os.path.join(ROOT, path), encoding='utf-8') as fh:
        return fh.read()


def norm(text):
    """把 CRLF/行尾空格/连续空行抹平，避免跨平台误报。"""
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    out, blank = [], 0
    for line in text.split('\n'):
        line = line.rstrip()
        if not line:
            blank += 1
            if blank > 1:
                continue
        else:
            blank = 0
        out.append(line)
    return '\n'.join(out).strip() + '\n'


def sha(text):
    return hashlib.sha256(norm(text).encode('utf-8')).hexdigest()[:16]


def sha_file(path):
    with open(os.path.join(ROOT, path), 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:16]


def pages():
    return sorted(p for p in glob.glob(os.path.join(ROOT, '*.html'))
                  if not os.path.basename(p).startswith('_'))


def root_tokens():
    """把 :root 里的每个 --变量 抓成 {名字: 值}。"""
    src = read(TOKEN_SOURCE)
    tokens = {}
    for block in re.findall(r':root\s*\{(.*?)\}', src, re.S):
        block = re.sub(r'/\*.*?\*/', '', block, flags=re.S)
        for name, value in re.findall(r'(--[\w-]+)\s*:\s*([^;]+);', block):
            tokens[name] = ' '.join(value.split())
    return tokens


def inline_styles():
    """每个页面的 <style> 块合并后取哈希；正文改动不影响这一项。"""
    result = {}
    for path in pages():
        name = os.path.basename(path)
        blocks = re.findall(r'<style[^>]*>(.*?)</style>', read(name), re.S)
        result[name] = sha('\n'.join(blocks)) if blocks else ''
    return result


def external_refs():
    """样式/脚本不许从站外加载 —— 字体必须自托管。"""
    hits = []
    for path in pages():
        name = os.path.basename(path)
        src = read(name)
        for m in re.finditer(r'<(?:link|script)\b[^>]*?(?:href|src)="(https?://[^"]+)"', src):
            hits.append('%s -> %s' % (name, m.group(1)[:70]))
    for css in ('assets/site.css', 'assets/catalog.css', 'assets/fonts.css'):
        src = read(css)
        for m in re.finditer(r'@import\s+(?:url\()?["\']?(https?://[^"\')]+)', src):
            hits.append('%s @import %s' % (css, m.group(1)[:60]))
        for m in re.finditer(r'url\(\s*["\']?(https?://[^"\')]+)', src):
            hits.append('%s url() %s' % (css, m.group(1)[:60]))
    return hits


def snapshot():
    fonts = {os.path.relpath(p, ROOT).replace('\\', '/'): sha_file(
        os.path.relpath(p, ROOT).replace('\\', '/')) for p in glob.glob(os.path.join(ROOT, FONT_GLOB))}
    return {
        'version': 1,
        'tokens': root_tokens(),
        'files': {p: sha(read(p)) for p in STYLE_FILES + BEHAVIOUR_FILES},
        'fonts': fonts,
        'inline': inline_styles(),
    }


def load():
    with open(BASELINE, encoding='utf-8') as fh:
        return json.load(fh)


def save(data):
    os.makedirs(os.path.dirname(BASELINE), exist_ok=True)
    with open(BASELINE, 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write('\n')


def cmd_init(quiet=False):
    data = snapshot()
    save(data)
    if not quiet:
        print('已建立基线 _design/baseline.json')
        print('  设计令牌 %d 个 · 样式/脚本 %d 个 · 字体 %d 个 · 页面内联样式 %d 页'
              % (len(data['tokens']), len(data['files']), len(data['fonts']), len(data['inline'])))
    return 0


def cmd_check():
    if not os.path.exists(BASELINE):
        print('没有基线文件，先运行: python tools/guard_design.py init')
        return 2

    base = load()
    cur = snapshot()
    problems = []

    changed = [(p, base['files'].get(p), cur['files'].get(p))
               for p in cur['files'] if base['files'].get(p) != cur['files'].get(p)]
    if changed:
        problems.append('样式/脚本文件被改动：')
        for path, old, new in changed:
            problems.append('   - %s  %s -> %s' % (path, old or '新增', new))

    old_t = base.get('tokens', {})
    new_t = cur['tokens']
    missing = sorted(set(old_t) - set(new_t))
    added = sorted(set(new_t) - set(old_t))
    edited = sorted(k for k in set(old_t) & set(new_t) if old_t[k] != new_t[k])
    if missing or added or edited:
        problems.append('设计令牌被改动：')
        for k in missing:
            problems.append('   - 删除  %s  (原值 %s)' % (k, old_t[k]))
        for k in added:
            problems.append('   + 新增  %s = %s' % (k, new_t[k]))
        for k in edited:
            problems.append('   ~ 修改  %s  %s -> %s' % (k, old_t[k], new_t[k]))

    old_f = base.get('fonts', {})
    new_f = cur['fonts']
    fdiff = [p for p in set(old_f) | set(new_f) if old_f.get(p) != new_f.get(p)]
    if fdiff:
        problems.append('字体文件被改动：')
        for p in sorted(fdiff):
            problems.append('   - %s' % p)

    old_i = base.get('inline', {})
    new_i = cur['inline']
    idiff = [p for p in set(old_i) | set(new_i) if old_i.get(p) != new_i.get(p)]
    if idiff:
        problems.append('页面内联 <style> 被改动：')
        for p in sorted(idiff):
            problems.append('   - %s' % p)

    refs = external_refs()
    if refs:
        problems.append('出现站外资源引用（本项目要求全部自托管）：')
        problems.extend('   - ' + r for r in refs)

    if not problems:
        print('样式层完好：令牌 %d 个、样式/脚本 %d 个、字体 %d 个、内联样式 %d 页，全部与基线一致。'
              % (len(new_t), len(cur['files']), len(new_f), len(new_i)))
        return 0

    print('检测到样式层漂移 —— 如果这是你有意改的，确认后运行 accept 刷新基线；')
    print('如果只是想改文案，请撤销下列改动。\n')
    for line in problems:
        print(line)
    groups = sum(1 for line in problems if not line.startswith('   '))
    print('\n共 %d 组问题。' % groups)
    return 1


def main():
    argv = sys.argv[1:]
    cmd = argv[0] if argv else 'check'
    if cmd == 'init':
        return cmd_init()
    if cmd in ('accept', 'update'):
        cmd_init(quiet=True)
        print('基线已刷新到当前状态。')
        return 0
    if cmd == 'check':
        return cmd_check()
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main())
