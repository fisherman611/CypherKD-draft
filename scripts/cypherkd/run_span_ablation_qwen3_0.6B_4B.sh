#! /bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRAIN_SCRIPT="${SCRIPT_DIR}/cypherkd_qwen3_0.6B_4B.sh"

ABLATIONS=(
  "wo_clause:clause"
  "wo_node:node_pattern"
  "wo_expression:expression"
)

for ablation in "${ABLATIONS[@]}"; do
  tag="${ablation%%:*}"
  excluded_span_type="${ablation#*:}"

  echo "Running CypherKD span ablation: ${tag} (exclude ${excluded_span_type})"
  SPAN_ABLATION_TAG="${tag}" \
    EXCLUDE_SPAN_TYPES="${excluded_span_type}" \
    "${TRAIN_SCRIPT}" "$@"
done
