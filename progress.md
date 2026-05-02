# new-skill — Implementation Progress

## Step 1 — Project spec, README & GitHub remote
- [x] CLAUDE.md — full spec
- [x] README.md — user-facing docs
- [x] progress.md — this file
- [x] Repo structure: bin/, skills/new-skill-upgrade/, template/
- [x] git init + initial commit
- [ ] Create GitHub repo: github.com/ibalasite/new-skill
- [ ] Set remote origin + push
> DONE

---

## Step 2 — `bin/new-skill-init.py`
- [ ] Accept all 8 answers + `--org` + `--output` as CLI args
- [ ] Guard: confirm `~/.claude/skills/new-skill/template/` exists; exit with install hint if not
- [ ] Create output directory if not exists
- [ ] Recursively copy `template/` → output dir (preserve structure, skip `.gitkeep`)
- [ ] Build substitution map from all `{{}}` placeholders
- [ ] Apply sed substitutions to all copied text files
- [ ] Print structured next-steps block (git init, gh repo create, push)

---

## Step 3 — `skill.md` (`/new-skill` entrypoint)
- [ ] Skill frontmatter: name, description, allowed-tools (Bash, AskUserQuestion)
- [ ] Guard: check `~/.claude/skills/new-skill/template/` exists
- [ ] AskUserQuestion: ask all 8 questions + output path
- [ ] Assemble CLI args, call `bin/new-skill-init.py` via Bash tool
- [ ] Display generated file list and next-steps output

---

## Step 4 — `skills/new-skill-upgrade/skill.md`
- [ ] Skill frontmatter
- [ ] `git pull` in `~/.claude/skills/new-skill/`
- [ ] Redeploy sub-skills: copy `skills/*` → `~/.claude/skills/`
- [ ] Print upgrade summary (git log --oneline -1)

---

## Step 5 — `setup` script
- [ ] Prereq check: git; exit 1 with clear message if missing
- [ ] `install`: clone → deploy sub-skills → print "Restart Claude Code"
- [ ] `update`: git pull → redeploy sub-skills
- [ ] `uninstall`: remove sub-skills → remove `~/.claude/skills/new-skill/`
- [ ] No hook registration (new-skill has no hooks)

---

## Step 6 — Verify commands (user runs after install)

```bash
# Check new-skill skill is discoverable
ls ~/.claude/skills/ | grep new-skill

# Check sub-skill deployed
ls ~/.claude/skills/new-skill-upgrade/

# Run the skill (inside Claude Code)
# /new-skill

# Manually test init script
python3 ~/.claude/skills/new-skill/bin/new-skill-init.py \
  --name test-skill \
  --purpose "Test scaffold" \
  --scope "Does nothing real" \
  --data "none" \
  --hooks "none" \
  --sub-skills "test-skill-upgrade" \
  --deps "python3" \
  --risks "none" \
  --org ibalasite \
  --output /tmp/test-skill

ls /tmp/test-skill/
cat /tmp/test-skill/CLAUDE.md | head -5
```
> ← user runs these; not executed in this repo
