# ZEMING Car Audio — 官网

广东择明科技（Guangdong Zeming Technology Co., Ltd.）英文官网。11 个静态页面，手写 HTML / CSS / JS，
无构建步骤、无框架、无 CDN、字体自托管。设计方向是「精密仪器」：墨黑 + 纸蓝 + 品牌蓝，细线表格，等宽小标签。

## 快速开始

```bash
git clone https://github.com/Lucas-shi08/zmduliz.git
cd zmduliz
python serve.py
```

打开 <http://127.0.0.1:8788>。

**必须用本地服务打开，不要双击 HTML 文件。** 直接 `file://` 打开时，产品筛选、深链锚点、
证书灯箱这类依赖 `fetch`/`location` 的逻辑会失效。

只需要 Python 3，没有 npm 依赖。

## 目录

```
*.html                 11 个页面（首页、目录、3 个详情、能力、OEM/ODM、品牌、公司、资讯、联系）
assets/site.css        全站设计系统：42 个令牌 + 所有组件
assets/catalog.css     只有产品目录页用：筛选、卡片、对比条
assets/fonts.css       自托管字体声明（assets/fonts/*.woff2）
assets/site.js         导航、滚动揭示、灯箱、WhatsApp 悬浮球
assets/catalog.js      筛选、排序、对比、深链
assets/img/opt/        优化后的 WebP（页面实际引用的都在这）
assets/img/pic/        原图与实拍素材
tools/nav.py           导航生成器：一次重写 11 页的导航与抽屉（幂等）
tools/guard_design.py  样式护栏：防止改内容时改掉颜色/字体/间距
tools/audit.js         全站巡检：缺图、横向溢出、JS 报错、菜单开合
_FACTS.md              唯一事实来源
DESIGN-SYSTEM.md       设计契约：令牌、硬规矩、可改与不可改
AGENTS.md              给 AI 的作业说明
交付说明.md            中文交付记录
```

## 改内容 vs 改样式

| 你想做的事 | 怎么做 |
|---|---|
| 改文案 | 直接改 HTML 里的文字，样式不受影响 |
| 换图片 | 新图存 `assets/img/opt/`，WebP、最长边 ≤1200、**保持原比例** |
| 改导航 | 改 `tools/nav.py`，然后 `python tools/nav.py`；不要手改页面里的导航 |
| 改颜色 / 字体 / 间距 | 先读 `DESIGN-SYSTEM.md`，改 `:root` 令牌，然后跑 `accept` 刷新基线 |

## 防止样式被改跑

这个仓库自带一道护栏，**随仓库一起走，换机器也生效**：

```bash
python tools/guard_design.py check    # 退出码 0 = 样式层没被动过
```

它比对 `_design/baseline.json` 里的三项：样式/脚本文件哈希、42 个设计令牌的值、
7 个页面内联 `<style>` 的内容哈希。**只改正文文字不会报警**；改了颜色、字体、间距、圆角，或者引入了外部 CDN，
会立刻列出哪一项从什么变成了什么，退出码 1。

确实想改样式时：

```bash
python tools/guard_design.py accept   # 刷新基线，相当于"我确认这个视觉变更"
```

可选：装成提交前钩子，漏跑也会拦住。

```bash
git config core.hooksPath .githooks
```

（这是每个克隆各自设的，不会自动带过去。）

## 换行

`.gitattributes` 锁 LF。如果在新机器上 `git status` 忽然冒出几十个"已修改"，那是换行差异，不是内容差异：

```bash
git add --renormalize .
git status
```

## 事实红线

`_FACTS.md` 是唯一来源。可用的真实数字只有：2012 年成立、10,000 m² 厂房、8 个品类 / 30 个平台、
CE-EMC / RoHS / REACH / MSDS 四份认证。不要编造型号、卖点、参数、交期、认证或人物姓名；
产品定位一律写 Universal Car Audio，不绑定具体车型。

## 上线前待办

- 联系表单尚未接后端收件箱，接入后删掉表单下方的提示文案
- `window.ZEMING_MAP_KEY` 为空时显示 SVG 定位图，填入腾讯地图 key 后启用实景地图
- 证书地址（南海区大沥镇盐步西瑶路 251 号）与页脚地址（顺德区乐从镇裕和路 110 号金海中心）口径待客户确认
- 老板照片与姓名职务待客户提供，替换 `contact.html` 的 `.owner` 占位
