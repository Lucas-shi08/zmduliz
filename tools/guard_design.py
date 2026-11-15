#!/usr/bin/env python3
"""样式提示器 —— 告诉你颜色和字体有没有被改动，不做强制约束。

这套东西是「提醒」，不是「门禁」：
  · 颜色 / 字体变了  -> 退出码 1（这两样一改，整站观感就变了）
  · 间距、字号、内联样式、其他微调 -> 只列出来，退出码 0，随便改

用法：
    python tools/guard_design.py check            # 看一眼，改颜色会返回 1
    python tools/guard_design.py check --strict   # 任何样式层变化都返回 1（备而不用）
    python tools/guard_design.py accept           # 把当前状态记为新的参考快照
    python tools/guard_design.py init             # 首次建立快照

快照文件：_design/baseline.json
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

STYLE_FILES = ['assets/site.css', 'assets/catalog.css', 'assets/fonts.css']
BEHAVIOUR_FILES = ['assets/site.js', 'assets/catalog.js']
FONT_GLOB = 'assets/fonts/*.woff2'
TOKEN_SOURCE = 'assets/site.css'


def read(path):
    with open(os.path.join(ROOT, path), encoding='utf-8') as fh:
        return fh.read()


def norm(text):
    """抹平换行与行尾空格，避免跨平台误报。"""
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
    src = read(TOKEN_SOURCE)
    tokens = {}
    for block in re.findall(r':root\s*\{(.*?)\}', src, re.S):
        block = re.sub(r'/\*.*?\*/', '', block, flags=re.S)
        for name, value in re.findall(r'(--[\w-]+)\s*:\s*([^;]+);', block):
            tokens[name] = ' '.join(value.split())
    return tokens


def inline_styles():
    result = {}
    for path in pages():
        name = os.path.basename(path)
        blocks = re.findall(r'<style[^>]*>(.*?)</style>', read(name), re.S)
        result[name] = sha('\n'.join(blocks)) if blocks else ''
    return result


def external_refs():
    hits = []
    for path in pages():
        name = os.path.basename(path)
        src = read(name)
        for m in re.finditer(r'<(?:link|script)\b[^>]*?(?:href|src)="(https?://[^"]+)"', src):
            hits.append('%s 引用了站外资源 %s' % (name, m.group(1)[:70]))
    for css in STYLE_FILES:
        src = read(css)
        for m in re.finditer(r'@import\s+(?:url\()?["\']?(https?://[^"\')]+)', src):
            hits.append('%s 里 @import 了 %s' % (css, m.group(1)[:60]))
        for m in re.finditer(r'url\(\s*["\']?(https?://[^"\')]+)', src):
            hits.append('%s 里 url() 指向 %s' % (css, m.group(1)[:60]))
    return hits


def snapshot():
    fonts = {}
    for p in glob.glob(os.path.join(ROOT, FONT_GLOB)):
        rel = os.path.relpath(p, ROOT).replace('\\', '/')
        fonts[rel] = sha_file(rel)
    return {
        'version': 2,
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


def is_colour(value):
    v = value.strip().lower()
    return v.startswith('#') or v.startswith('rgb') or v.startswith('hsl')


def is_font(name):
    return name.startswith('--f-')


def cmd_init(quiet=False):
    data = snapshot()
    save(data)
    if not quiet:
        print('参考快照已写入 _design/baseline.json（%d 个变量，%d 个页面）'
              % (len(data['tokens']), len(data['inline'])))
    return 0


def cmd_check(strict=False):
    if not os.path.exists(BASELINE):
        print('还没有参考快照，先运行: python tools/guard_design.py init')
        return 0

    base = load()
    cur = snapshot()

    red = []      # 颜色 / 字体：会改变整站观感
    grey = []     # 其它一切：只提一句

    old_t, new_t = base.get('tokens', {}), cur['tokens']
    for k in sorted(set(old_t) - set(new_t)):
        grey.append('删掉了变量 %s' % k)
    for k in sorted(set(new_t) - set(old_t)):
        bucket = red if (is_colour(new_t[k]) or is_font(k)) else grey
        bucket.append('新增变量 %s = %s' % (k, new_t[k]))
    for k in sorted(set(old_t) & set(new_t)):
        if old_t[k] == new_t[k]:
            continue
        strongly = is_colour(old_t[k]) or is_colour(new_t[k]) or is_font(k)
        bucket = red if strongly else grey
        bucket.append('%s  %s → %s' % (k, old_t[k], new_t[k]))

    for path, old in sorted(base.get('files', {}).items()):
        if cur['files'].get(path) != old:
            grey.append('%s 内容有变' % path)

    for path in sorted(set(base.get('fonts', {})) | set(cur['fonts'])):
        if base.get('fonts', {}).get(path) != cur['fonts'].get(path):
            red.append('字体文件 %s 有变动' % os.path.basename(path))

    old_i, new_i = base.get('inline', {}), cur['inline']
    for page in sorted(set(old_i) | set(new_i)):
        if old_i.get(page) != new_i.get(page):
            grey.append('%s 的内联样式有变' % page)

    for ref in external_refs():
        grey.append(ref)

    if not red and not grey:
        print('颜色和字体都没动。')
        return 0

    print('和参考快照对比：')
    if red:
        print('\n  颜色 / 字体：')
        for line in red:
            print('    · ' + line)
    if grey:
        print('\n  其它变化（一般没问题）：')
        for line in grey[:12]:
            print('    · ' + line)
        if len(grey) > 12:
            print('    · … 还有 %d 项' % (len(grey) - 12))

    if red:
        print('\n这两样会直接改变整站观感。如果是顺手改的，撤回就好；'
              '真想要这个变化，执行下面这条把它记成新的快照：')
        print('  python tools/guard_design.py accept')
        return 1

    print('\n都只是排版细节，不影响整体风格，继续就好。')
    return 1 if strict else 0


def main():
    argv = sys.argv[1:]
    cmd = argv[0] if argv else 'check'
    if cmd == 'init':
        return cmd_init()
    if cmd in ('accept', 'update'):
        cmd_init(quiet=True)
        print('参考快照已更新为当前状态。')
        return 0
    if cmd == 'check':
        return cmd_check(strict='--strict' in argv)
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main())
