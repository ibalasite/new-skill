# {{SKILL_NAME}} — Project Spec

## 專案目標

{{SKILL_PURPOSE}}

---

## Repo Scope（Iron Law）

此 repo 是**純原始碼 repo**，只負責 source code + git push to remote。  
**開發期間絕對不執行任何 runtime 操作。**

| 屬於這個 repo | 不屬於這個 repo |
|--------------|----------------|
| `bin/` 腳本原始碼 | 執行 `bin/` 腳本 |
| `setup` 腳本原始碼 | 執行 `setup install` |
| `skill.md` 內容 | 修改 `~/.claude/settings.json` |
| `skills/` sub-skill 原始碼 | 在當前目錄建立任何 runtime 資料 |

Runtime 操作全部由 `setup install` 在**使用者的機器**上執行。

---

## 架構設計

```
{repo-root}/
├── CLAUDE.md
├── README.md
├── progress.md
├── skill.md                              ← /{{SKILL_NAME}} 主 skill entrypoint
├── setup                                 ← install / update / uninstall
├── bin/
│   ├── {{SKILL_NAME}}-settings-hook.py   ← hook 注冊管理
│   └── ...                               ← 其他腳本
└── skills/
    └── {{SKILL_NAME}}-upgrade/
        └── skill.md                      ← /{{SKILL_NAME}}-upgrade sub-skill

安裝後的 runtime 位置（與 source repo 無關）：
~/.claude/skills/{{SKILL_NAME}}/          ← repo clone 到這裡
~/.claude/skills/{{SKILL_NAME}}-upgrade/  ← sub-skill deploy 到這裡
```

---

## Scope Boundary（明確不做的事）

{{SKILL_SCOPE_BOUNDARY}}

---

## 資料模型

{{DATA_MODEL_DESC}}

### 懶建立規則

Project data 目錄由 hook 腳本在**第一次執行時**建立，不由 `setup install` 建立：

```python
data_dir = Path(os.getcwd()) / ".{{SKILL_NAME}}"
if not data_dir.exists():
    data_dir.mkdir(parents=True)
    (data_dir / ".gitignore").write_text("*\n")
```

---

## Hook 設計

{{HOOKS_DESC}}

Hook 注冊方式：`bin/{{SKILL_NAME}}-settings-hook.py` 管理 `~/.claude/settings.json` 的讀寫。  
使用 `tempfile + os.replace` atomic write，避免設定檔損毀。  
Dedup guard：同一 hook 已存在時跳過，不重複注冊。

---

## Sub-skills

{{SUB_SKILLS_DESC}}

deploy 邏輯（install 和 update 都執行）：
```bash
for d in ~/.claude/skills/{{SKILL_NAME}}/skills/*/; do
  name="$(basename "$d")"
  rm -rf ~/.claude/skills/"$name"
  cp -r "$d" ~/.claude/skills/"$name"
done
```

---

## 外部依賴

{{DEPS}}

`setup` 開頭做 prereq check，缺少依賴時輸出清楚的錯誤訊息並 exit 1。

---

## 可行性風險

{{FEASIBILITY_RISKS}}

---

## 實作順序

1. `bin/` 核心庫（最底層，無外部依賴，可獨立測試）
2. Hook 腳本（依賴核心庫）
3. `bin/{{SKILL_NAME}}-settings-hook.py`（hook 注冊管理）
4. `skill.md`（主 skill entrypoint）
5. `skills/{{SKILL_NAME}}-upgrade/skill.md`（upgrade sub-skill）
6. `setup`（install/update/uninstall）
7. 整理驗收指令清單（使用者自行執行）

---

## 已知限制

{{KNOWN_LIMITATIONS}}
