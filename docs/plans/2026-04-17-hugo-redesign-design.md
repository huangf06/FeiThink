# FeiThink 站点重设计 — 设计文档

**日期**：2026-04-17
**状态**：brainstorming 完成，待写实施计划
**前置文档**：`2026-04-17-hugo-redesign-handoff.md`（含已锁品牌定位、域名、托管选择）

---

## 0. 本次设计的根锚（不能动的前提）

| 维度 | 锁定 |
|---|---|
| 品牌 | "会写康德的思考者，顺便是 AI 工程师"。核心身份是思想者，工程能力是手段不是身份。 |
| 受众（主） | 国际化思想+技术圈，英文为主。 |
| 受众（次） | 荷兰 Data/AI hiring manager。 |
| 受众（排除） | 中文舆论场（豆瓣/小红书/即刻/微博）。 |
| 平台分工 | Substack = 主写作阵地，完整思想档案；feithink.org = 精选橱窗 + 身份锚定。 |
| feithink.org 独特职能 | ① 身份主权与归属（域名自有）② 策展权（主题化而非时间流）③ 正式名片（URL 的重量，给 LinkedIn / 简历 / 邮件署名用） |
| 域名 | feithink.org（Cloudflare Registrar，已买） |
| 审美 | INTJ + Kantian。克制、精确、不 performative。参照"作者/出版物"而非"开发者博客"。 |

---

## 1. 核心目标（访客第一动作）

**品牌钉印优先**。

访客打开首页的那一刻，目标是：**在 10 秒内被一句定位 + 一组具体思想样本钉住，形成"这人是谁、在想什么"的印象**。订阅 Substack 是隐性次要 CTA，不放首屏 hero，只放 footer 和文章底部。深度阅读转化是再次级的自然结果，不设计。

**不采用的其他目标**：
- 订阅转化优先（A）— 会让首页充斥 CTA，和"克制"审美冲突。
- 深度阅读优先（C）— 过度乐观假设访客有耐心读完一篇。
- 职业信号优先（D）— 把思想者定位颠倒成工程师定位，和品牌战略反向。

---

## 2. 叙事（Narrative）

### 2.1 Hero 定位线方向

现在的 "Square the circle to approach the perfect round" 过度文学晦涩，和"思想者"定位是不等价的——文学抒情 ≠ 思想厚度。新 Hero 要英文主语句 + 一段 subtitle：

- **主语句**：一行话点出"康德读者 + AI 工程师"的交叉身份。候选方向（待写作阶段敲定）：
  - "Essays on moral philosophy, from a reader of Kant (and an AI engineer by trade)."
  - "Thinking in the gap between moral law and machine learning."
  - 方向原则：**具体 >> 诗意**。不要比喻，不要典故，不要"seeking truth"这类空话。
- **Subtitle**（2–3 句）：说清这里有什么 + 为什么值得停留。例："Longform essays on Kant, Dostoevsky, and the moral life. Curated from four years of writing at FeiThink on Substack. New pieces go there first."
- 中文版 Hero 保留"割圆为方，以趋正圆"作为诗意 layer（仅中文页用）。

### 2.2 About 页重写方向

当前 `about.en.md` 是"wanderer between precision and meaning" 文学化措辞，和新定位 tonal gap 明显。重写方向：

**结构**（从上到下）：
1. **Who**：两三句直接陈述——康德读者、陀氏注者、道德哲学学习者；AI 工程师（VU Amsterdam M.Sc.）。不用"wanderer"、"explorer"、"seeker"这类 performative 词。
2. **What I write about**：四条策展线的简短介绍（链到 Essays 下的四条线）。
3. **Professional**（极简一段，承担 hiring manager 信号）：VU M.Sc. AI + Databricks cert + 10 年 data/ML + 7 年 quant。一两行时间线，不展开。这段也在 Work 板块独立页面呈现，About 里是概述。
4. **Why write in English**：一句话说明——"Chinese by birth, but this site is for an international audience. Chinese writing happens on Substack." 这是把"排除中文舆论场"的战略选择明说出来的诚实段落。
5. **Contact**：邮箱 + GitHub + LinkedIn + Substack 链接。去掉"welcome thoughtful conversation"这类 filler。

**删除**：
- "wanderer between precision and meaning" 整段
- "Born into poverty yet blessed with intellect" 这句自陈虽诚实但过度戏剧化
- 结尾引用 "Only the descent into the hell of self-cognition..." — 文学 flex，和新定位不匹配

---

## 3. 信息架构（IA）

**四板块菜单**：

```
Home   ·   Essays   ·   Work   ·   About
```

### 3.1 `/` Home

见 §5 首页布局。

### 3.2 `/essays/`

**结构**（从上到下）：

1. **策展路线区（页顶）**：4 张 card，每张 = 路线名 + 一句导读 + 推荐阅读前 2 篇。点击进入路线专页 `/essays/lines/<line>/`。
2. **完整时间流**：25 篇精选按时间倒序。每条 = 标题 + 日期 + 阅读时长 + 一句摘录。**无缩略图、无 card 网格**——保持 retypeset 默认的"出版物 entry list"气质。
3. **筛选**：简单 tag 筛选；可选年份切片。

### 3.3 `/essays/lines/<line>/` 四条策展路线

| 路线 | 英文名（待敲定） | 主题 | 预计篇数 |
|---|---|---|---|
| 康德轴 | `kant` | 道德哲学根基、理性与自由 | 5 |
| 陀氏与文学 | `dostoevsky-and-literature` | 通过文学进入道德与人性 | 5 |
| 存在与自我 | `existence-and-self` | 存在主义、主体性、自我认知 | 5 |
| 道德与公共生活 | `moral-life` | 诚实、尊严、公共参与 | 5 |

**每条路线专页结构**：
- 一段导读（为什么这条线、入门门槛、阅读顺序建议）
- 按阅读顺序排列的精选（非时间顺序）
- 延伸阅读（指向 Substack 或外部资源）

思想史系列（`History of Thought 01-04`）散入各线作为延伸阅读，不独立成线。

### 3.4 `/work/`

**极简一页**，承担"顺便 AI 工程师"的正式证据，但视觉层级低于 Essays。

**三段结构，每段 2–3 条硬货，不超过一屏**：
1. **Academic**：M.Sc. AI thesis (VU Amsterdam, 2025) — 标题 + 1–2 句 abstract + 可能的 PDF 链接。
2. **Projects**：公开的 AI / RL / quant 项目（GitHub repos），每个一行描述。
3. **Credentials**：Databricks Certified Data Engineer Professional。其他相关认证。

**不放**：项目截图、详细 tech stack、代码样例、过长职业履历（那在 LinkedIn）。

### 3.5 `/about/`

见 §2.2。

### 3.6 未被收入精选的 23 篇

- Hugo 站不展示（不生成页面）。
- Substack 仍然是完整档案，URL 稳定。
- 如果有读者从外部链接点过来的旧 URL：
  - 如果旧 URL 是 `/posts/<id>/` 且内容在 Substack 有对应，设置 301 到 Substack。
  - 如果没有 Substack 对应，返回 404 + 友好提示链到 Essays。

---

## 4. 精选策略

- **总数 ~25 篇**：4 线 × 5 + 5 篇独立精品。
- **独立精品候选**（不成线但单独有分量）：
  - 《Ikiru》
  - 《The Scale of Time》
  - 《Dumbledore's Woolen Socks》
  - 《Let There Be Light》
  - 《Perfect Friendship and Bitter Merit》
- **具体 25 篇名单**：留到实施阶段逐线拍板（本文档不凝固，因为可能要重读几篇判断。四条线的候选池已在上次 brainstorming 列出）。
- **Featured 机制**：retypeset 原生 `pin: 0-99` frontmatter 字段，首页 3 篇置顶用 pin 值排序。

---

## 5. 首页（`/`）布局

```
─────────────────────────────────────
[Hero]
  主语句（一行大字，定位线）
  Subtitle（2–3 句）
─────────────────────────────────────
[3 篇钉印代表作]
  3 张极简 card（非网格感、单列或三列自适应）
  每张 = 标题 + 一句钩子 + "read →"
─────────────────────────────────────
[4 条策展路线]
  小尺寸入口（文字链为主，非大 card）
  每条 = 路线名 + 一句导读
─────────────────────────────────────
[身份 footer]
  一段短 bio（1–2 句，compressed About）
  Substack 订阅 CTA（文字级，非彩色按钮轰炸）
  Social（GitHub · LinkedIn · Substack · RSS · email）
─────────────────────────────────────
```

**关键约束**：
- Hero 后到 footer 之间**无最新文章列表**、无 tags cloud、无 search bar（search 在菜单或页脚图标）。
- Substack CTA 用文字链而非彩色按钮（避免 performative 订阅推销感）。
- 整页无装饰性图像、渐变、动效。

---

## 6. 双语策略

**英文主，中文存档**。

- 默认语言：英文。`/` 是英文首页。
- 中文页保留在 `.zh.md` / `/zh/` 路径，通过 URL 可访问。
- 首页和导航不突出中文入口；footer 可加一个低调的 "中文" 链接到 `/zh/`。
- **中文精选清单缩到最小**：About 中文版 + 3–5 篇重点中文文章。大部分 23 篇 `.zh.md` 可以不暴露在 Hugo 站（作为 deprecated archive，留在 Substack）。
- hreflang 配置完整（给搜索引擎正确信号）。
- `lang="en"` 是 `<html>` 默认。

**决定边界**：**不做**独立中文首页和平行的中文策展路线。中文内容继续在 Substack 写，feithink.org 是英文世界的身份锚。

---

## 7. 技术栈与主题

### 7.1 从 Hugo 迁移到 Astro

**放弃 Hugo 的结构性理由**：
1. Hugo 的世界观是"时间流博客"，本站的定位是"主题化策展站"——栈和定位有本质错配。
2. PaperMod / Blowfish / stack / hugo-profile 全是"工程师博客"美学，脱不出这层皮。
3. Go template 对定制首页（Hero + 3 pinned + 4 lines + footer 这种层次布局）不友好。
4. 48 篇对 Hugo 编译速度优势完全用不上。

**Astro 的匹配度**：
- Content collections 原生支持策展分组。
- 首页和路线入口页可以是独立 `.astro` 文件，和文章 layout 解耦。
- MDX 让长文嵌入脚注 / 引用 / 轻组件更自然。
- Cloudflare Pages 一级支持，无需 GitHub Actions（可以删掉 `.github/workflows/hugo.yml`）。
- 内容仍是 markdown + 标准 frontmatter，可逆性强。

### 7.2 主题：**astro-theme-retypeset**

- Repo: https://github.com/radishzzz/astro-theme-retypeset
- 648⭐ | MIT | Astro 6.1 | 维护极活跃（2026-04-12）
- Demo: https://retypeset.radishzz.cc/en/

**为什么是这个而非 astro-micro / nano / paper / cactus**：
- 默认气质是"作者出版物"而非"开发者博客"——这是根本气质差异，不是 CSS 可以修的。
- 原生 `pin: z.number().int().min(0).max(99)` frontmatter 字段：3 篇钉印零改造即用。
- `fontStyle: 'sans' | 'serif'` 一行切换（长哲学文走 serif）。
- 单 accent color（一点芥末黄），整站近单色。
- 暗色模式一等公民。
- i18n 架构完整（即使英文主，未来中文也能接）。
- KaTeX + MDX 支持脚注、引用、嵌入组件。

**需要的定制改造**（集中在 Astro 语境下）：
1. 重写 `src/pages/index.astro`：实现 §5 的四段首页布局（retypeset 默认主页是 post list，不满足"Hero + 3 pinned + 4 lines + footer"层次）。
2. 新增 `src/content/config.ts` 里 `work` collection。
3. 新增 `src/pages/work.astro` 实现 §3.4。
4. 新增 `src/pages/essays/lines/[line].astro` 实现四条策展路线专页。
5. 改 `src/pages/about.astro`（或 md 源）实现 §2.2。
6. 决定是否保留 `[...lang]/` 路由前缀（retypeset 默认 i18n-first，URL 会是 `/en/...`）。倾向：**去掉前缀**，英文直接走根路径，中文走 `/zh/`，简化 URL。

### 7.3 内容迁移

- 48 篇 `.en.md` / `.zh.md` → Astro content collection。
- 写一个小脚本做 frontmatter 映射（Hugo 的 `summary`, `categories`, `draft` → Astro schema）。
- 25 篇进精选，加 `pin` 字段（3 篇 pinned、line 分组通过 `tags` 或 `line` 字段）。
- 23 篇不迁或打 `archive: true` 不生成页面。

### 7.4 托管

- **Cloudflare Pages**（已在 handoff 锁定，尚未执行迁移）。
- DNS：`feithink.org` 在 Cloudflare Registrar，Pages 自动绑定，零额外配置。
- 不需要 GitHub Actions。把 `.github/workflows/hugo.yml` 删除。
- 旧的 `huangf06.github.io/GitStack/` 可以保留一段 grace period（或直接 301 重定向到 feithink.org）。

---

## 8. 工作量估计

| 阶段 | 预计工作量 |
|---|---|
| Astro 项目脚手架 + retypeset 安装配置 | 半天 |
| 内容迁移脚本（48 篇 frontmatter 重映射） | 半天 |
| 首页 index.astro 自定义布局 | 半天 |
| 路线专页 + Work 页 + About 重写 | 半天到一天 |
| Hero / About / 25 篇筛选 的写作内容 | 一到两天（写作，不是工程） |
| Cloudflare Pages 部署 + DNS + 301 跳转 | 半天 |
| **总计** | **4–5 个半天的工程 + 2 天的写作** |

---

## 9. 不在本次范围（out of scope）

- Newsletter 自建（仍用 Substack）
- 评论系统（retypeset 默认有 Giscus，但本次不启用——保持克制，评论去 Substack）
- 搜索（retypeset 默认 Pagefind 开启即用，无需定制）
- 分析（暂不加 Google Analytics 或其他 tracker，保持极简）
- 付费内容（不做）
- 社区功能（不做）

---

## 10. 下一步

- 用 `superpowers:writing-plans` skill 基于本设计文档写详细实施计划（阶段化、可验证的 task 列表）。
- 实施计划应该覆盖：Astro 项目初始化、内容迁移脚本、布局定制、写作任务（Hero 文案、About 重写、4 条路线导读、25 篇筛选）、部署。
