#!/usr/bin/env bash
# delete-tags.sh - 批次刪除 GitHub Repo 的 tag（支援 Git Bash / Linux / macOS）
# 預設：刪除遠端 tag（origin）。可加 --also-local / --also-release。
# 需求：git（必要）；gh（可選，用於刪 Release）

set -Eeuo pipefail

#######################################
# ★ 在此維護欲刪除的 tag 名稱（可自由增減）
#######################################
TAGS=(
  "v0.5.1"
  "v0.5.2"
  # "kb-2024-09-30"
)

#######################################
# 參數預設
#######################################
REMOTE="origin"
DRY_RUN=false
YES=false
ALSO_LOCAL=false
ALSO_RELEASE=false

#######################################
# 顏色與輸出
#######################################
RED=$'\e[31m'; GREEN=$'\e[32m'; YELLOW=$'\e[33m'; CYAN=$'\e[36m'; BOLD=$'\e[1m'; CLR=$'\e[0m'
info(){  echo "${CYAN}[INFO]${CLR} $*"; }
warn(){  echo "${YELLOW}[WARN]${CLR} $*"; }
err(){   echo "${RED}[ERR ]${CLR} $*"; }
ok(){    echo "${GREEN}[ OK ]${CLR} $*"; }

#######################################
# 工具檢查
#######################################
need_cmd(){ command -v "$1" >/dev/null 2>&1 || { err "缺少指令：$1"; exit 127; }; }

#######################################
# 使用說明
#######################################
usage(){
  cat <<'USAGE'
用法：
  bash delete-tags.sh [選項]

選項：
  -r, --remote <name>     指定遠端（預設 origin）
  -n, --dry-run           試跑，不做實際刪除
  -y, --yes               不詢問，直接執行
      --also-local        同步刪除本機 tag
      --also-release      也刪除同名 GitHub Release（需 gh 已登入）
  -h, --help              顯示說明

修改 TAGS 陣列以設定要刪的 tag 清單。
範例：
  bash delete-tags.sh -r origin --also-local
  bash delete-tags.sh -y --also-release
  bash delete-tags.sh -n  # 先看會刪哪些，再正式執行
USAGE
}

#######################################
# 參數解析
#######################################
while (( $# )); do
  case "$1" in
    -r|--remote)      REMOTE="${2:-}"; shift 2;;
    -n|--dry-run)     DRY_RUN=true; shift;;
    -y|--yes)         YES=true; shift;;
        --also-local) ALSO_LOCAL=true; shift;;
        --also-release) ALSO_RELEASE=true; shift;;
    -h|--help)        usage; exit 0;;
    *) err "未知參數：$1"; usage; exit 2;;
  esac
done

need_cmd git

# 檢查是否在 Git 版本庫內
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { err "當前目錄不是 Git 版本庫"; exit 2; }

# 檢查遠端是否存在
if ! git remote | grep -qx "$REMOTE"; then
  err "找不到遠端：$REMOTE"
  info "可用遠端："
  git remote -v
  exit 2
fi

# 需要時檢查 gh
if $ALSO_RELEASE; then
  if ! command -v gh >/dev/null 2>&1; then
    err "選了 --also-release 但未安裝 GitHub CLI（gh）"
    info "請安裝並執行：gh auth login"
    exit 2
  fi
fi

#######################################
# 輔助：存在檢查
#######################################
remote_tag_exists(){
  local tag="$1"
  # ls-remote 回傳非空表示存在（含 ^{} 參考，僅需判斷有無）
  [[ -n "$(git ls-remote --tags "$REMOTE" "refs/tags/$tag" 2>/dev/null)" ]]
}

local_tag_exists(){
  local tag="$1"
  git show-ref --tags --verify --quiet "refs/tags/$tag"
}

#######################################
# 確認
#######################################
if ! $YES; then
  echo
  echo "${BOLD}將刪除的遠端（$REMOTE）tags：${CLR}"
  for t in "${TAGS[@]}"; do echo "  - $t"; done
  $ALSO_LOCAL   && echo "（同時會刪除本機 tags）"
  $ALSO_RELEASE && echo "（同時會刪除同名 GitHub Releases）"
  $DRY_RUN      && echo "（DRY-RUN：不會真的刪）"
  echo
  read -rp "確認執行？[y/N] " ans
  [[ "${ans:-}" =~ ^[Yy]$ ]] || { warn "已取消"; exit 0; }
fi

#######################################
# 執行
#######################################
total=${#TAGS[@]}
cnt_ok=0; cnt_skip=0; cnt_err=0

info "遠端：$REMOTE | 目標 tags：$total | dry-run=$DRY_RUN | also-local=$ALSO_LOCAL | also-release=$ALSO_RELEASE"

for tag in "${TAGS[@]}"; do
  echo "----------------------------------------"
  info "處理 tag：$tag"

  # 1) 刪遠端 tag
  if remote_tag_exists "$tag"; then
    if $DRY_RUN; then
      warn "[dry-run] 將刪除遠端 tag：$REMOTE $tag"
    else
      if git push "$REMOTE" --delete "$tag"; then
        ok "已刪遠端 tag：$tag"
      else
        err "刪遠端 tag 失敗：$tag（可能受保護、或權限不足）"
        ((cnt_err++))
        continue
      fi
    fi
  else
    warn "遠端不存在該 tag：$tag（略過刪遠端）"
    ((cnt_skip++))
  fi

  # 2) 刪本機 tag（可選）
  if $ALSO_LOCAL; then
    if local_tag_exists "$tag"; then
      if $DRY_RUN; then
        warn "[dry-run] 將刪除本機 tag：$tag"
      else
        git tag -d "$tag" && ok "已刪本機 tag：$tag" || { err "刪本機 tag 失敗：$tag"; ((cnt_err++)); continue; }
      fi
    else
      warn "本機不存在該 tag：$tag（略過刪本機）"
    fi
  fi

  # 3) 刪 GitHub Release（可選）
  if $ALSO_RELEASE; then
    if $DRY_RUN; then
      warn "[dry-run] 將刪 GitHub Release：$tag"
    else
      if gh release view "$tag" >/dev/null 2>&1; then
        gh release delete "$tag" --yes && ok "已刪 Release：$tag" || { err "刪 Release 失敗：$tag"; ((cnt_err++)); continue; }
      else
        warn "無同名 Release：$tag（略過）"
      fi
    fi
  fi

  ((cnt_ok++))
done

echo "========================================"
ok   "完成：成功 $cnt_ok"
warn "略過：$cnt_skip"
[[ $cnt_err -gt 0 ]] && err "失敗：$cnt_err"
echo

# 建議同步一下 tags
if ! $DRY_RUN; then
  info "同步遠端 tags 狀態到本機..."
  git fetch "$REMOTE" --tags --prune --prune-tags >/dev/null 2>&1 || true
  ok "已同步"
fi

