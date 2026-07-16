#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$project_root"

if [[ -x ".venv/bin/python" ]]; then
  python_command=".venv/bin/python"
else
  python_command="${PYTHON:-python3}"
fi

echo "Running Ruff..."
"$python_command" -m ruff check .

echo "Running mypy..."
"$python_command" -m mypy src

echo "Running pytest..."
"$python_command" -m pytest
