---
name: {{SKILL_NAME}}
description: |
  {{SKILL_PURPOSE}}
  Use when the user invokes /{{SKILL_NAME}} or asks about {{SKILL_NAME}}.
allowed-tools:
  - Bash
  - Read
  - Write
---

# /{{SKILL_NAME}}

{{SKILL_PURPOSE}}

---

## Iron Law

Source repo scope: this skill only reads from `~/.claude/skills/{{SKILL_NAME}}/bin/`.  
Never modifies `~/.claude/settings.json` at runtime.  
Project data lives in `{PWD}/.{{SKILL_NAME}}/`, created lazily by hooks on first run.

---

## Step 1 — Guard: runtime installed?

```bash
_RUNTIME="$HOME/.claude/skills/{{SKILL_NAME}}"
if [[ ! -d "$_RUNTIME" ]]; then
  echo "[{{SKILL_NAME}}] Not installed. Run:"
  echo "  git clone https://github.com/{{GITHUB_ORG}}/{{SKILL_NAME}}.git ~/.claude/skills/{{SKILL_NAME}}"
  echo "  ~/.claude/skills/{{SKILL_NAME}}/setup install"
  exit 1
fi
```

**[AI 指令]** If runtime not found, output the install instructions above and stop.

---

## Step 2 — Parse arguments

```bash
# Parse first argument from user message
_ARG=""   # AI fills from user message, e.g. "all", "reset", etc.
```

---

## Step 3 — Main logic

```bash
python3 "$HOME/.claude/skills/{{SKILL_NAME}}/bin/{{SKILL_NAME}}-main.py" \
  --cwd "$PWD" \
  ${_ARG:+--arg "$_ARG"}
```

**[AI 指令]** Run the command above via Bash tool. Display the output to the user.

---

## Step 4 — Error handling

If the script exits non-zero:
- Check if `{PWD}/.{{SKILL_NAME}}/` exists. If not: this is the first run — show setup hint.
- Otherwise: display the error output and suggest running `/{{SKILL_NAME}}-upgrade` to update.
