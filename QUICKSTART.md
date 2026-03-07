# Consilium 技能快速上手指南

## 安装

```bash
# 方法 1: 从 OpenClaw 技能市场安装
openclaw skill install consilium

# 方法 2: 手动安装
# 下载 consilium.skill 文件，然后:
openclaw skill install ./consilium.skill
```

## 配置

### 设置 API Key

选择以下任一方式：

**环境变量（推荐）:**
```bash
export DEEPSEEK_API_KEY="sk-xxxxxxxxxxxxxxxx"
# 或
export OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxx"
# 或
export ANTHROPIC_API_KEY="sk-xxxxxxxxxxxxxxxx"
```

**OpenClaw 配置:**
```bash
openclaw config set env.DEEPSEEK_API_KEY "sk-xxxxxxxxxxxxxxxx"
```

## 使用方式

### 方式 1: CLI 命令行

```bash
# 基础用法
python consilium_deliberate.py "你的需求"

# 示例：安全删除文件
python consilium_deliberate.py "删除所有临时文件" --safety-level high

# JSON 输出（供程序处理）
python consilium_deliberate.py "生成一个爬虫" --format json

# 保存报告
python consilium_deliberate.py "复杂任务" -o report.md
```

### 方式 2: Python API

```python
from consilium_api import ConsiliumEngine

# 初始化
engine = ConsiliumEngine()

# 审议需求
result = engine.deliberate("自动回复所有邮件")

# 检查结果
if engine.is_safe_to_proceed(result):
    actions = engine.get_approved_actions(result)
    execute(actions)
else:
    print("操作被拒绝:", result['decision_manifest']['safety_notes'])
```

### 方式 3: 作为 OpenClaw 决策中间件

```python
# 在 skill 中使用
from consilium_api import ConsiliumEngine

engine = ConsiliumEngine(safety_level='high')

def sensitive_operation(params):
    # 审议前
    result = engine.deliberate(f"执行操作: {params}")
    
    if result['recommendation'] == 'reject':
        raise SafetyError("操作被 Consilium 拒绝")
    
    # 执行
    return execute(params)
```

## 典型场景

### 场景 1: 文件操作安全

```python
# 删除文件前审议
result = engine.deliberate(
    f"删除匹配 {pattern} 的文件",
    {'safety_level': 'high'}
)

# 输出示例:
# ✅ 批准: 删除7天前的 .tmp 文件
# ⚠️ 需要确认: 递归删除子目录
# ❌ 拒绝: 删除隐藏文件
```

### 场景 2: 代码生成审查

```python
# 生成 skill 后审查
generated_code = generate_skill(request)
review = engine.review_skill(generated_code, description)

# 检查安全问题
if review['guardian_review']['safety_level'] == 'critical':
    # 重新生成或人工审查
    regenerate()
```

### 场景 3: 复杂需求澄清

```python
# 分析模糊需求
analysis = engine.analyze_requirements(
    "帮我建一个个人助理",
    {'user_background': 'non-technical'}
)

# 获取澄清后的需求
clarified = analysis['deliverables']['prd']
```

## 输出解读

### Decision Manifest（决策清单）

```json
{
  "approved_actions": ["可立即执行的操作"],
  "needs_confirmation": ["需用户确认的操作"],
  "rejected_actions": ["拒绝执行的操作"],
  "conditional_actions": ["带条件的操作"],
  "safety_notes": ["安全提醒"]
}
```

### Recommendation（建议）

| 值 | 含义 | 操作建议 |
|----|------|----------|
| `proceed` | 安全，可执行 | 直接执行 approved_actions |
| `proceed_with_caution` | 需谨慎 | 显示 concerns 给用户确认 |
| `needs_clarification` | 需澄清 | 询问用户更多信息 |
| `reject` | 拒绝 | 不执行，显示 safety_notes |

## 安全级别

| 级别 | 适用场景 | 审议严格度 |
|------|----------|------------|
| `low` | 读取操作、查询 | 快速审议 |
| `medium` | 一般操作（默认） | 标准审议 |
| `high` | 文件修改、API调用 | 严格审议 |
| `critical` | 删除、敏感操作 | 最严格审议 |

设置方式：
```python
engine = ConsiliumEngine(config={'safety_level': 'high'})
# 或
result = engine.deliberate(req, {'safety_level': 'high'})
```

## 故障排除

### API Key 错误
```
ValueError: DeepSeek API key is required
```
**解决**: 设置 DEEPSEEK_API_KEY 环境变量

### API 限流
```
HTTP Error 429: Too Many Requests
```
**解决**: 添加延迟或切换 API 后端

### 解析错误
```
Failed to parse JSON from response
```
**解决**: 重试或使用更高 temperature

## 最佳实践

1. **敏感操作必用**: 删除、修改、发送等操作前调用
2. **合适的安全级别**: 不要盲目用 critical，会拖慢速度
3. **记录审计日志**: 保留审议结果用于事后分析
4. **结合其他安全措施**: Consilium 是一层防护，不是唯一防护

## 获取帮助

- GitHub Issues: https://github.com/deloog/consilium/issues
- 文档: https://github.com/deloog/consilium/tree/main/docs
- OpenClaw 社区: https://discord.gg/clawd
