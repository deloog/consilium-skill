# Consilium Doc | 文档审查官

<img src="https://img.shields.io/badge/OpenClaw-Skill-blue?style=flat-square" alt="OpenClaw Skill">
<img src="https://img.shields.io/badge/Focus-Documentation-green?style=flat-square" alt="Focus: Documentation">

你写的文档，别人真的能看懂吗？Consilium Doc 帮你消除"你懂的"假设。

## 为什么需要它

- 📝 写了 3 小时文档，用户还是看不懂
- 🔍 关键步骤漏了，读者卡在第 4 步
- 🎨 结构混乱，找信息像破案

## 审查维度

| 维度 | 检查内容 | 输出 |
|------|---------|------|
| **清晰度** | 术语解释、逻辑跳跃、歧义表达 | 具体修改建议 |
| **完整性** | 前置条件、示例缺失、边界情况 | 补充清单 |
| **结构** | 章节组织、导航性、信息层级 | 重排建议 |
| **易用性** | 新手友好度、背景知识要求 | 难度评级 |

## 工作原理

```
Your doc → [PM 视角] 目标读者是谁？他们已知什么？
         → [Tech Writer] 步骤是否完整？术语是否一致？
         → [User Rep] 我能按这个做出来吗？
         → [Report] 问题清单 + 修改建议
```

## 快速开始

```bash
# 安装
openclaw skill install consilium-doc

# 使用
review my_doc.md
# 或
review ./docs/api-reference.md --format=json
```

## 使用方式

### 命令行
```bash
# 审查单个文件
consilium-doc review README.md

# 审查整个文档目录
consilium-doc review ./docs --recursive

# 输出 JSON 供程序处理
consilium-doc review api.md --format json

# 生成修改后的版本
consilium-doc review draft.md --apply-suggestions -o final.md
```

### 在对话中使用
```
You: 帮我审查这份安装指南
OpenClaw: [Doc Reviewer] 发现 3 个问题：
          1. 第 2 步缺少 macOS 的说明
          2. "配置环境变量" 太简略，建议给出具体命令
          3. 没有故障排除章节
          
          要生成修改后的版本吗？
```

## 审查维度详解

### 1. 清晰度检查
- ⚠️ 未解释的术语（"使用 foobar 初始化" → foobar 是什么？）
- ⚠️ 逻辑跳跃（"然后配置好就行了" → 具体怎么配？）
- ⚠️ 歧义表述（"适当调整" → 什么是"适当"？）

### 2. 完整性检查
- ✅ 前置条件清单
- ✅ 系统要求（版本、依赖）
- ✅ 完整示例（可复制的代码）
- ✅ 边界情况（常见错误及解决）

### 3. 结构检查
- 📌 标题层级是否合理？
- 📌 信息顺序是否符合认知？
- 📌 目录导航是否清晰？

### 4. 读者匹配
- 🎯 目标读者是谁？
- 🎯 需要的先备知识？
- 🎯 与实际阅读者匹配度？

## 示例输出

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

## 支持的文档类型

- 📖 README / 项目说明
- 📘 API 文档
- 📙 教程 / Guide
- 📗 安装配置文档
- 📕 发布说明 / Changelog
- 📔 设计文档 / RFC

## 配置

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

## 许可证

MIT License
