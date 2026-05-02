#!/usr/bin/env python3
"""
new-skill-init.py — copy template/ and substitute {{}} placeholders.
Called by skill.md via Bash tool.
"""
import argparse, os, shutil, sys, re
from pathlib import Path

RUNTIME = Path.home() / ".claude" / "skills" / "new-skill"
TEMPLATE_DIR = RUNTIME / "template"

def die(msg):
    print(f"[new-skill] ERROR: {msg}", file=sys.stderr)
    sys.exit(1)

def log(msg):
    print(f"[new-skill] {msg}")

def build_substitutions(args):
    year = __import__("datetime").date.today().year
    return {
        "SKILL_NAME":           args.name,
        "SKILL_PURPOSE":        args.purpose,
        "SKILL_SCOPE_BOUNDARY": args.scope,
        "DATA_MODEL_DESC":      args.data,
        "HOOKS_DESC":           args.hooks,
        "SUB_SKILLS_DESC":      args.sub_skills,
        "DEPS":                 args.deps,
        "FEASIBILITY_RISKS":    args.risks,
        "KNOWN_LIMITATIONS":    args.risks,
        "PRICING_NOTE":         "N/A",
        "GITHUB_ORG":           args.org,
        "YEAR":                 str(year),
    }

def substitute(text, subs):
    for key, val in subs.items():
        text = text.replace("{{" + key + "}}", val)
    return text

def is_text_file(path):
    try:
        with open(path, "rb") as f:
            chunk = f.read(1024)
        return b"\x00" not in chunk
    except OSError:
        return False

def copy_template(src_dir, dst_dir, subs):
    dst_dir.mkdir(parents=True, exist_ok=True)
    copied = []

    for src in src_dir.rglob("*"):
        if not src.is_file():
            continue
        if src.name == ".gitkeep":
            # Create the parent directory but skip the file itself
            rel = src.relative_to(src_dir)
            (dst_dir / rel.parent).mkdir(parents=True, exist_ok=True)
            continue

        rel = src.relative_to(src_dir)
        dst = dst_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(src, dst)

        if is_text_file(dst):
            content = dst.read_text(encoding="utf-8", errors="replace")
            dst.write_text(substitute(content, subs), encoding="utf-8")

        copied.append(str(rel))

    return copied

def main():
    p = argparse.ArgumentParser(description="Scaffold a new skill from template")
    p.add_argument("--name",       required=True)
    p.add_argument("--purpose",    required=True)
    p.add_argument("--scope",      required=True)
    p.add_argument("--data",       required=True)
    p.add_argument("--hooks",      required=True)
    p.add_argument("--sub-skills", required=True, dest="sub_skills")
    p.add_argument("--deps",       required=True)
    p.add_argument("--risks",      required=True)
    p.add_argument("--org",        default="ibalasite")
    p.add_argument("--output",     required=True)
    args = p.parse_args()

    # Validate name
    if not re.match(r"^[a-z][a-z0-9-]*$", args.name):
        die(f"Skill name must be kebab-case (lowercase + hyphens): {args.name!r}")

    # Guard: template must exist (runtime installed)
    if not TEMPLATE_DIR.exists():
        die(
            f"Template not found at {TEMPLATE_DIR}\n"
            "Install new-skill first:\n"
            "  git clone https://github.com/ibalasite/new-skill.git ~/.claude/skills/new-skill\n"
            "  ~/.claude/skills/new-skill/setup install"
        )

    output = Path(args.output).expanduser().resolve()

    if output.exists() and any(output.iterdir()):
        die(f"Output directory already exists and is not empty: {output}")

    log(f"Scaffolding '{args.name}' → {output}")

    subs = build_substitutions(args)
    copied = copy_template(TEMPLATE_DIR, output, subs)

    log(f"Created {len(copied)} files:")
    for f in sorted(copied):
        print(f"  {f}")

    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  Next steps")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  cd {output}")
    print(f"  git init && git add -A")
    print(f"  git commit -m 'feat: init from new-skill template'")
    print(f"  gh repo create {args.org}/{args.name} --public")
    print(f"  git remote add origin https://github.com/{args.org}/{args.name}.git")
    print(f"  git push -u origin main")
    print()
    print("  Then open progress.md — Step 1 is already DONE.")
    print()

if __name__ == "__main__":
    main()
