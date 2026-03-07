# Consilium Integration Examples

## Example 1: File Operations Safety

### Scenario
User asks: "Delete all temporary files"

### Without Consilium
```python
# DANGEROUS: Direct execution
import os
for f in os.listdir('/tmp'):
    os.remove(f)  # Might delete important files!
```

### With Consilium
```python
from scripts.consilium_api import ConsiliumEngine

engine = ConsiliumEngine()
result = engine.deliberate(
    "Delete all temporary files in /tmp directory",
    {'safety_level': 'high'}
)

if result['recommendation'] == 'proceed':
    for action in result['decision_manifest']['approved_actions']:
        execute_safely(action)
elif result['recommendation'] == 'proceed_with_caution':
    # Show concerns to user
    concerns = result['decision_manifest']['needs_confirmation']
    if ask_user(concerns):
        execute_actions(result['decision_manifest']['approved_actions'])
else:
    print("Action rejected for safety reasons")
    print(result['decision_manifest']['safety_notes'])
```

**Sample Output:**
```
审议结果:
- ✅ 批准: 删除7天前访问的/tmp文件
- ⚠️ 需要确认: 删除当前用户拥有的文件（排除其他用户）
- ❌ 拒绝: 递归删除子目录（风险过高）
- 📝 提醒: 建议先备份重要文件
```

## Example 2: Email Auto-Reply

### Scenario
User wants to set up automatic email replies.

```python
from scripts.consilium_api import ConsiliumEngine, review_before_execute

result = review_before_execute(
    "Set up automatic reply to all incoming emails",
    callback=lambda: configure_auto_reply()
)

if not result['proceed']:
    print("Auto-reply configuration rejected:")
    for concern in result['concerns']:
        print(f"  - {concern}")
```

**Deliberation Output:**
```json
{
  "recommendation": "proceed_with_caution",
  "decision_manifest": {
    "approved_actions": [
      "自动回复仅订阅类邮件（检测'unsubscribe'关键词）",
      "排除VIP发件人列表的自动回复",
      "每日生成操作摘要供用户审查"
    ],
    "needs_confirmation": [
      "确认VIP发件人列表",
      "确认回复模板内容"
    ],
    "rejected_actions": [
      "对所有邮件 blanket 自动回复（隐私风险）"
    ],
    "safety_notes": [
      "自动回复可能泄露用户在线状态",
      "建议设置回复频率限制"
    ]
  }
}
```

## Example 3: Skill Generation Review

### Scenario
AI generates a new skill and needs quality review.

```python
from scripts.consilium_api import ConsiliumEngine

skill_code = """
def organize_photos(directory):
    import os
    import shutil
    for file in os.listdir(directory):
        if file.endswith('.jpg'):
            year = extract_year(file)
            os.makedirs(f"{directory}/{year}", exist_ok=True)
            shutil.move(f"{directory}/{file}", f"{directory}/{year}/{file}")
"""

engine = ConsiliumEngine()
review = engine.review_skill(
    skill_code=skill_code,
    skill_description="Organize photos by year extracted from filename"
)

print("Quality Review:")
print(review['roles_analysis']['tech_lead']['approach'])
print("\nSafety Concerns:")
for concern in review['guardian_review']['security_concerns']:
    print(f"  ⚠️ {concern}")
```

## Example 4: Complex Requirement Analysis

### Scenario
Vague request: "Build me a personal assistant"

```python
from scripts.consilium_api import ConsiliumEngine

engine = ConsiliumEngine()
analysis = engine.analyze_requirements(
    user_request="Build me a personal assistant",
    context={
        'user_background': 'non-technical',
        'budget': 'limited',
        'platform': 'desktop'
    }
)

print("Clarified Requirements:")
print(analysis['deliverables']['prd'])
print("\nPotential Misunderstandings:")
for point in analysis['roles_analysis']['pm']['clarifications']:
    print(f"  • {point}")
```

**Output:**
```
Clarified Requirements:
用户需要一个桌面端的个人助理应用，主要功能包括：
- 日程管理和提醒
- 简单的笔记记录
- 待办事项追踪
- 由于预算有限，不需要AI对话功能

Potential Misunderstandings:
  • "Personal assistant" could mean: 
    a) Software application
    b) Human virtual assistant service
    c) AI chatbot
  • Scope unclear: calendar only vs. full productivity suite
  • Budget constraint affects feature choices
```

## Example 5: Batch Operation Safety

### Scenario
Batch processing sensitive data.

```python
from scripts.consilium_api import ConsiliumEngine

engine = ConsiliumEngine(safety_level='critical')

data_operations = [
    "Export user data to CSV",
    "Anonymize email addresses",
    "Delete old logs",
    "Send report to admin"
]

for op in data_operations:
    result = engine.quick_check(op, action_type='data')
    
    print(f"\n{op}:")
    print(f"  Risk Level: {engine.get_risk_level(result)}")
    
    if engine.is_safe_to_proceed(result):
        print(f"  ✅ Approved")
        execute(op)
    else:
        print(f"  ❌ Needs Review: {result['recommendation']}")
        for note in result.get('decision_manifest', {}).get('safety_notes', []):
            print(f"     - {note}")
```

## Example 6: CLI Usage

### Basic Usage
```bash
# Simple deliberation
python scripts/consilium_deliberate.py "Generate a file backup script"

# High safety for sensitive operations
python scripts/consilium_deliberate.py "Delete database records" --safety-level critical

# JSON output for programmatic use
python scripts/consilium_deliberate.py "Send emails to users" --format json

# Save report
python scripts/consilium_deliberate.py "Migrate database" -o migration_report.md
```

### In Shell Scripts
```bash
#!/bin/bash

# Check before dangerous operation
python scripts/consilium_deliberate.py "Remove all Docker containers" --format json > decision.json

RECOMMENDATION=$(cat decision.json | jq -r '.recommendation')

if [ "$RECOMMENDATION" = "proceed" ]; then
    docker rm -f $(docker ps -aq)
else
    echo "Operation not approved. Check decision.json for details."
    exit 1
fi
```

## Example 7: Web Application Integration

### Flask Example
```python
from flask import Flask, request, jsonify
from scripts.consilium_api import ConsiliumEngine

app = Flask(__name__)
engine = ConsiliumEngine()

@app.route('/api/deliberate', methods=['POST'])
def deliberate():
    data = request.json
    requirement = data.get('requirement')
    context = data.get('context', {})
    
    result = engine.deliberate(requirement, context)
    
    return jsonify({
        'proceed': engine.is_safe_to_proceed(result),
        'risk_level': engine.get_risk_level(result),
        'approved_actions': engine.get_approved_actions(result),
        'full_result': result
    })

@app.route('/api/safety-check', methods=['POST'])
def safety_check():
    data = request.json
    action = data.get('action')
    action_type = data.get('type', 'general')
    
    result = engine.quick_check(action, action_type)
    
    return jsonify({
        'safe': engine.is_safe_to_proceed(result),
        'risk_level': engine.get_risk_level(result),
        'notes': result.get('decision_manifest', {}).get('safety_notes', [])
    })
```

## Example 8: OpenClaw Integration

### As a Pre-Execution Hook
```python
# In OpenClaw skill execution
from scripts.consilium_api import ConsiliumEngine

class SafeSkillExecutor:
    def __init__(self):
        self.consilium = ConsiliumEngine()
    
    def execute(self, skill, params):
        # Deliberate before execution
        action_desc = f"Execute skill '{skill.name}' with params: {params}"
        result = self.consilium.deliberate(action_desc)
        
        if result['recommendation'] == 'reject':
            return {
                'success': False,
                'error': 'Action rejected by Consilium',
                'reason': result['decision_manifest']['safety_notes']
            }
        
        if result['recommendation'] == 'proceed_with_caution':
            # Log for review
            self.log_for_review(skill, params, result)
        
        # Execute approved actions
        return skill.execute(result['decision_manifest']['approved_actions'])
```

## Best Practices

1. **Always check recommendation**: Don't just check if result exists
2. **Log deliberations**: Keep audit trail of all decisions
3. **Respect safety levels**: Use appropriate level for the context
4. **Handle errors gracefully**: LLM APIs can fail
5. **Combine with other safety**: Consilium is one layer of defense
