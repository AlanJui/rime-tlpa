#!/usr/bin/env bash
# delete-tags.sh - 批次刪除 GitHub 遠端 tags（可選：本機 tag、GitHub Releases）
# 用法例：bash delete-tags.sh v0.1 v0.2 v0.3 v0.5.1 v0.5.2
# 進階：  bash delete-tags.sh -y --also-local --also-release v0.1 v0.2
#         bash delete-tags.sh --from-file tags.txt

set -Eeuo pipefail

# 預設參數
REMOTE="origin"
DRY_RUN=false
YES=false
ALSO_LOCAL=false
ALSO_RELEASE=false
FROM_FILE=""

# 收集的目標 tags（來自參數與/或檔案）
TAGS=()

# 彩色輸出
RED=$'\e[31m'; GREEN=$'\e[32m'; YELLOW=$'\e[33m'; CYAN=$'\e[36m'; BOLD=$'\e[1m'; CLR=$'\e[0m'
info(){  echo "${CYAN}[INFO]${CLR} $*"; }
warn(){  echo "${YELLOW}[WARN]${CLR} $*"; }
err(){   echo "${RED}[ERR ]${CLR} $*"; }
ok(){    echo "${GREEN}[ OK ]${CLR} $*"; }

usage(){
  cat <<'USAGE'
用法：
  bash delete-tags.sh [選項] <tag1> <tag2> ...

選項：
  -r, --remote <name>     指定遠端（預設 origin）
  -n, --dry-run           試跑（只顯示將執行動作，不實際刪）
  -y, --yes               不詢問，直接執行
      --also-local        同步刪除本機 tags
      --also-release      也刪同名 GitHub Release（需 gh 已登入）
      --from-file <path>  從檔案讀取 tags（每行一個，支援 # 註解）
  -h, --help              顯示說明並離開

範例：
  bash delete-tags.sh v0.1 v0.2 v0.3
  bash delete-tags.sh -y --also-local v0.5.1 v0.5.2
  bash delete-tags.sh -r upstream --dry-run v1.0.0
  bash delete-tags.sh --from-file tags.txt -y --also-release
USAGE
}

need_cmd(){ command -v "$1" >/dev/null 2>&1 || { err "缺少指令：$1"; exit 127; }; }

# 參數解析
while (( $# )); do
  case "$1" in
    -r|--remote)      REMOTE="${2:-}"; shift 2;;
    -n|--dry-run)     DRY_RUN=true; shift;;
    -y|--yes)         YES=true; shift;;
        --also-local) ALSO_LOCAL=true; shift;;
        --also-release) ALSO_RELEASE=true; shift;;
        --from-file)  FROM_FILE="${2:-}"; shift 2;;
    -h|--help)        usage; exit 0;;
    --) shift; break;;
    -*) err "未知參數：$1"; usage; exit 2;;
    *)  TAGS+=("$1"); shift;;
  esac
done

# 將 "--" 之後的全部視為 tags
if (( $# )); then
  TAGS+=("$@")
fi

need_cmd git
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { err "當前目錄不是 Git 版本庫"; exit 2; }

# 遠端存在性
if ! git remote | grep -qx "$REMOTE"; then
  err "找不到遠端：$REMOTE"
  info "可用遠端："; git remote -v
  exit 2
fi

# 從檔案讀 tags（選用）
if [[ -n "$FROM_FILE" ]]; then
  [[ -f "$FROM_FILE" ]] || { err "找不到檔案：$FROM_FILE"; exit 2; }
  while IFS= read -r line; do
    # 去除註解與前後空白
    line="${line%%#*}"
    line="$(echo "$line" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
    [[ -n "$line" ]] && TAGS+=("$line")
  done < "$FROM_FILE"
fi

# 沒指定任何 tag
if (( ${#TAGS[@]} == 0 )); then
  err "沒有指定要刪除的 tags。"
  usage; exit 2
fi

# --also-release 需要 gh
if $ALSO_RELEASE; then
  need_cmd gh
fi

remote_tag_exists(){
  local tag="$1"
  [[ -n "$(git ls-remote --tags "$REMOTE" "refs/tags/$tag" 2>/dev/null)" ]]
}
local_tag_exists(){
  local tag="$1"
  git show-ref --tags --verify --quiet "refs/tags/$tag"
}

# 確認
if ! $YES; then
  echo
  echo "${BOLD}即將刪除的遠端（$REMOTE）tags：${CLR}"
  for t in "${TAGS[@]}"; do echo "  - $t"; done
  $ALSO_LOCAL   && echo "（也會刪除本機 tag）"
  $ALSO_RELEASE && echo "（也會刪同名 GitHub Release）"
  $DRY_RUN      && echo "（DRY-RUN 試跑）"
  echo
  read -rp "確認執行？[y/N] " ans
  [[ "${ans:-}" =~ ^[Yy]$ ]] || { warn "已取消"; exit 0; }
fi

info "遠端：$REMOTE | dry-run=$DRY_RUN | also-local=$ALSO_LOCAL | also-release=$ALSO_RELEASE"
ok "目標 tags：${#TAGS[@]}"

cnt_ok=0; cnt_skip=0; cnt_err=0

for tag in "${TAGS[@]}"; do
  echo "----------------------------------------"
  info "處理：$tag"

  # 1) 刪遠端 tag
  if remote_tag_exists "$tag"; then
    if $DRY_RUN; then
      warn "[dry-run] 將刪遠端 tag：$REMOTE $tag"
    else
      if git push "$REMOTE" --delete "$tag"; then
        ok "已刪遠端 tag：$tag"
      else
        err "刪遠端 tag 失敗：$tag（可能受保護或權限不足）"
        cnt_err=$((cnt_err+1)); continue
      fi
    fi
  else
    warn "遠端不存在：$tag（略過刪遠端）"
    cnt_skip=$((cnt_skip+1))
  fi

  # 2) 刪本機 tag（可選）
  if $ALSO_LOCAL; then
    if local_tag_exists "$tag"; then
      if $DRY_RUN; then
        warn "[dry-run] 將刪本機 tag：$tag"
      else
        git tag -d "$tag" && ok "已刪本機 tag：$tag" || { err "刪本機 tag 失敗：$tag"; cnt_err=$((cnt_err+1)); continue; }
      fi
    else
      warn "本機不存在：$tag（略過刪本機）"
    fi
  fi

  # 3) 刪 GitHub Release（可選）
  if $ALSO_RELEASE; then
    if $DRY_RUN; then
      warn "[dry-run] 將刪 Release：$tag"
    else
      if gh release view "$tag" >/dev/null 2>&1; then
        gh release delete "$tag" --yes && ok "已刪 Release：$tag" || { err "刪 Release 失敗：$tag"; cnt_err=$((cnt_err+1)); continue; }
      else
        warn "無同名 Release：$tag（略過）"
      fi
    fi
  fi

  cnt_ok=$((cnt_ok+1))
done

echo "========================================"
ok   "完成：成功 $cnt_ok"
warn "略過：$cnt_skip"
[[ $cnt_err -gt 0 ]] && err "失敗：$cnt_err"

# 同步 tag 狀態
if ! $DRY_RUN; then
  info "同步遠端 tags 狀態到本機..."
  git fetch "$REMOTE" --tags --prune --prune-tags >/dev/null 2>&1 || true
  ok "已同步"
fi

