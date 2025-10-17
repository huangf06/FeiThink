# 文章格式规范 / Article Format Standards

本文档定义了 FeiThink 项目中所有文章的标准格式规范。请确保所有新文章都遵循这些标准。

---

## 一、Front Matter 规范

### 必需字段（Required）

所有文章必须包含以下字段：

```yaml
---
title: "文章标题"
date: 2025-01-01
lastmod: 2025-01-01
draft: false
categories: ["Essays"]  # 或 ["Philosophy"], ["Literature"]
tags: [tag1, tag2, tag3]  # 至少 3 个标签
summary: "文章摘要，50-100 字之间，用一句话概括文章核心内容"
weight: 999
author: "FeiThink"
showToc: true
TocOpen: false
---
```

### 字段说明

| 字段 | 说明 | 示例 |
|------|------|------|
| `title` | 文章标题（中英文都应用英文或中文一致） | `"Prologue"` 或 `"序言"` |
| `date` | 发布日期（YYYY-MM-DD 格式） | `2025-01-01` |
| `lastmod` | 最后修改日期（通常与 date 相同，有更新时改为当前日期） | `2025-01-01` |
| `draft` | 发布状态（`true` 为草稿，`false` 为已发布） | `false` |
| `categories` | 文章分类，必须从以下中选择：| `["Essays"]` |
|  | • `Essays` - 个人随笔 | |
|  | • `Philosophy` - 哲学思考 | |
|  | • `Literature` - 文学评论 | |
| `tags` | 标签列表，用于分类和搜索，至少 3 个 | `[personal-essay, philosophy, reflection]` |
| `summary` | 文章摘要（50-100 字），用于列表展示和 SEO | `"开办写字空间的思考..."` |
| `weight` | 权重（数字越小越靠前），用于排序 | `999`（默认值）或 `1`（置顶） |
| `author` | 作者名称 | `"FeiThink"` |
| `showToc` | 是否显示目录 | `true` |
| `TocOpen` | 目录默认是否展开 | `false` |

### 标签规范

标签应该：
- 使用**小写+连字符**格式（kebab-case）
- 语义清晰，易于分类和搜索
- 每篇文章至少 3 个，最多 5 个

常用标签示例：
```yaml
tags: [personal-essay, philosophy, reflection, introspection, ethics]
tags: [book-review, literature, philosophy, moral-philosophy]
tags: [political-commentary, social-analysis, ethics]
tags: [translation, literature, philosophy]
```

---

## 二、内容格式规范

### 2.1 空行和间距

**Front Matter 后的空行：**
- Front Matter 末尾的 `---` 后面应有 **1 个空行**
- 不要多于 1 个空行

```markdown
---
title: "文章标题"
...
---

第一段内容开始
```

### 2.2 标题层级

遵循 Markdown 标题层级规范：

| 层级 | 用途 | 格式 | 示例 |
|------|------|------|------|
| H1 (`#`) | **不要使用** | — | — |
| H2 (`##`) | 一级标题（章节） | `## 一、标题` | `## Why create this space?` |
| H3 (`###`) | 二级标题（小节） | `### 1. 小标题` | `### Birthday Commemoration` |
| H4 (`####`) | 三级标题（小标题） | `#### 详细标题` | — |

**规则：**
- 不要使用 H1（`#`），因为页面标题来自 front matter
- 章节使用 H2（`##`），并在上下各保留 1 个空行
- 小节使用 H3（`###`）
- 标题前后各 1 个空行
- 使用数字编号时格式统一：`## 一、标题` 或 `## 1. Title`

**示例：**
```markdown
## 为什么要建立这个空间

这是第一段内容。

### 1. 理由一

详细说明...

### 2. 理由二

详细说明...
```

### 2.3 段落和分隔

**段落间距：**
- 段落之间用 1 个空行分隔
- 段落内句子不需空行

**分隔符：**
- 在逻辑上独立的内容块之间使用 `---` 分隔
- `---` 前后各 1 个空行

```markdown
第一个逻辑块的最后一段。

---

第二个逻辑块的开始。
```

### 2.4 列表

**无序列表：**
```markdown
- 第一项
- 第二项
- 第三项
```

**有序列表：**
```markdown
1. 第一项
2. 第二项
3. 第三项
```

### 2.5 强调和引用

**加粗：**
- 使用 `**text**` 表示重点
- 仅用于特别重要的词或短语

**斜体：**
- 使用 `*text*` 表示斜体（书名、专有名词等）
- 示例：*The Brothers Karamazov*

**引用：**
- 使用 `> 引用文本` 表示块引用
- 长引用需标注出处

```markdown
> 这是一段引用文本。
>
> 可以有多个段落。

> 引用文本
>
> ——作者名字
```

### 2.6 代码

**行内代码：**
```markdown
使用 `code` 表示行内代码。
```

**代码块：**
使用三个反引号（```）包围，指定语言：
````markdown
```python
def hello():
    print("Hello, World!")
```
````

---

## 三、双语文章规范

对于中英文双语文章：

### 3.1 文件命名

```
content/posts/
├── 167521111-rereading-the-brothers-karamazov.zh.md  # 中文版本
└── 167521111-rereading-the-brothers-karamazov.en.md  # 英文版本
```

**规则：**
- 使用 Substack ID 作为前缀（如 `167521111-`）
- 文件名用英文（kebab-case）
- 文件尾部用 `.zh.md` 或 `.en.md` 区分语言

### 3.2 Front Matter 对齐

两个语言版本的 Front Matter 应该完全相同，**除了 `summary` 字段**：

```yaml
# 中文版本
summary: "中文摘要..."

# 英文版本
summary: "English summary..."
```

其他所有字段（title, date, tags, categories 等）保持完全一致。

### 3.3 标题翻译

确保对应的标题翻译准确：

```markdown
# 中文版本
## 一、为什么要建立这个空间

# 英文版本
## Why create this space?
```

---

## 四、可选字段

以下字段可选，根据需要添加：

```yaml
# 文章描述（SEO）
description: "详细的 meta description，用于搜索引擎"

# 隐藏元数据
hidemeta: false  # 是否隐藏发布日期、作者等

# 评论
comments: true  # 是否允许评论

# 分享
disableShare: false  # 是否禁用分享按钮

# 搜索
searchHidden: false  # 是否在搜索中隐藏

# 封面
cover:
    image: "/path/to/image.jpg"
    alt: "图片说明"
    caption: "图片标题"
    relative: false
```

---

## 五、创建新文章

### 使用 Hugo 命令创建：

```bash
# 创建新文章（会自动使用 archetypes/default.md 模板）
hugo new posts/article-name.md
```

### 手动创建：

1. 在 `content/posts/` 目录创建新文件
2. 复制以下模板
3. 填入相关信息

```markdown
---
title: "Your Article Title"
date: 2025-01-15
lastmod: 2025-01-15
draft: false
categories: ["Essays"]
tags: [tag1, tag2, tag3]
summary: "Brief summary of your article (50-100 words)"
weight: 999
author: "FeiThink"
showToc: true
TocOpen: false
---

Your article content starts here.

## Section 1

Content...

### Subsection 1.1

Content...
```

---

## 六、检查清单

发布文章前，请确认以下事项：

- [ ] Front Matter 所有必需字段都已填写
- [ ] `draft: false` （确保不是草稿）
- [ ] 至少包含 3 个标签
- [ ] 标签使用 kebab-case 格式（小写+连字符）
- [ ] 包含 50-100 字的摘要
- [ ] 不使用 H1 标题
- [ ] 标题前后各 1 个空行
- [ ] 段落间隔使用 1 个空行
- [ ] 没有多余的空行
- [ ] 代码块有正确的语言标识
- [ ] 引用有出处标注（如需要）
- [ ] 双语文章的两个版本 Front Matter 一致
- [ ] 文件名使用 kebab-case（小写+连字符）

---

## 七、快速参考

### 标准 Front Matter 模板

```yaml
---
title: "Article Title"
date: 2025-01-15
lastmod: 2025-01-15
draft: false
categories: ["Essays"]  # Essays / Philosophy / Literature
tags: [tag1, tag2, tag3]
summary: "Brief summary here"
weight: 999
author: "FeiThink"
showToc: true
TocOpen: false
---
```

### 标准内容结构

```markdown
简洁的开篇段落。

## 一、第一部分

### 1. 小节

内容...

### 2. 小节

内容...

---

## 二、第二部分

更多内容...
```

---

## 八、示例文章

参考以下文章了解标准格式：

- ✅ **[Prologue](content/posts/137279583-prologue.zh.md)** - 完整的规范格式
- ✅ **[Rereading The Brothers Karamazov](content/posts/167521111-rereading-the-brothers-karamazov.zh.md)** - 内容组织示例

---

**最后更新**：2025-01-17
**维护者**：FeiThink
**版本**：1.0
