# {{SKILL_NAME}}

{{SKILL_PURPOSE}}

---

## Requirements

- Claude Code CLI
- {{DEPS}}

---

## Install

```bash
git clone https://github.com/{{GITHUB_ORG}}/{{SKILL_NAME}}.git ~/.claude/skills/{{SKILL_NAME}}
~/.claude/skills/{{SKILL_NAME}}/setup install
```

Restart Claude Code after install to activate hooks.

---

## Update

```bash
/{{SKILL_NAME}}-upgrade
```

Or manually:

```bash
~/.claude/skills/{{SKILL_NAME}}/setup update
```

---

## Uninstall

```bash
~/.claude/skills/{{SKILL_NAME}}/setup uninstall
```

Runtime data is preserved. Delete manually if needed.

---

## Usage

```
/{{SKILL_NAME}}
```

---

## What gets installed

```
~/.claude/skills/{{SKILL_NAME}}/      ← runtime (cloned repo)
~/.claude/skills/{{SKILL_NAME}}-upgrade/  ← upgrade sub-skill
~/.claude/settings.json               ← hooks registered here
```

Project data (created lazily on first use):

```
{your-project}/
└── .{{SKILL_NAME}}/
    └── .gitignore    ← auto-created, ignores entire .{{SKILL_NAME}}/
```

---

## Known limitations

{{KNOWN_LIMITATIONS}}
