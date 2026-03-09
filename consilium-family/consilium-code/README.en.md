# Consilium Code

<img src="https://img.shields.io/badge/OpenClaw-Skill-blue?style=flat-square" alt="OpenClaw Skill">
<img src="https://img.shields.io/badge/Focus-Code%20Review-purple?style=flat-square" alt="Focus: Code Review">

Code reviewer for OpenClaw that checks for over-engineering vs under-engineering. Catches premature optimization, unnecessary complexity, AND missing abstractions, hardcoded values, and "it works don't touch it" laziness.

## The Two Traps

### Trap 1: Over-Engineering ⚙️
> "I'm going to design a perfect, extensible, generic..."

- Strategy pattern for 3 cases
- Premature abstraction
- Complex code for "potential future needs"
- "Elegant" code beginners can't understand

### Trap 2: Under-Engineering 🚧
> "It works, don't touch it"

- Copy-paste instead of abstracting
- Magic numbers everywhere
- Error handling? Nope
- 500-line functions

## Review Dimensions

| Dimension | Over-Engineering Check | Under-Engineering Check |
|-----------|----------------------|------------------------|
| **Abstraction** | Too many abstraction layers? | Duplicated code not extracted? |
| **Complexity** | Unnecessary design patterns? | Lacks basic structure? |
| **Flexibility** | Reserving for hypothetical needs? | Hardcoded, not configurable? |
| **Simplicity** | "Clever" code? | Too crude/simple? |

## How It Works

```
Your code → [Architect] Is architecture sound?
          → [Pragmatist] Is it over-designed?
          → [Maintainability] Will I understand this in 6 months?
          → [Report] Balance point suggestions
```

## Quick Start

```bash
# Install
openclaw skill install consilium-code

# Review file
consilium-code review myfile.py

# Review diff
consilium-code review --diff HEAD~1

# Use in PR
consilium-code review --pr https://github.com/user/repo/pull/123
```

## Usage

### Command Line
```bash
# Review single file
consilium-code review src/utils.py

# Output JSON
consilium-code review main.ts --format json

# Check specific dimension only
consilium-code review app.py --focus=abstraction

# Compare with best practices
consilium-code review service.py --compare-with=google-python-style
```

### In Conversation
```
You: Review this function
OpenClaw: [Code Reviewer] 
          ✅ Good: Clear logic, good naming
          ⚠️ Over: 2 cases use strategy pattern, suggest if-else
          ⚠️ Under: Missing error handling, suggest try-catch
          
          Overall: Simplicity 7/10, Maintainability 8/10
```

## Review Details

### 1. Abstraction Balance

**Over-Engineering** ⚠️
```python
# ❌ Strategy pattern for 3 cases
class PaymentStrategy(ABC): ...
class AlipayStrategy(PaymentStrategy): ...
class WechatStrategy(PaymentStrategy): ...
class CardStrategy(PaymentStrategy): ...
# Suggest: Just use if/elif, refactor when you actually have 10+ methods
```

**Under-Engineering** ⚠️
```python
# ❌ Duplicated code
if user_type == 'vip':
    discount = 0.9
    send_email(user, msg_vip)
if user_type == 'svip':
    discount = 0.8
    send_email(user, msg_svip)
# Suggest: Extract function, use config table
```

**Balanced** ✅
```python
# Current 3 cases, if-else is clear enough
if payment_type == 'alipay':
    return process_alipay(amount)
elif payment_type == 'wechat':
    return process_wechat(amount)
else:
    return process_card(amount)
# Note: Consider strategy pattern if growing to 5+ methods
```

### 2. Complexity Check

**Over-Engineering** ⚠️
- Using design patterns just because
- Multi-layer decorator nesting
- Over-generic interfaces

**Under-Engineering** ⚠️
- 200+ line functions
- 5+ nested if statements
- No modularity, everything in one pile

### 3. Flexibility Check

**Over-Engineering** ⚠️
- "Might support multi-language in future" → placeholders for 10 languages
- "Might switch database" → abstract DAO layer with only MySQL implementation

**Under-Engineering** ⚠️
- Hardcoded API keys
- Magic numbers (timeout=30, why 30?)
- Hardcoded file paths

### 4. Simplicity Check

**Over-Engineering** ⚠️
```python
# ❌ One-liner, hard to understand
result = list(map(lambda x: x.value, filter(lambda y: y.active, items)))
# Suggest: Expand for readability
```

**Under-Engineering** ⚠️
```python
# ❌ Hundreds of lines, no function split
def process():
    # ... 300 lines ...
    pass
```

## Example Output

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
      "issue": "Strategy pattern for 2 cases",
      "severity": "medium",
      "suggestion": "Use if-else, refactor when actual needs grow",
      "rationale": "Current complexity doesn't match benefits"
    },
    {
      "type": "under-engineering",
      "line": 78,
      "issue": "Hardcoded API endpoint",
      "severity": "high",
      "suggestion": "Extract to config, support environment switching"
    },
    {
      "type": "good-practice",
      "line": 120,
      "issue": "Good function split",
      "note": "Single responsibility, clear naming"
    }
  ],
  "summary": "Good overall balance, avoid over-designing for hypothetical needs"
}
```

## Supported Languages

- Python
- TypeScript / JavaScript
- Go
- Rust
- Java
- C/C++

## Configuration

```bash
# Review strictness
export CONSILIUM_CODE_STRICTNESS=strict      # Picky mode
export CONSILIUM_CODE_STRICTNESS=balanced    # Balanced (default)
export CONSILIUM_CODE_STRICTNESS=permissive  # Permissive mode

# Code style
export CONSILIUM_CODE_STYLE=google
export CONSILIUM_CODE_STYLE=pep8
export CONSILIUM_CODE_STYLE=standardjs

# Focus area
export CONSILIUM_CODE_FOCUS=abstraction      # Focus on abstraction layers
export CONSILIUM_CODE_FOCUS=performance      # Focus on performance
export CONSILIUM_CODE_FOCUS=security         # Focus on security
```

## Principles

Consilium Code follows these principles:

1. **YAGNI** - You Aren't Gonna Need It
2. **KISS** - Keep It Simple, Stupid
3. **DRY** - Don't Repeat Yourself
4. **Readability First** - Code is for humans first, machines second

## License

MIT License
