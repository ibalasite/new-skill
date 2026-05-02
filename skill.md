---
name: new-skill
description: |
  Scaffold a new Claude Code skill from template.
  Use when the user invokes /new-skill or asks to create a new skill.
allowed-tools:
  - Bash
  - AskUserQuestion
---

# /new-skill — New Skill Scaffolder

Scaffold a new Claude Code skill by answering 8 questions.

---

## Step 1 — Guard: runtime installed?

```bash
_TEMPLATE="$HOME/.claude/skills/new-skill/template"
test -d "$_TEMPLATE"
```

**[AI 指令]** Run the check. If the template directory does not exist, output:

```
[new-skill] Not installed. Run:
  git clone https://github.com/ibalasite/new-skill.git ~/.claude/skills/new-skill
  ~/.claude/skills/new-skill/setup install
```

Then stop. Do not proceed.

---

## Step 2 — Ask 8 questions

Use `AskUserQuestion` to collect answers. Ask all 8 in sequence.

```
question: "1/8  Skill name (kebab-case, e.g. getcost, my-tool)"
question: "2/8  One-line purpose — what does this skill do?"
question: "3/8  Scope boundary — what does it explicitly NOT do?"
question: "4/8  Data model — where does state live, and who creates it?"
         hint: "e.g. {project}/.myskill/data.json, lazily created by Stop hook"
question: "5/8  Hook types + behavior"
         hint: "e.g. Stop: session-end accounting; PostToolUse: 5-min checkpoint  |  or: none"
question: "6/8  Sub-skills to ship in skills/"
         hint: "e.g. myskill-upgrade  |  or: none (upgrade sub-skill still recommended)"
question: "7/8  External dependencies for prereq check"
         hint: "e.g. python3, git, curl"
question: "8/8  Feasibility risks or known limitations"
```

Then ask:

```
question: "GitHub org / username"
default: "ibalasite"

question: "Output directory"
default: "~/projects/{skill-name from Q1}"
```

---

## Step 3 — Run init script

Assemble arguments from the answers above and run:

```bash
python3 "$HOME/.claude/skills/new-skill/bin/new-skill-init.py" \
  --name      "{Q1}" \
  --purpose   "{Q2}" \
  --scope     "{Q3}" \
  --data      "{Q4}" \
  --hooks     "{Q5}" \
  --sub-skills "{Q6}" \
  --deps      "{Q7}" \
  --risks     "{Q8}" \
  --org       "{org}" \
  --output    "{output}"
```

**[AI 指令]** Run via Bash tool. Display the full output to the user.

---

## Step 4 — Confirm and show next steps

If the script exits 0, tell the user:

```
[new-skill] Scaffolded → {output}

Next steps:
  cd {output}
  git init && git add -A
  git commit -m "feat: init from new-skill template"
  gh repo create {org}/{skill-name} --public
  git remote add origin https://github.com/{org}/{skill-name}.git
  git push -u origin main

Then open progress.md — Step 1 is already DONE.
```
