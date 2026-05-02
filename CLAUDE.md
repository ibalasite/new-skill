# new-skill — Project Spec

## 專案目標

互動式 Claude Code skill，用來快速建立符合既定慣例的新 skill。  
呼叫 `/new-skill`，回答 8 個問題，自動將 `template/` 複製到目標目錄並替換佔位符，  
輸出 git init / gh repo create / push 指令讓使用者自行執行。

**不需要每次重複討論**：scope boundary、目錄結構、hook 設計、sub-skill deploy 等決策  
已全部固化進 `template/`，每個從此 template 建立的 skill 自動繼承。

---

## Repo 結構（與 template 慣例完全一致）

```
new-skill/
├── CLAUDE.md
├── README.md
├── progress.md
├── skill.md                           ← /new-skill skill entrypoint
├── setup                              ← install / update / uninstall
├── bin/
│   └── new-skill-init.py              ← template copy + {{}} 替換邏輯
├── skills/
│   └── new-skill-upgrade/
│       └── skill.md                   ← /new-skill-upgrade sub-skill
└── template/                          ← 新 skill 的原始碼範本（含 {{}} 佔位符）
    ├── CLAUDE.md
    ├── README.md
    ├── progress.md
    ├── skill.md
    ├── setup
    ├── bin/.gitkeep
    └── skills/.gitkeep

安裝後 runtime：
~/.claude/skills/new-skill/            ← repo clone 到這裡
~/.claude/skills/new-skill/template/   ← skill 在這裡讀 template
~/.claude/skills/new-skill-upgrade/    ← sub-skill deploy 到這裡
```

---

## Repo Scope（Iron Law）

| 屬於這個 repo | 不屬於這個 repo |
|--------------|----------------|
| `template/` 範本檔案 | 執行 git init / gh repo create |
| `bin/new-skill-init.py` 原始碼 | 替使用者建立 GitHub repo |
| `skill.md` / `setup` 原始碼 | 修改 `~/.claude/settings.json` |

**開發期間 `template/` 不使用**，只有安裝後由 `skill.md` 在 runtime 讀取。

---

## Scope Boundary（明確不做的事）

- **不執行 git / gh 指令**：列出指令讓使用者自行執行
- **不修改 `~/.claude/settings.json`**：new-skill 本身不需要任何 hook
- **不觸碰使用者的專案目錄**：只在使用者指定的 output 路徑建立檔案
- **不建立 GitHub repo**：列出 `gh repo create` 指令讓使用者執行

---

## 無 Hook 設計

`new-skill` 是純 on-demand slash command，不需要 Stop / PostToolUse hooks。  
`setup` 不注冊任何 hook，也沒有 project data 目錄（不需要懶建立邏輯）。

---

## `bin/new-skill-init.py` 介面與行為

由 `skill.md` 透過 Bash tool 呼叫：

```bash
python3 ~/.claude/skills/new-skill/bin/new-skill-init.py \
  --name      "myskill" \
  --purpose   "Does X for Claude Code" \
  --scope     "Does not touch user project dir" \
  --data      "~/.myskill/config.json, lazily created by hooks" \
  --hooks     "Stop: session-end; PostToolUse: 5-min checkpoint" \
  --sub-skills "myskill-upgrade" \
  --deps      "python3, git, curl" \
  --risks     "Depends on tool calls for checkpoint" \
  --org       "ibalasite" \
  --output    "~/projects/myskill"
```

執行邏輯：
1. 確認 `~/.claude/skills/new-skill/template/` 存在（runtime guard）
2. 建立 `--output` 目錄（若不存在）
3. Recursively copy `template/` → output 目錄
4. 對所有複製的檔案執行 `{{}}` 佔位符替換（`sed` in-place）
5. 印出 next steps

---

## `skill.md` 行為（`/new-skill` 指令）

1. 確認 runtime 已安裝（`~/.claude/skills/new-skill/template/` 存在）
2. 用 `AskUserQuestion` 逐一詢問 8 個問題
3. 詢問 output 路徑（預設 `~/projects/{skill-name}`）
4. 組合參數，呼叫 `bin/new-skill-init.py` via Bash tool
5. 顯示產出路徑與 next steps

---

## 8 個初始問題（固定，不可省略）

| # | 問題 | 佔位符 |
|---|------|--------|
| 1 | Skill 名稱（kebab-case） | `{{SKILL_NAME}}` |
| 2 | 一句話說明 | `{{SKILL_PURPOSE}}` |
| 3 | 明確不做什麼 | `{{SKILL_SCOPE_BOUNDARY}}` |
| 4 | 資料模型（狀態存哪、誰建立） | `{{DATA_MODEL_DESC}}` |
| 5 | Hook 種類 + 行為 | `{{HOOKS_DESC}}` |
| 6 | Sub-skills 清單 | `{{SUB_SKILLS_DESC}}` |
| 7 | 外部依賴 | `{{DEPS}}` |
| 8 | 可行性風險 | `{{FEASIBILITY_RISKS}}` |

---

## 已固化的慣例（template 自動繼承，不需每次重新討論）

### Repo Scope Rule
Source repo 只負責 source code + git push。開發期間不執行任何 runtime 操作。

### Runtime Isolation Rule
- 安裝目標：`~/.claude/skills/{name}/`（整個 repo clone 到這裡）
- Sub-skills：`skills/*` → copy 到 `~/.claude/skills/`（install 和 update 都執行）
- Hook 注冊：透過 `bin/{name}-settings-hook.py` 管理 `~/.claude/settings.json`
- 安裝後不碰 source repo 目錄

### Project Data Rule
- 用戶專案目錄的資料由 hook 腳本懶建立（第一次執行時）
- 建立時同時寫入 `.gitignore`（`*`）
- `setup install` 不建立 project data 目錄

### Sub-skill Deploy Rule
```bash
for d in ~/.claude/skills/{name}/skills/*/; do
  name="$(basename "$d")"
  rm -rf ~/.claude/skills/"$name" && cp -r "$d" ~/.claude/skills/"$name"
done
```

### Uninstall Rule
移除 hooks + 移除 sub-skills + 移除 runtime dir。永遠不刪 project data。

---

## 實作順序

1. `template/` 範本檔（已存在，需確認完整性）
2. `bin/new-skill-init.py`（copy + 替換核心邏輯）
3. `skill.md`（`/new-skill` 互動 entrypoint）
4. `skills/new-skill-upgrade/skill.md`
5. `setup`（install/update/uninstall，無 hook 注冊）
6. 驗收指令清單
