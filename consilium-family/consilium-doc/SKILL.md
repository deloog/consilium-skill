---
name: consilium-doc
tags: [documentation, review, writing, quality]
description: |
  AI-powered documentation reviewer for OpenClaw. Reviews your docs for clarity, 
  completeness, and structure before you publish. Catches the "you know what I mean" 
  moments that confuse readers.
---

# Consilium Doc | 文档审查官

**Documentation Quality Reviewer for OpenClaw**

你写的文档，别人真的能看懂吗？Consilium Doc 帮你消除"你懂的"假设。

## Why You Need This

- 📝 写了 3 小时文档，用户还是看不懂
- 🔍 关键步骤漏了，读者卡在第 4 步
- 🎨 结构混乱，找信息像破案

## What It Reviews

| Aspect | Checks | Output |
|--------|--------|--------|
| **Clarity** | 术语解释、逻辑跳跃、歧义表达 | 具体修改建议 |
| **Completeness** | 前置条件、示例缺失、边界情况 | 补充清单 |
| **Structure** | 章节组织、导航性、信息层级 | 重排建议 |
| **Accessibility** | 新手友好度、背景知识要求 | 难度评级 |

## How It Works

```
Your doc → [PM 视角] 目标读者是谁？他们已知什么？
         → [Tech Writer] 步骤是否完整？术语是否一致？
         → [User Rep] 我能按这个做出来吗？
         → [Report] 问题清单 + 修改建议
```

## Quick Start

```bash
# 安装
openclaw skill install consilium-doc
```

## Usage

在对话中请求文档审查，或在上传文档后自动触发。

### 触发方式
- **主动请求**：说"审查这份文档"、"看看写得怎么样"
- **自动触发**：上传/创建文档后，OpenClaw 自动询问是否需要审查

### 示例对话

```
You: 帮我审查这份 README
OpenClaw: [Doc Reviewer] 📋 文档审查报告
          
          [PM] 目标读者明确 → 开发者，有一定技术基础
          [Tech Writer] 发现 3 个问题：
          
          ⚠️ Step 2: 缺少 macOS 安装说明
             建议：添加 "brew install xxx" 命令
          
          ⚠️ Step 3: "配置环境变量"太简略
             建议：给出具体命令，如 export API_KEY="xxx"
          
          ⚠️ 缺少 Troubleshooting 章节
             建议：添加常见问题（端口占用、权限错误等）
          
          总体评分：72/100 (B级)
          需要我生成修改后的版本吗？
```

## Review Dimensions

### 1. Clarity Check
- ⚠️ 未解释的术语（"使用 foobar 初始化" → foobar 是什么？）
- ⚠️ 逻辑跳跃（"然后配置好就行了" → 具体怎么配？）
- ⚠️ 歧义表述（"适当调整" → 什么是"适当"？）

### 2. Completeness Check
- ✅ 前置条件清单
- ✅ 系统要求（版本、依赖）
- ✅ 完整示例（可复制的代码）
- ✅ 边界情况（常见错误及解决）

### 3. Structure Check
- 📌 标题层级是否合理？
- 📌 信息顺序是否符合认知？
- 📌 目录导航是否清晰？

### 4. Audience Match
- 🎯 目标读者是谁？
- 🎯 需要的先备知识？
- 🎯 与实际阅读者匹配度？

## Example Output

以下是 AI 生成的审查报告示例格式：

```json
{
  "score": 72,
  "grade": "B",
  "issues": [
    {
      "type": "missing_prerequisite",
      "location": "Step 1",
      "issue": "假设用户已安装 Node.js",
      "suggestion": "添加: '确保已安装 Node.js 16+ (node --version)'"
    },
    {
      "type": "vague_instruction",
      "location": "Step 3",
      "issue": "'适当修改配置'过于模糊",
      "suggestion": "给出具体示例: '将 PORT 改为你想要的端口号，如 3000'"
    }
  ],
  "suggestions": [
    "添加 Quick Start 章节",
    "增加 Troubleshooting 部分",
    "提供完整可运行的示例"
  ]
}
```

> 💡 **注意**：实际输出由 AI 根据文档内容实时生成，不一定是严格的 JSON 格式。

## Doc Types

支持审查的文档类型：
- 📖 README / 项目说明
- 📘 API 文档
- 📙 教程 / Guide
- 📗 安装配置文档
- 📕 发布说明 / Changelog
- 📔 设计文档 / RFC

## Configuration

```bash
# 审查严格度
export CONSILIUM_DOC_STRICTNESS=strict    # 挑剔模式
export CONSILIUM_DOC_STRICTNESS=balanced  # 平衡（默认）
export CONSILIUM_DOC_STRICTNESS=gentle    # 温和建议

# 目标读者
export CONSILIUM_DOC_AUDIENCE=beginner    # 新手友好
export CONSILIUM_DOC_AUDIENCE=intermediate
export CONSILIUM_DOC_AUDIENCE=expert      # 可以跳过基础
```

## License

MIT License - See [LICENSE](LICENSE)
