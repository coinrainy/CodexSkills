#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"
TARGET_ROOT="${HOME}/.codex/skills"
SKILLS=(
  "gnn-paper-reproduction"
  "gnn-repo-runner"
  "gnn-idea-lab"
  "gnn-experiment-review"
)

mkdir -p "${TARGET_ROOT}"

for skill in "${SKILLS[@]}"; do
  src="${SOURCE_DIR}/${skill}"
  dst="${TARGET_ROOT}/${skill}"

  if [[ ! -d "${src}" ]]; then
    echo "Skip missing skill: ${src}"
    continue
  fi

  rm -rf "${dst}"
  cp -a "${src}" "${dst}"
  echo "Installed ${skill} -> ${dst}"
done

echo "Done. Skills installed to ${TARGET_ROOT}"
