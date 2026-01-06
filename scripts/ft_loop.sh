#!/usr/bin/env bash
set -euo pipefail

# Minimal outer loop driver.
# - Generates a prompt for the next actionable task
# - Prints instructions to run a Ralph-style loop runner
#
# This script does NOT call any LLM. Use it to generate the prompt file.

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
AGENT_NAME="${1:-}"

if [[ -z "${AGENT_NAME}" ]]; then
  echo "Usage: scripts/ft_loop.sh <AgentName>"
  echo "Example: scripts/ft_loop.sh Frontend_Dev_Alpha"
  exit 1
fi

python3 "${ROOT_DIR}/scripts/ft_orchestrator.py" --agent "${AGENT_NAME}" --out ".ft/prompt.md" --completion-promise "<promise>DONE</promise>"

echo
echo "Next step (example with Claude Code + ralph-wiggum):"
echo "/ralph-loop \"\$(cat .ft/prompt.md)\" --completion-promise \"<promise>DONE</promise>\" --max-iterations 40"
