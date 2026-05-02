# new-skill

Claude Code skill that scaffolds a new skill in seconds.  
Answer 8 questions, get a fully structured skill repo with all conventions baked in.

---

## Install

```bash
git clone https://github.com/ibalasite/new-skill.git ~/.claude/skills/new-skill
~/.claude/skills/new-skill/setup install
```

Restart Claude Code after install.

---

## Usage

```
/new-skill
```

Claude asks 8 questions, then generates a ready-to-code skill directory at `~/projects/{skill-name}/`.

---

## What the 8 questions capture

| # | Question | Why it matters |
|---|----------|---------------|
| 1 | Skill name (kebab-case) | Becomes repo name, `~/.claude/skills/{name}/`, slash command |
| 2 | One-line purpose | README headline, skill.md description |
| 3 | Scope boundary — what it does NOT do | Prevents runtime pollution of source repo |
| 4 | Data model — where state lives | Lazy-create rules for hook scripts |
| 5 | Hook types + behavior | Stop / PostToolUse / SessionStart registration |
| 6 | Sub-skills list | What gets deployed to `~/.claude/skills/` on install |
| 7 | External dependencies | Prereq checks in setup script |
| 8 | Feasibility risks | Known limitations section in CLAUDE.md |

---

## What you get

```
~/projects/{skill-name}/
├── CLAUDE.md       ← full spec, filled with your answers
├── README.md       ← user-facing docs
├── progress.md     ← standard + skill-specific implementation steps
├── skill.md        ← /{skill-name} entrypoint
├── setup           ← install / update / uninstall
├── bin/            ← ready for hook scripts and shared libs
└── skills/
    └── {skill-name}-upgrade/
        └── skill.md
```

Then follow `progress.md` — Step 1 is already DONE.

---

## Conventions every generated skill inherits

1. **Source repo = source only.** No runtime ops during development.
2. **`~/.claude/skills/{name}/` is the runtime.** Clone = install.
3. **Sub-skills via `skills/`.** Deployed on install AND update.
4. **Project data = lazy.** Hooks create `{project}/.{name}/` on first run.
5. **Uninstall preserves data.** Never deletes user project directories.

---

## Update

```
/new-skill-upgrade
```

Or: `~/.claude/skills/new-skill/setup update`

## Uninstall

```bash
~/.claude/skills/new-skill/setup uninstall
```
