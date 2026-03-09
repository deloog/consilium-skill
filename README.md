# Consilium | 智议

[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://typescriptlang.org)

> **Multi-Agent Collaborative Decision Engine for Safe AI Operations**
>
> 多智能体协同决策引擎，为 AI 操作添加安全审议层

[English](#english) | [中文](#中文)

---

<a name="english"></a>
## 🇺🇸 English

### 📦 What's in This Repo

This repository contains two distinct offerings:

#### 1. 🛠️ Consilium SDK (Original)
A standalone multi-language implementation of the Consilium decision engine.
- **Python** (`scripts/consilium_deliberate.py`) - Full implementation
- **TypeScript** - Coming soon
- **Go** - Coming soon
- **Rust** - Coming soon

Use this if you want to integrate Consilium into your own applications.

#### 2. 🔧 Consilium Family (OpenClaw Skills)
Three specialized OpenClaw skills for different scenarios:
- **`consilium-guard`** - Safety guardrail for dangerous operations
- **`consilium-doc`** - Documentation quality reviewer
- **`consilium-code`** - Balanced code reviewer

See [`consilium-family/README.md`](consilium-family/README.md) for details.

---

### 🚀 Quick Start

#### Using the Python SDK

```bash
# Clone the repository
git clone https://github.com/deloog/consilium-skill.git
cd consilium-skill

# Set up environment
export DEEPSEEK_API_KEY="your-key"

# Run deliberation
python scripts/consilium_deliberate.py "Your requirement here"
```

#### Using OpenClaw Skills

```bash
# Install skills
openclaw skill install consilium-guard
openclaw skill install consilium-doc
openclaw skill install consilium-code

# Use in conversation
You: Delete all temp files
Guard: [Intercepted] This will delete 156 files. Confirm? [Yes/No/Review]
```

---

### 📚 Documentation

| Document | Description |
|----------|-------------|
| [SKILL.md](SKILL.md) | Original skill definition (OpenClaw v1) |
| [QUICKSTART.md](QUICKSTART.md) | SDK quick start guide |
| [references/api_reference.md](references/api_reference.md) | API documentation |
| [references/architecture.md](references/architecture.md) | Architecture details |
| [references/examples.md](references/examples.md) | Usage examples |
| [consilium-family/README.md](consilium-family/README.md) | OpenClaw skills guide |

---

<a name="中文"></a>
## 🇨🇳 中文

### 📦 仓库内容

本仓库包含两个独立的项目：

#### 1. 🛠️ Consilium SDK (原版)
智议决策引擎的独立多语言实现：
- **Python** (`scripts/consilium_deliberate.py`) - 完整实现
- **TypeScript** - 即将推出
- **Go** - 即将推出
- **Rust** - 即将推出

如果你想将 Consilium 集成到自己的应用中，使用这个。

#### 2. 🔧 Consilium Family (OpenClaw 技能)
三个针对 OpenClaw 优化的专业技能：
- **`consilium-guard`** - 危险操作安全守护
- **`consilium-doc`** - 文档质量审查官
- **`consilium-code`** - 代码平衡审议员

详情见 [`consilium-family/README.md`](consilium-family/README.md)。

---

### 🚀 快速开始

#### 使用 Python SDK

```bash
# 克隆仓库
git clone https://github.com/deloog/consilium-skill.git
cd consilium-skill

# 配置环境
export DEEPSEEK_API_KEY="your-key"

# 运行审议
python scripts/consilium_deliberate.py "你的需求"
```

#### 使用 OpenClaw 技能

```bash
# 安装技能
openclaw skill install consilium-guard
openclaw skill install consilium-doc
openclaw skill install consilium-code

# 在对话中使用
你：删除所有临时文件
Guard：[拦截] 这将删除 156 个文件。确认？[是/否/查看]
```

---

### 📚 文档

| 文档 | 描述 |
|------|------|
| [SKILL.md](SKILL.md) | 原版技能定义 (OpenClaw v1) |
| [QUICKSTART.md](QUICKSTART.md) | SDK 快速入门 |
| [references/api_reference.md](references/api_reference.md) | API 文档 |
| [references/architecture.md](references/architecture.md) | 架构详情 |
| [references/examples.md](references/examples.md) | 使用示例 |
| [consilium-family/README.md](consilium-family/README.md) | OpenClaw 技能指南 |

---

## 📄 License

MIT License - See [LICENSE](LICENSE)

---

## 🙏 Credits

Created by [deloog](https://github.com/deloog) for the OpenClaw community.
