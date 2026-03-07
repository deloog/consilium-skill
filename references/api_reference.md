# Consilium API Reference

## Python API

### ConsiliumEngine Class

Main entry point for programmatic use.

```python
from consilium_api import ConsiliumEngine

engine = ConsiliumEngine()
```

#### Constructor

```python
ConsiliumEngine(config: Optional[Dict] = None)
```

**Parameters:**
- `config`: Optional configuration dictionary
  - `safety_level`: 'low' | 'medium' | 'high' | 'critical'
  - `model`: LLM model name to use
  - `backend`: 'deepseek' | 'openai' | 'anthropic'

**Environment Variables:**
- `DEEPSEEK_API_KEY` - DeepSeek API key
- `OPENAI_API_KEY` - OpenAI API key
- `ANTHROPIC_API_KEY` - Anthropic API key

#### Methods

##### deliberate()

```python
deliberate(requirement: str, context: Optional[Dict] = None) -> Dict[str, Any]
```

Run full multi-party deliberation on a requirement.

**Parameters:**
- `requirement`: The requirement or task description
- `context`: Additional context (user preferences, safety level, etc.)

**Returns:**
Dictionary with keys:
- `deliberation_summary`: Executive summary
- `roles_analysis`: Analysis from each role (PM, Tech Lead, etc.)
- `guardian_review`: Safety review results
- `decision_manifest`: Final decision with approved/rejected actions
- `recommendation`: 'proceed' | 'proceed_with_caution' | 'needs_clarification' | 'reject'

##### quick_check()

```python
quick_check(action: str, action_type: str = 'general') -> Dict[str, Any]
```

Quick safety check for a single action.

**Parameters:**
- `action`: Description of the action
- `action_type`: 'file' | 'network' | 'data' | 'general'

##### review_skill()

```python
review_skill(skill_code: str, skill_description: str) -> Dict[str, Any]
```

Review generated skill code for quality and safety.

##### analyze_requirements()

```python
analyze_requirements(user_request: str, context: Optional[Dict] = None) -> Dict[str, Any]
```

Analyze and clarify complex user requirements.

##### Helper Methods

```python
is_safe_to_proceed(result: Dict[str, Any]) -> bool
get_approved_actions(result: Dict[str, Any]) -> List[str]
get_risk_level(result: Dict[str, Any]) -> str
```

### Convenience Functions

```python
from consilium_api import deliberate, quick_safety_check, review_before_execute

# One-shot deliberation
result = deliberate("Automatically reply to emails")

# Quick safety check
is_safe = quick_safety_check("Delete all temp files")

# Review before execute
result = review_before_execute(
    "Delete files matching: *.tmp",
    callback=lambda: perform_deletion()
)
```

## CLI Usage

```bash
# Basic deliberation
python consilium_deliberate.py "Your requirement here"

# With safety level
python consilium_deliberate.py "Delete all files" --safety-level high

# JSON output
python consilium_deliberate.py "Generate skill" --format json

# Save to file
python consilium_deliberate.py "Complex task" -o report.md
```

## Response Format

### Full Response Structure

```json
{
  "deliberation_summary": "Executive summary of the deliberation",
  "roles_analysis": {
    "pm": {
      "understanding": "PM's understanding of requirements",
      "clarifications": ["Point 1", "Point 2"],
      "concerns": ["Concern 1"]
    },
    "tech_lead": {
      "feasibility": "Feasibility assessment",
      "approach": "Recommended technical approach",
      "risks": ["Risk 1", "Risk 2"]
    },
    "cost_expert": {
      "estimate": "Cost estimate",
      "optimizations": ["Optimization 1"]
    },
    "user_rep": {
      "experience_concerns": ["UX concern 1"],
      "suggestions": ["Suggestion 1"]
    }
  },
  "deliverables": {
    "prd": "PRD summary",
    "technical_proposal": "Technical proposal summary",
    "cost_analysis": "Cost analysis summary",
    "risk_assessment": "Risk assessment summary",
    "execution_plan": ["Step 1", "Step 2"]
  },
  "guardian_review": {
    "privacy_risk": "Privacy risk assessment",
    "irreversible_ops": ["Irreversible operation 1"],
    "user_understanding": "Assessment of user understanding",
    "security_concerns": ["Security concern 1"],
    "safety_level": "low|medium|high|critical"
  },
  "decision_manifest": {
    "approved_actions": ["Action to proceed with"],
    "needs_confirmation": ["Action needing user confirmation"],
    "rejected_actions": ["Action to reject"],
    "conditional_actions": ["Action with conditions"],
    "safety_notes": ["Safety reminder 1"]
  },
  "recommendation": "proceed|proceed_with_caution|needs_clarification|reject",
  "_metadata": {
    "timestamp": "2024-01-01T00:00:00",
    "backend": "deepseek",
    "model": "deepseek-chat",
    "requirement": "Original requirement"
  }
}
```

### Decision Manifest

The `decision_manifest` is the key output for automated decision making:

| Field | Description |
|-------|-------------|
| `approved_actions` | Safe to execute without confirmation |
| `needs_confirmation` | Requires explicit user confirmation |
| `rejected_actions` | Should not be executed |
| `conditional_actions` | Can execute with specified conditions |
| `safety_notes` | Important safety reminders |

## Integration Patterns

### Pattern 1: Middleware

```python
def sensitive_operation(params):
    # Pre-execution deliberation
    engine = ConsiliumEngine()
    result = engine.deliberate(f"Execute: {params}")
    
    if not engine.is_safe_to_proceed(result):
        raise SafetyException(result['decision_manifest']['safety_notes'])
    
    # Execute approved actions only
    for action in engine.get_approved_actions(result):
        execute(action)
```

### Pattern 2: Decorator

```python
def consilium_review(action_description):
    def decorator(func):
        def wrapper(*args, **kwargs):
            engine = ConsiliumEngine()
            desc = action_description.format(*args, **kwargs)
            result = engine.deliberate(desc)
            
            if result['recommendation'] == 'reject':
                raise PermissionError("Action rejected by Consilium")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

@consilium_review("Delete file: {}")
def delete_file(filepath):
    os.remove(filepath)
```

### Pattern 3: User Confirmation Flow

```python
def execute_with_confirmation(requirement):
    engine = ConsiliumEngine()
    result = engine.deliberate(requirement)
    
    if result['recommendation'] == 'proceed_with_caution':
        concerns = result['decision_manifest']['needs_confirmation']
        if not ask_user_confirmation(concerns):
            return {'status': 'cancelled'}
    
    # Proceed with approved actions
    execute_actions(result['decision_manifest']['approved_actions'])
```

## Error Handling

```python
try:
    result = engine.deliberate(requirement)
except ValueError as e:
    # API key not configured
    print(f"Configuration error: {e}")
except Exception as e:
    # LLM API failure
    print(f"Deliberation failed: {e}")
    # Fallback to simple heuristic
    proceed = simple_safety_check(requirement)
```
