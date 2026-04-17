# Hugo 站重新设计 — 会话交接文档

**日期**：2026-04-17
**状态**：Phase 0（基础设施）部分完成，Hugo 项目整体重新设计尚未开始
**下一步**：新开会话，进入完整的 Hugo 重设计 brainstorming

---

## 本次会话已经锁定的决策（不要重新讨论）

### 品牌与定位

- **统一的个人品牌**："会写康德的思考者，顺便是 AI 工程师"
- **核心身份是思想者**，工程能力是生计手段不是身份
- **目标受众**：国际化技术 + 思想圈（英文为主），次要是荷兰 Data/AI hiring manager
- **明确排除**中文舆论场（豆瓣/小红书/即刻/微博等），这是刻意选择不是遗漏

### 平台架构（Hub-and-Spoke）

- **Substack** = 主要写作阵地，想写就写，完整思想档案
- **Hugo 站 (feithink.org)** = 精选橱窗，个人品牌展示
- 职能边界清晰，Hugo 只放精选，Substack 承载完整思想流水

### 已完成的基础设施

- **域名** `feithink.org` 已购买于 Cloudflare Registrar
- `config.yml` 的 `baseURL` 已改为 `https://feithink.org/`（本次会话已编辑）
- 决定用 **Cloudflare Pages** 托管（**尚未执行**，新会话前别碰）

---

## 当前项目状态（事实描述）

- **技术栈**：Hugo 0.146.0 + PaperMod 主题（git submodule `themes/PaperMod`）
- **内容**：`content/posts/` 有 48 篇双语文章（96 个 `.md`），主题哲学/文学/随笔，来自 Substack 翻译流水线
- **About 页**：`content/about.en.md` + `about.zh.md`，当前版本偏文学化，与新定位不匹配，需重写
- **无 Projects 页**
- **首页**：用 PaperMod `profileMode`，subtitle 是"割圆为方，以趋正圆"
- **Substack 原文**：`substack_export/posts/` 122 篇
- **仓库**：`huangf06/FeiThink`，主分支 `main`

---

## 新会话的焦点：完整的 Hugo 重新设计

这是一次大的重新设计，不是微调。至少要覆盖：

1. **叙事**：About 页讲什么故事才能立住"思考者"身份？
2. **信息架构**：除了 Posts / About，要加 Projects / Essays / Notes / Reading / 书单吗？每板块职能是什么？
3. **视觉与主题**：PaperMod 够不够？候选替代：`hugo-theme-stack`、`Blowfish`、`hugo-profile`，或自写。是否需要独立 landing page？
4. **双语策略**：继续双语，还是英文优先 / 中文留精选？
5. **精选策略**：48 篇里挑多少做 featured？其他放 archive 还是删？
6. **首页布局**：访客第一眼看到什么？
7. **技术栈评估**：Hugo 要不要换？（Astro、Next.js、Zola 等）成本收益？

---

## 设计约束

- **INTJ + Kantian**：讨厌 performative 和花哨。站点审美要克制、精确、有思想厚度。
- **骄傲的是思想不是技术**：不强调工程能力，但也不完全藏起来（AI 工程师背景是求职现实）。
- **可逆性优先**：任何重大决定（主题/栈）要能在未来反悔。
- **远离中文舆论场**是策略不是疏忽。

---

## 新会话的开场建议

先读以下文件建立上下文：

- 全局 `~/.claude/CLAUDE.md`（用户身份）
- `CLAUDE.md`（项目约定）
- `config.yml`
- `content/about.en.md` / `about.zh.md`
- `ls content/posts/` 看文章清单
- 本文档

然后用 `superpowers:brainstorming` skill 进入设计流程。用"一次一个问题"的节奏，**第一个问题建议**：

> "这次重新设计要达成的最核心的一个结果是什么？是让一个荷兰 hiring manager 3 秒内决定要面试你；还是让一个国际思想圈读者读完首页就想订阅；还是别的？"

基于此再往下推进。
