# Consilium Doc

<img src="https://img.shields.io/badge/OpenClaw-Skill-blue?style=flat-square" alt="OpenClaw Skill">
<img src="https://img.shields.io/badge/Focus-Documentation-green?style=flat-square" alt="Focus: Documentation">

AI-powered documentation reviewer for OpenClaw. Reviews your docs for clarity, completeness, and structure before you publish.

## Why You Need This

- 📝 Spent 3 hours writing docs, users still don't understand
- 🔍 Missing key steps, readers stuck at step 4
- 🎨 Messy structure, finding info feels like detective work

## Review Dimensions

| Dimension | Checks | Output |
|-----------|--------|--------|
| **Clarity** | Term explanations, logic jumps, ambiguous phrasing | Specific fixes |
| **Completeness** | Prerequisites, missing examples, edge cases | Addition checklist |
| **Structure** | Section organization, navigation, info hierarchy | Reordering suggestions |
| **Accessibility** | Beginner-friendliness, background knowledge required | Difficulty rating |

## How It Works

```
Your doc → [PM Lens] Who's the target reader? What do they know?
         → [Tech Writer] Are steps complete? Terms consistent?
         → [User Rep] Can I follow this?
         → [Report] Issue list + improvement suggestions
```

## Quick Start

```bash
# Install
openclaw skill install consilium-doc

# Usage
review my_doc.md
# or
review ./docs/api-reference.md --format=json
```

## Usage

### Command Line
```bash
# Review single file
consilium-doc review README.md

# Review entire docs directory
consilium-doc review ./docs --recursive

# Output JSON for programmatic use
consilium-doc review api.md --format json

# Generate improved version
consilium-doc review draft.md --apply-suggestions -o final.md
```

### In Conversation
```
You: Review this installation guide
OpenClaw: [Doc Reviewer] Found 3 issues:
          1. Step 2 missing macOS instructions
          2. "Configure environment variables" too vague
          3. No troubleshooting section
          
          Generate improved version?
```

## Review Details

### 1. Clarity Check
- ⚠️ Undefined terms ("Initialize with foobar" → what's foobar?)
- ⚠️ Logic jumps ("Then just configure it" → how exactly?)
- ⚠️ Ambiguous phrasing ("Adjust appropriately" → what's "appropriate"?)

### 2. Completeness Check
- ✅ Prerequisites checklist
- ✅ System requirements (versions, dependencies)
- ✅ Complete examples (copy-paste ready code)
- ✅ Edge cases (common errors and solutions)

### 3. Structure Check
- 📌 Is heading hierarchy reasonable?
- 📌 Does info order match cognitive flow?
- 📌 Is table of contents clear?

### 4. Audience Match
- 🎯 Who's the target reader?
- 🎯 What prior knowledge is needed?
- 🎯 Match with actual readers?

## Example Output

```json
{
  "score": 72,
  "grade": "B",
  "issues": [
    {
      "type": "missing_prerequisite",
      "location": "Step 1",
      "issue": "Assumes Node.js is installed",
      "suggestion": "Add: 'Ensure Node.js 16+ is installed (node --version)'"
    },
    {
      "type": "vague_instruction",
      "location": "Step 3",
      "issue": "'Modify config appropriately' too vague",
      "suggestion": "Give specific example: 'Change PORT to your desired port, e.g., 3000'"
    }
  ],
  "suggestions": [
    "Add Quick Start section",
    "Add Troubleshooting section",
    "Provide complete runnable example"
  ]
}
```

## Supported Doc Types

- 📖 README / Project overview
- 📘 API documentation
- 📙 Tutorials / Guides
- 📗 Installation/configuration docs
- 📕 Changelogs / Release notes
- 📔 Design docs / RFCs

## Configuration

```bash
# Review strictness
export CONSILIUM_DOC_STRICTNESS=strict    # Picky mode
export CONSILIUM_DOC_STRICTNESS=balanced  # Balanced (default)
export CONSILIUM_DOC_STRICTNESS=gentle    # Gentle suggestions

# Target audience
export CONSILIUM_DOC_AUDIENCE=beginner    # Beginner-friendly
export CONSILIUM_DOC_AUDIENCE=intermediate
export CONSILIUM_DOC_AUDIENCE=expert      # Can skip basics
```

## License

MIT License
