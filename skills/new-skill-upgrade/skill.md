---
name: new-skill-upgrade
description: |
  Upgrade the new-skill installation to the latest version.
  Use when the user invokes /new-skill-upgrade.
allowed-tools:
  - Bash
---

# /new-skill-upgrade

Pull the latest version of new-skill and redeploy sub-skills.

---

## Step 1 — Guard: installed?

```bash
test -d "$HOME/.claude/skills/new-skill/.git"
```

**[AI 指令]** If not found, output:
```
[new-skill] Not installed. Run setup install first.
```
Then stop.

---

## Step 2 — Pull and redeploy

```bash
cd "$HOME/.claude/skills/new-skill" && git pull --ff-only
```

Then redeploy sub-skills:

```bash
SKILLS_SRC="$HOME/.claude/skills/new-skill/skills"
SKILLS_DST="$HOME/.claude/skills"
for d in "$SKILLS_SRC"/*/; do
  [ -d "$d" ] || continue
  name="$(basename "$d")"
  rm -rf "$SKILLS_DST/$name"
  cp -r "$d" "$SKILLS_DST/$name"
  echo "  · redeployed $name"
done
```

**[AI 指令]** Run both blocks via Bash tool.

---

## Step 3 — Show summary

```bash
cd "$HOME/.claude/skills/new-skill" && git log --oneline -1
```

Display: `[new-skill-upgrade] Updated to: {commit message}`
