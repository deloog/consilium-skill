---
name: consilium
description: Multi-Agent Collaborative Decision Engine for safe AI operations. Use when Codex needs to make important decisions, evaluate complex requirements, or perform safety checks before executing sensitive operations. Triggers on tasks involving (1) sensitive operations (file deletion, data modification, external API calls), (2) complex requirement analysis needing multiple perspectives, (3) code/skill generation requiring quality control, (4) safety-critical decisions, or (5) when the user explicitly requests "deliberation", "review", or "consensus" before acting.
---

# Consilium | 智议决策引擎

**Multi-Agent Collaborative Decision Engine for Safe AI Operations**

Consilium adds "deliberative thinking" capability to AI Agents, preventing reckless decisions through multi-party review and safety checks.

## When to Use This Skill

Use Consilium when:
- The user requests involves **sensitive operations** (deleting files, sending messages, accessing private data)
- **Complex requirements** need analysis from multiple perspectives
- Generating **new skills or code** that requires quality control
- **Safety-critical decisions** that could have negative consequences
- User explicitly asks for "deliberation", "review", or "consensus" before acting

## Core Workflow

```
User Request → Multi-Party Review → Safety Check → Approved Actions
```

### Phase 0: Multi-Party Deliberation

Simulate a team discussion with distinct roles:

| Role | Responsibility |
|------|----------------|
| **PM** | Ensure requirements are accurately understood |
| **Tech Lead** | Assess technical feasibility |
| **Cost Expert** | Analyze resource consumption |
| **User Rep** | Review from end-user perspective |

### Phase 1-5: Detailed Analysis

Based on the deliberation, produce:
- **PRD** (Product Requirements Document)
- **Technical Proposal**
- **Cost Analysis**
- **Risk Assessment**
- **Implementation Plan**

### Phase 6: Guardian Review

Safety layer that checks:
- Will this leak private data?
- Is this operation irreversible?
- Does the user truly understand the consequences?

### Output: Decision Manifest

```json
{
  "approvedActions": [...],
  "needsConfirmation": [...],
  "rejectedActions": [...],
  "safetyNotes": [...]
}
```

## Quick Start

### Option 1: Use the Python Implementation (Recommended)

```bash
# Run Consilium deliberation
python scripts/consilium_deliberate.py "Your requirement here"
```

### Option 2: Direct API Integration

```python
from scripts.consilium_api import ConsiliumEngine

result = ConsiliumEngine.deliberate(
    requirement="Automatically reply to all emails",
    context={"user_preferences": prefs, "safety_level": "high"}
)

# Execute only approved actions
for action in result["approvedActions"]:
    execute_safely(action)
```

## Configuration

Set environment variables:

```bash
# Required: API key for LLM backend
export DEEPSEEK_API_KEY="your-key"
# OR
export OPENAI_API_KEY="your-key"

# Optional: Model configuration
export CONSILIUM_MODEL="deepseek-chat"
export CONSILIUM_BASE_URL="https://api.deepseek.com"
```

## Integration Patterns

### Pattern 1: Pre-Execution Safety Check

Use Consilium as a middleware before executing sensitive operations:

```python
def sensitive_operation(params):
    # Run deliberation first
    decision = run_consilium_deliberation(params)
    
    if decision["safety_level"] == "high_risk":
        return ask_user_confirmation(decision["concerns"])
    
    # Proceed with approved actions only
    execute(decision["approved_actions"])
```

### Pattern 2: Skill Generation Quality Control

When generating a new skill:

```python
# Generate skill draft
draft = generate_skill_draft(user_request)

# Review through Consilium
review = ConsiliumEngine.review_skill(draft)

# Apply improvements
final_skill = apply_feedback(draft, review["suggestions"])
```

### Pattern 3: Complex Requirement Analysis

For ambiguous or complex requests:

```python
analysis = ConsiliumEngine.analyze_requirements(
    user_request="Build me a personal assistant",
    context={"user_background": "non-technical", "budget": "limited"}
)

# Use the clarified requirements
execute_based_on(analysis["clarified_requirements"])
```

## Multi-Language Support

Consilium implementations available in:
- **Python** (`src/python/consilium.py`) - Recommended for beginners
- **TypeScript** (`src/typescript/consilium.ts`) - Recommended for OpenClaw integration
- **Go** (`src/go/consilium.go`) - Recommended for high-performance scenarios
- **Rust** (`src/rust/consilium.rs`) - Recommended for system-level applications

## Advanced: Custom Roles

Define custom deliberation roles in `references/roles.json`:

```json
{
  "roles": [
    {
      "name": "Security Auditor",
      "focus": "Identify security vulnerabilities",
      "questions": ["What data is exposed?", "Are there injection risks?"]
    },
    {
      "name": "Performance Expert",
      "focus": "Optimize for speed and resources",
      "questions": ["What's the time complexity?", "Can we cache results?"]
    }
  ]
}
```

## References

- **API Documentation**: See [references/api_reference.md](references/api_reference.md)
- **Architecture Details**: See [references/architecture.md](references/architecture.md)
- **Integration Examples**: See [references/examples.md](references/examples.md)

## Example Scenarios

### Scenario 1: File Deletion Request

**User**: "Delete all temp files"

**Without Consilium**: AI deletes files immediately → May delete important files

**With Consilium**:
```
[PM] User wants to free up disk space from temporary files
[Tech] Should exclude files accessed in last 7 days
[Guardian] ⚠️ Confirm the specific directories first
[Decision] Ask user to confirm: /tmp/, ~/.cache/, or specific paths?
```

### Scenario 2: Auto-Reply Setup

**User**: "Auto-reply to all my emails"

**Without Consilium**: Sets up blanket auto-reply → Replies to spam, leaks info

**With Consilium**:
```
[PM] Core need: Reduce email handling time
[Tech] Can filter by sender domain and content patterns
[User Rep] Worried about replying to important emails incorrectly
[Guardian] ⚠️ High risk of information leakage
[Decision] 
  ✅ Auto-reply ONLY newsletters/subscriptions
  ✅ VIP senders excluded permanently
  ✅ Daily summary for user review
  ❌ Blanket auto-reply rejected
```

## Troubleshooting

**Issue**: Consilium takes too long for simple tasks
**Solution**: Set `CONSILIUM_MODE=fast` for lightweight deliberation

**Issue**: API rate limit exceeded
**Solution**: Add retry logic with exponential backoff, or use local LLM

**Issue**: Deliberation results too conservative
**Solution**: Adjust `safety_level` to "medium" or "low" in context

## License

MIT License - See [LICENSE](LICENSE)
