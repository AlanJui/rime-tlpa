# Git Tag 操作小抄（ops-git-tags.md）

> 適用：Git / GitHub。包含「建立、刪除、修正 tag」與「搭配 Release」的常用指令與排錯要點。

---

## 1) 檢視與建立 Tag

```bash
# 列出所有 tag
git tag --list

# 建立「輕量」tag（lightweight）
git tag v1.2.3

# 建立「註解」tag（annotated，推薦）
git tag -a v1.2.3 -m "v1.2.3"
# 或 GPG 簽名：git tag -s v1.2.3 -m "v1.2.3"
```

---

## 2) 推送／抓取 Tag

```bash
# 推送單一 tag
git push origin v1.2.3

# 一次推送所有本地 tag
git push origin --tags

# 抓取遠端所有 tag（並修剪已刪除者）
git fetch origin --tags --prune --prune-tags
```

---

## 3) 刪除 Tag

```bash
# 刪本機
git tag -d v1.2.3

# 刪遠端
git push origin --delete v1.2.3
# 或：git push origin :refs/tags/v1.2.3
```

> 小提醒：刪遠端後，其他人的本機仍會殘留該 tag，請他們 `git fetch origin --prune --prune-tags` 再清理本機 tag。

---

## 4) Tag 指錯 Commit？（更正流程）

```bash
# (A) 先刪遠端舊 tag
git push origin --delete v1.2.3

# (B) 在正確 commit 重建/改指向（建議用註解 tag）
git tag -fa v1.2.3 <正確commitSHA> -m "v1.2.3"

# (C) 推送新的 tag
git push origin v1.2.3
```

---

## 5) GitHub Release（搭配 gh CLI）

```bash
# 建立 Release（tag 已存在）
gh release create v1.2.3 -t "v1.2.3" -n "變更說明..."

# 指定目標分支/commit（tag 尚未存在時）
gh release create v1.2.3 --target main -t "v1.2.3" -n "變更說明..."

# 刪除 Release（保留 tag）
gh release delete v1.2.3 --yes
```

---

## 6) GitHub Actions（自動發行）必要權限

```yaml
permissions:
  contents: write
```

- 若用 `softprops/action-gh-release@v2`：
  ```yaml
  - uses: softprops/action-gh-release@v2
    with:
      tag_name: ${{ steps.meta.outputs.TAG }}
      target_commitish: ${{ steps.meta.outputs.REF }}
      prerelease: ${{ github.event.inputs.prerelease || false }}
      files: |
        dist/*.zip
        dist/*.sha256
  ```
- 若遇 403：檢查 workflow `permissions: contents: write`、Repo 的 **Settings → Actions → Workflow permissions** 是否開 **Read and write**；或改用 PAT（`token:` 指定 secrets）。

---

## 7) 常見錯誤與排解

- **`tag 'vX.Y.Z' already exists`**：本機已存在；改名或先 `git tag -d vX.Y.Z`。遠端同名時，請先刪遠端再推。
- **`Resource not accessible by integration`（403）**：GitHub Actions 權限不足，需 `permissions: contents: write` 或 PAT。
- **想確認某 tag 指到哪裡**：
  ```bash
  git rev-parse v1.2.3
  git show v1.2.3 --no-patch --pretty=fuller
  ```

---

## 8) 進階：重寫歷史移除某檔（全庫清除）

> 若需要將敏感檔案在「所有歷史」中移除，請使用 `git filter-repo` 或 BFG，並 **強制推送**。操作前務必備份。

```bash
# 安裝（其中一種）
pip install git-filter-repo
# or: brew install git-filter-repo（macOS）

# 例：移除某檔（可重複 --path 多次）；--invert-paths = 移除符合者、保留其他
git filter-repo --path secret.txt --invert-paths

# 推送重寫後歷史（請注意會影響所有人）
git push origin --force --tags
```

## del tags ```bash

使用方式

編輯陣列
打開腳本，把 TAGS=( ... ) 內的 tag 名稱改成你要刪的清單。

### 試跑（不動真格）

```bash
bash delete-tags.sh -n
```

### 正式刪遠端 tags（預設 origin）

```bash
bash delete-tags.sh -y
```

### 也刪本機 tag

```bash
bash delete-tags.sh -y --also-local
```

### 也刪同名 GitHub Release（需 gh 已登入）

```bash
bash delete-tags.sh -y --also-release
```

### 指定遠端（如果不是 origin）

```bash
bash delete-tags.sh -y --remote upstream
```

【補註】：

(1) 若遇到 保護的 tag 規則（Protected tags） 或權限不足，刪遠端會失敗；需調整 repo 設定或用有權限的帳號。

(2) --also-release 需要 gh 登入：gh auth login。

(3) 在 Windows Git Bash 上執行沒問題；若是 PowerShell 直接跑，請用 bash delete-tags.sh ...。
