# Consilium Guard

<img src="https://img.shields.io/badge/OpenClaw-Skill-blue?style=flat-square" alt="OpenClaw Skill">
<img src="https://img.shields.io/badge/Focus-Safety-red?style=flat-square" alt="Focus: Safety">

Safety guardrail for OpenClaw. Automatically intercepts dangerous operations (file deletion, data modification, external API calls) and requires multi-party deliberation before execution.

## Why You Need This

> "AI Agent went rogue, sent 500 spam messages to the user" — This isn't sci-fi, it's a real incident.

OpenClaw is powerful, but has no brakes by default. Consilium Guard is your safety brake.

## What It Catches

| Operation | Risk | Guard Action |
|-----------|------|--------------|
| `rm -rf` / File deletion | Accidental data loss | ⚠️ Intercept, require confirmation |
| Sending emails/messages | Info leak, spam | ⚠️ Review content, limit frequency |
| External API calls | Key leak, cost explosion | ⚠️ Confirm necessity and cost |
| System config changes | System damage | ⚠️ Backup before execution |
| Sensitive file access | Privacy leak | ⚠️ De-identify data |

## How It Works

```
User: "Delete all temp files"
     ↓
[Guardian Intercepts]
     ↓
[PM] User wants to free disk space → but "temp" is ambiguous
[Tech] Suggest excluding files accessed in last 7 days
[Security] ⚠️ Need to confirm specific directories
     ↓
[Decision] Ask user: /tmp/ or ~/.cache/ or specific path?
```

## Quick Start

```bash
# Install
openclaw skill install consilium-guard

# Configure API Key
export DEEPSEEK_API_KEY="your-key"
# OR
export OPENAI_API_KEY="your-key"
```

## Usage

Guard automatically intercepts dangerous operations:

```
You: Delete logs folder
OpenClaw: [Guardian] About to delete logs/ containing 156 files.
          Suggest backup to logs_backup_20240309/ first?
          [Confirm] [View List] [Cancel]
```

## Configuration

```bash
# Safety level
export CONSILIUM_SAFETY_LEVEL=high    # Strict mode (recommended)
export CONSILIUM_SAFETY_LEVEL=medium  # Balanced mode
export CONSILIUM_SAFETY_LEVEL=low     # Fast mode

# Deliberation speed
export CONSILIUM_MODE=fast     # Lightweight (3-5s)
export CONSILIUM_MODE=standard # Standard (10-15s)
export CONSILIUM_MODE=deep     # Deep (30s+)
```

## Example Scenarios

### File Deletion
**User**: "Clean up disk space"
**Without Guard**: AI may delete system files
**With Guard**: 
- Identify safe-to-delete categories (cache, logs, temp)
- Exclude critical system directories
- Suggest compressed backup first

### API Call
**User**: "Analyze this website"
**Without Guard**: AI may spam API calls, cost explosion
**With Guard**:
- Estimate call count and cost
- Set call limits
- Suggest caching results

### Data Export
**User**: "Export all my emails"
**Without Guard**: May include sensitive info
**With Guard**:
- Scan for sensitive content
- Suggest de-identification or encryption
- Confirm recipient identity

## Advanced: Custom Rules

Create `~/.consilium/guard-rules.json`:

```json
{
  "blocked_patterns": ["*.key", "*.pem", ".env"],
  "require_confirmation": ["rm -rf", "DROP TABLE", "DELETE FROM"],
  "cost_limits": {
    "per_operation": 10.0,
    "per_hour": 100.0
  }
}
```

## License

MIT License
