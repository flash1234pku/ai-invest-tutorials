# 投资策略向 Grok Bot / Claude Code 中文教程站

纯静态、零依赖、无追踪脚本。

## 结构
- `issues/YYYY-MM-DD.json` 每期一个数据文件
- `pages/*.md` 独立页面（如 `anti-scam.md` 防骗提醒）
- `build.py` 构建脚本 → `public/`
- `public/` 生成的 HTML（勿手改）

## 新增一期
1. 复制 `issues/2026-10-14.json` 为 `issues/新日期.json`，改 `date`、`title`、`range`、`items`。
2. 每条字段：`title`、`points`(列表)、`url`、`author`、`time`、可选 `stats`、`flag`（醒目“仅供参考”警示）、`note`（备注）。
3. 运行 `python3 build.py`，首页自动按日期倒序列出。
4. 预览：`cd public && python3 -m http.server 8000`。
