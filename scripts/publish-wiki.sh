#!/usr/bin/env bash
set -euo pipefail

repo_url="https://github.com/infinitepwn/cs-knowledge-tree.wiki.git"
workdir="${TMPDIR:-/tmp}/cs-knowledge-tree.wiki"
source_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/wiki"

if [ ! -d "$source_dir" ]; then
  echo "wiki source directory not found: $source_dir" >&2
  exit 1
fi

rm -rf "$workdir"
git clone "$repo_url" "$workdir"

find "$workdir" -mindepth 1 -maxdepth 1 ! -name ".git" -exec rm -rf {} +
cp "$source_dir"/*.md "$workdir"/

cd "$workdir"
git add .
if git diff --cached --quiet; then
  echo "No wiki changes to publish."
  exit 0
fi

git commit -m "Publish wiki pages"
git push
