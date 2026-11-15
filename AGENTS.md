# 给接手这个仓库的 AI

这是 ZEMING（广东择明科技）的英文静态官网，11 个页面，手写 HTML/CSS/JS，无构建步骤、无框架、无 CDN。
用户通常只需要改内容，**不希望视觉被改动**。

## 开工前必读

1. 读 `DESIGN-SYSTEM.md` —— 设计令牌与六条硬规矩。
2. 读 `_FACTS.md` —— 唯一事实来源，不要编造数字、认证、人物、卖点。
3. 只做被要求的事。不要"顺手美化"、不要重构、不要升级依赖、不要引入 Tailwind/Bootstrap/CDN 字体。

## 允许改

- `<p>` `<h2>` `<h3>` `<li>` 里的纯文字
- `href`（站内锚点必须真有对应 `id`）
- 图片替换（WebP，最长边 ≤1200，保持原比例，放 `assets/img/opt/`）

## 不要改（除非用户明确要求改样式）

- `assets/site.css`、`assets/catalog.css`、`assets/fonts.css`
- `assets/site.js`、`assets/catalog.js`
- 任何页面的 `<style>` 块
- `class` 名、`data-*` 属性
- `assets/fonts/*.woff2`

## 改完必须做的两步

```bash
python tools/guard_design.py check    # 必须退出码 0
```

如果它报"样式层漂移"而用户并不想要样式变化 → 撤销改动。若确实是有意的样式修改，才运行 `accept` 刷新基线，并在提交信息里说明。

```bash
python serve.py                       # 需要目视时：127.0.0.1:8788
node tools/audit.js                   # 全站巡检（需无头 Chrome 在 9222）
```

## 导航不要手改

11 页导航与抽屉由 `tools/nav.py` 生成，幂等。改导航 = 改这个脚本 + 跑一次，不要逐页编辑。

## 换行

仓库用 `.gitattributes` 锁 LF。若在你的机器上 `git status` 忽然显示几十个文件被改，先跑
`git add --renormalize .` 再判断，不要提交换行噪声。
