# Consilium Architecture

## System Overview

Consilium is a multi-agent deliberation engine that simulates team-based decision making to ensure AI actions are safe, appropriate, and aligned with user intent.

```
┌─────────────┐
│   User      │
│  Request    │
└──────┬──────┘
       ▼
┌─────────────────────────┐
│    Consilium Engine      │
│  ┌───────────────────┐  │
│  │ Phase 0: Multi-   │  │
│  │ Party Deliberation│  │
│  │ (PM/Tech/Cost/    │  │
│  │  User Rep)        │  │
│  └───────────────────┘  │
│  ┌───────────────────┐  │
│  │ Phase 1-5:        │  │
│  │ Detailed Analysis │  │
│  │ (PRD/Tech/Cost/   │  │
│  │  Risk/Plan)       │  │
│  └───────────────────┘  │
│  ┌───────────────────┐  │
│  │ Phase 6: Guardian │  │
│  │ Review (Safety)   │  │
│  └───────────────────┘  │
└──────────┬──────────────┘
           ▼
    ┌──────────────┐
    │   Decision   │
    │   Manifest   │
│  └──────────────┘  │
           ▼
    ┌──────────────┐
│   Execution    │
    └──────────────┘
```

## Multi-Party Deliberation (Phase 0)

### Roles

| Role | Perspective | Key Questions |
|------|-------------|---------------|
| **PM** | Product requirements | Is the requirement clear? What's the real user need? |
| **Tech Lead** | Technical feasibility | Can we build this? What are the risks? |
| **Cost Expert** | Resource efficiency | What's the cost? Can we optimize? |
| **User Rep** | End-user experience | How will users be affected? Any UX issues? |

### Design Rationale

Multiple perspectives catch different types of issues:
- PM catches requirement misinterpretation
- Tech Lead catches implementation risks
- Cost Expert catches resource waste
- User Rep catches experience problems

## Guardian Review (Phase 6)

The safety layer that prevents harmful actions.

### Safety Checks

1. **Privacy Risk**: Will private data be exposed?
2. **Irreversible Operations**: Can this be undone?
3. **User Understanding**: Does the user know what will happen?
4. **Security Concerns**: Are there security vulnerabilities?

### Safety Levels

| Level | Description | Typical Actions |
|-------|-------------|-----------------|
| **low** | Minimal risk | Read operations, safe queries |
| **medium** | Some risk | File modifications, API calls |
| **high** | Significant risk | Data deletion, external comms |
| **critical** | Severe risk | System changes, irreversible ops |

## Decision Manifest

The structured output that drives execution.

```
┌─────────────────────────────────────┐
│         Decision Manifest            │
├─────────────────────────────────────┤
│ ✅ Approved Actions                  │
│    → Execute immediately             │
├─────────────────────────────────────┤
│ ⚠️ Needs Confirmation               │
│    → Ask user before proceeding      │
├─────────────────────────────────────┤
│ ❌ Rejected Actions                  │
│    → Do not execute                  │
├─────────────────────────────────────┤
│ 📋 Conditional Actions               │
│    → Execute with conditions         │
├─────────────────────────────────────┤
│ 📝 Safety Notes                      │
│    → Important reminders             │
└─────────────────────────────────────┘
```

## LLM Backend Architecture

Consilium supports multiple LLM providers:

### Supported Backends

| Backend | Model | Strengths |
|---------|-------|-----------|
| DeepSeek | deepseek-chat | Cost-effective, good reasoning |
| OpenAI | gpt-4 | High quality, reliable |
| Anthropic | claude-sonnet | Excellent at following instructions |

### Backend Selection

Priority order based on environment variables:
1. `DEEPSEEK_API_KEY` → DeepSeek
2. `OPENAI_API_KEY` → OpenAI
3. `ANTHROPIC_API_KEY` → Anthropic

## Data Flow

```
1. User Input
   ↓
2. Create Deliberation Prompt (with role instructions)
   ↓
3. Call LLM API
   ↓
4. Parse JSON Response
   ↓
5. Validate Structure
   ↓
6. Return Decision Manifest
   ↓
7. Application executes approved actions
```

## Security Considerations

### Trust Model

- Consilium itself runs in the same environment as the AI agent
- It cannot prevent all harmful actions, but significantly reduces risk
- Final responsibility remains with the user

### Limitations

1. **LLM Dependency**: Output quality depends on the LLM
2. **Context Window**: Very complex requirements may be truncated
3. **Not Foolproof**: Determined malicious prompts may bypass checks

### Best Practices

1. Use high safety level for sensitive operations
2. Always review `needs_confirmation` actions
3. Log all deliberation results for audit
4. Combine with other safety mechanisms

## Performance

### Latency

| Operation | Typical Latency |
|-----------|-----------------|
| Deliberation | 5-15 seconds |
| Quick Check | 3-8 seconds |

### Optimization

- Cache results for identical requirements
- Use `quick_check()` for simple validations
- Set appropriate safety levels (high = more thorough = slower)

## Extension Points

### Custom Roles

Define additional deliberation roles in configuration:

```json
{
  "custom_roles": [
    {
      "name": "Security Auditor",
      "focus": "Identify security vulnerabilities",
      "weight": 1.2
    }
  ]
}
```

### Custom Safety Rules

Add domain-specific safety checks:

```python
def custom_safety_check(action):
    if involves_financial_data(action):
        return requires_additional_approval(action)
    return True
```

## Future Enhancements

- [ ] Persistent deliberation history
- [ ] Learning from past decisions
- [ ] Collaborative deliberation (multiple Consilium instances)
- [ ] Domain-specific role templates
- [ ] Real-time monitoring dashboard
