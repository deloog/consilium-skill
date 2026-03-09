# Consilium Code | 代码审议官

<img src="https://img.shields.io/badge/OpenClaw-Skill-blue?style=flat-square" alt="OpenClaw Skill">
<img src="https://img.shields.io/badge/Focus-Code%20Review-purple?style=flat-square" alt="Focus: Code Review">

不是每个 if-else 都要变成策略模式，也不是每个函数都要 200 行。
Consilium Code 帮你找到那个平衡点。

## 两个陷阱

### 陷阱 1：过度设计 ⚙️
> "我要设计一个完美的、可扩展的、通用的..."

- 3 个 case 就上策略模式
- premature abstraction（过早抽象）
- 为了"可能的需求"写复杂代码
- 新手看不懂的"优雅"

### 陷阱 2：过于保守 🚧
> "能跑就行，别碰它"

- 该抽象的复制粘贴
- 魔法数字满天飞
- 错误处理？不存在的
- 一个函数 500 行

## 审查维度

| 维度 | 过度设计检查 | 过于保守检查 |
|------|-------------|-------------|
| **抽象** | 抽象层级过多？ | 重复代码未提取？ |
| **复杂度** | 不必要的设计模式？ | 缺乏基本结构？ |
| **灵活性** | 为假想需求预留？ | 硬编码、无法配置？ |
| **简洁度** | "聪明"的代码？ | 过于简单粗暴？ |

## 工作原理

```
Your code → [Architect] 架构是否合理？
          → [Pragmatist] 是否过度设计？
          → [Maintainability] 6个月后还能看懂吗？
          → [Report] 平衡点建议
```

## 快速开始

```bash
# 安装
openclaw skill install consilium-code

# 审查文件
consilium-code review myfile.py

# 审查 diff
consilium-code review --diff HEAD~1

# 在 PR 中使用
consilium-code review --pr https://github.com/user/repo/pull/123
```

## 使用方式

### 命令行
```bash
# 审查单个文件
consilium-code review src/utils.py

# 审查并输出 JSON
consilium-code review main.ts --format json

# 只检查特定维度
consilium-code review app.py --focus=abstraction

# 与最佳实践对比
consilium-code review service.py --compare-with=google-python-style
```

### 在对话中使用
```
You: 帮我审查这个函数
OpenClaw: [Code Reviewer] 
          ✅ 好：逻辑清晰，命名规范
          ⚠️ 过：2个case用了策略模式，建议直接用if-else
          ⚠️ 保：错误处理缺失，建议添加try-catch
          
          总体：简洁度 7/10，可维护性 8/10
```

## 审查维度详解

### 1. 抽象平衡

**过度设计** ⚠️
```python
# ❌ 3个case就上策略模式
class PaymentStrategy(ABC): ...
class AlipayStrategy(PaymentStrategy): ...
class WechatStrategy(PaymentStrategy): ...
class CardStrategy(PaymentStrategy): ...
# 建议：直接用 if/elif，等真有10个支付方式再重构
```

**过于保守** ⚠️
```python
# ❌ 重复代码
if user_type == 'vip':
    discount = 0.9
    send_email(user, msg_vip)
if user_type == 'svip':
    discount = 0.8
    send_email(user, msg_svip)
# 建议：提取函数，用配置表
```

**平衡** ✅
```python
# 当前3个case，if-else足够清晰
if payment_type == 'alipay':
    return process_alipay(amount)
elif payment_type == 'wechat':
    return process_wechat(amount)
else:
    return process_card(amount)
# 注释：如果增加到5+支付方式，考虑用策略模式
```

### 2. 复杂度检查

**过度设计** ⚠️
- 为了用设计模式而用
- 多层装饰器嵌套
- 过度泛化的接口

**过于保守** ⚠️
- 200+ 行的函数
- 嵌套 5+ 层的 if
- 无模块化，所有代码堆在一起

### 3. 灵活性检查

**过度设计** ⚠️
- "未来可能支持多语言" → 提前写 10 种语言的占位符
- "可能换数据库" → 抽象出通用 DAO 层，但只有 MySQL 实现

**过于保守** ⚠️
- 硬编码 API key
- 魔法数字（timeout=30，为什么是30？）
- 写死的文件路径

### 4. 简洁度检查

**过度设计** ⚠️
```python
# ❌ 一行流，难懂
result = list(map(lambda x: x.value, filter(lambda y: y.active, items)))
# 建议：展开写，可读性优先
```

**过于保守** ⚠️
```python
# ❌ 几百行没分函数
def process():
    # ... 300 lines ...
    pass
```

## 示例输出

```json
{
  "file": "payment.py",
  "scores": {
    "simplicity": 6,
    "maintainability": 7,
    "flexibility": 4,
    "overall": 6
  },
  "findings": [
    {
      "type": "over-engineering",
      "line": 45,
      "issue": "2个case使用策略模式",
      "severity": "medium",
      "suggestion": "改为if-else，等实际需求增长再重构",
      "rationale": "当前复杂度收益不匹配"
    },
    {
      "type": "under-engineering",
      "line": 78,
      "issue": "硬编码API endpoint",
      "severity": "high",
      "suggestion": "提取为配置项，支持环境切换"
    },
    {
      "type": "good-practice",
      "line": 120,
      "issue": "函数拆分合理",
      "note": "单一职责，命名清晰"
    }
  ],
  "summary": "整体平衡度良好，注意避免为假设需求过度设计"
}
```

## 支持的语言

- Python
- TypeScript / JavaScript
- Go
- Rust
- Java
- C/C++

## 配置

```bash
# 审查严格度
export CONSILIUM_CODE_STRICTNESS=strict      # 挑剔模式
export CONSILIUM_CODE_STRICTNESS=balanced    # 平衡（默认）
export CONSILIUM_CODE_STRICTNESS=permissive  # 宽松模式

# 代码风格
export CONSILIUM_CODE_STYLE=google
export CONSILIUM_CODE_STYLE=pep8
export CONSILIUM_CODE_STYLE=standardjs

# 焦点领域
export CONSILIUM_CODE_FOCUS=abstraction      # 专注抽象层级
export CONSILIUM_CODE_FOCUS=performance      # 专注性能
export CONSILIUM_CODE_FOCUS=security         # 专注安全
```

## 遵循原则

1. **YAGNI** - You Aren't Gonna Need It
2. **KISS** - Keep It Simple, Stupid
3. **DRY** - Don't Repeat Yourself
4. **可读性优先** - 代码是写给人看的，顺便给机器执行

## 许可证

MIT License
