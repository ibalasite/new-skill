# {{SKILL_NAME}} — Implementation Progress

## Step 1 — Project spec, README & GitHub remote
- [x] CLAUDE.md — full implementation spec
- [x] README.md — user-facing documentation
- [x] progress.md — this file
- [x] git init + initial commit
- [x] Create GitHub repo: github.com/{{GITHUB_ORG}}/{{SKILL_NAME}}
- [x] Set remote origin + push
> DONE

---

## Step 2 — Repository structure
- [x] `bin/` directory (for hook scripts and shared libraries)
- [x] `skills/{{SKILL_NAME}}-upgrade/` directory
- [ ] Update CLAUDE.md architecture section if needed after scaffolding
> DONE

---

## Step 3 — Core library (`bin/`)

> Implement shared logic first — no external dependencies, independently testable.

{{SKILL_SPECIFIC_STEP_3}}

---

## Step 4 — Hook scripts (`bin/`)

> Depend on core library. Lazily create `{project}/.{{SKILL_NAME}}/` on first run.

{{SKILL_SPECIFIC_STEP_4}}

---

## Step 5 — Hook registration manager (`bin/{{SKILL_NAME}}-settings-hook.py`)
- [ ] `add-stop` subcommand: inject Stop hook into `~/.claude/settings.json`
- [ ] `add-posttooluse` subcommand: inject PostToolUse hook
- [ ] `remove` subcommand: remove all hooks by marker string
- [ ] Dedup guard: skip if already present
- [ ] Atomic write: `tempfile + os.replace`
- [ ] Create `~/.claude/settings.json` skeleton if not exists

---

## Step 6 — `/{{SKILL_NAME}}` skill (`skill.md`)
- [ ] Skill frontmatter: name, description, allowed-tools
- [ ] Main command handler
- [ ] Handle missing data gracefully (first-run hint)

---

## Step 7 — `/{{SKILL_NAME}}-upgrade` skill (`skills/{{SKILL_NAME}}-upgrade/skill.md`)
- [ ] Skill frontmatter
- [ ] `git pull` in `~/.claude/skills/{{SKILL_NAME}}/`
- [ ] Redeploy sub-skills: copy `skills/*` → `~/.claude/skills/`
- [ ] Print upgrade summary

---

## Step 8 — `setup` script
- [ ] Prereq check: {{DEPS}}; exit 1 with clear message if missing
- [ ] `install` action:
  - Clone repo to `~/.claude/skills/{{SKILL_NAME}}/`
  - Deploy sub-skills: `skills/*` → `~/.claude/skills/`
  - Run `bin/{{SKILL_NAME}}-settings-hook.py add-stop`
  - Run `bin/{{SKILL_NAME}}-settings-hook.py add-posttooluse`
  - Init global config if not present
  - Print: "Restart Claude Code to activate hooks"
- [ ] `update` action:
  - `git pull` in `~/.claude/skills/{{SKILL_NAME}}/`
  - Redeploy sub-skills
- [ ] `uninstall` action:
  - Remove hooks via settings-hook.py remove
  - Remove deployed sub-skills from `~/.claude/skills/`
  - Remove `~/.claude/skills/{{SKILL_NAME}}/`
  - Leave all project data intact

---

## Step 9 — Verify commands (user runs after install)

This repo does not run setup or modify the local environment.
After installing, the user verifies with:

```bash
# Check hooks registered
python3 -c "import json; d=json.load(open('$HOME/.claude/settings.json')); print(json.dumps(d.get('hooks',{}), indent=2))"

# Check sub-skills deployed
ls ~/.claude/skills/ | grep {{SKILL_NAME}}

{{SKILL_SPECIFIC_VERIFY}}
```
> ← user runs these; not executed in this repo
