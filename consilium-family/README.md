# Consilium Family | 智议家族

[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange)](https://github.com/deloog/consilium-skill/releases)

> **Multi-Agent Collaborative Decision Engine for OpenClaw**
>
> 将单一审议引擎拆分为三个专业版本，针对不同场景优化。

[English](#english) | [中文](#中文)

---

<a name="english"></a>
## 🇺🇸 English

### Overview

Consilium Family is a collection of three specialized OpenClaw skills, each designed for a specific use case:

| Skill | Focus | One-liner | Use Cases |
|-------|-------|-----------|-----------|
| **consilium-guard** | Safety | Dangerous operation interceptor | File deletion, API calls, sensitive ops |
| **consilium-doc** | Documentation | Doc quality reviewer | README, tutorials, API docs |
| **consilium-code** | Code | Code balance reviewer | Code review, refactoring suggestions |

### Installation

```bash
# Install individual skills
openclaw skill install consilium-guard
openclaw skill install consilium-doc
openclaw skill install consilium-code

# Or install all at once
openclaw skill install consilium-guard consilium-doc consilium-code
```

### Quick Start

#### Scenario 1: Daily Development
```
You: Delete the logs folder
Guard: [Intercepted] Confirm deletion? Suggest backup first [Confirm/View/Cancel]
```

#### Scenario 2: Writing Documentation
```
You: Review this README for me
Doc: Found 3 issues:
     1. Missing macOS installation instructions
     2. "Configure environment variables" is too vague
     3. Suggest adding a troubleshooting section
```

#### Scenario 3: Code Review
```
You: Review this function
Code: ✅ Clean and clear
     ⚠️ Over: 2 cases using strategy pattern, suggest if-else
     ⚠️ Under: Missing error handling
```

### Repository Structure

```
consilium-family/
├── consilium-guard/    # Safety guardrail skill
├── consilium-doc/      # Documentation reviewer skill
├── consilium-code/     # Code reviewer skill
└── README.md           # This file
```

### Configuration

Set environment variables for LLM backend:

```bash
export DEEPSEEK_API_KEY="your-key"
# OR
export OPENAI_API_KEY="your-key"
# OR
export ANTHROPIC_API_KEY="your-key"
```

---

<a name="中文"></a>
## 🇨🇳 中文

### 概述

智议家族是三个专业的 OpenClaw 技能合集，每个针对特定场景优化：

| 技能 | 专注领域 | 一句话描述 | 适用场景 |
|------|---------|-----------|---------|
| **consilium-guard** | 安全 | 危险操作拦截器 | 文件删除、API调用、敏感操作 |
| **consilium-doc** | 文档 | 文档质量审查官 | README、教程、API文档 |
| **consilium-code** | 代码 | 代码平衡审议员 | 代码审查、重构建议 |

### 安装

```bash
# 安装单个技能
openclaw skill install consilium-guard
openclaw skill install consilium-doc
openclaw skill install consilium-code

# 或一键安装全部
openclaw skill install consilium-guard consilium-doc consilium-code
```

### 快速开始

#### 场景一：日常开发
```
你：删除 logs 文件夹
Guard：[拦截] 确认删除？建议先备份 [确认/查看/取消]
```

#### 场景二：撰写文档
```
你：帮我审查这份 README
Doc：发现 3 个问题：
     1. 缺少 macOS 安装说明
     2. "配置环境变量"太简略
     3. 建议添加故障排除章节
```

#### 场景三：代码审查
```
你：审查这个函数
Code：✅ 简洁清晰
     ⚠️ 过：2个case用了策略模式，建议if-else
     ⚠️ 保：缺少错误处理
```

### 目录结构

```
consilium-family/
├── consilium-guard/    # 安全守护技能
├── consilium-doc/      # 文档审查技能
├── consilium-code/     # 代码审议技能
└── README.md           # 本文件
```

### 配置

设置 LLM 后端的环境变量：

```bash
export DEEPSEEK_API_KEY="your-key"
# 或
export OPENAI_API_KEY="your-key"
# 或
export ANTHROPIC_API_KEY="your-key"
```

---

## 📦 Publishing

These skills are published to [ClawHub](https://clawhub.com):

| Skill | ClawHub Status |
|-------|----------------|
| consilium-guard | [View on ClawHub](https://clawhub.com/skills/consilium-guard) |
| consilium-doc | [View on ClawHub](https://clawhub.com/skills/consilium-doc) |
| consilium-code | [View on ClawHub](https://clawhub.com/skills/consilium-code) |

---

## 📄 License

MIT License - See [LICENSE](LICENSE)

---

## 🙏 Credits

Created by [deloog](https://github.com/deloog) for the OpenClaw community.
