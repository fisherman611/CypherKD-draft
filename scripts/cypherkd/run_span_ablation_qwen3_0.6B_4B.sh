#! /bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_PATH="$(cd "${SCRIPT_DIR}/../.." && pwd)"
TRAIN_SCRIPT="${SCRIPT_DIR}/cypherkd_qwen3_0.6B_4B.sh"
UPLOAD_SCRIPT="${BASE_PATH}/upload_to_hf.py"

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
    bash "${TRAIN_SCRIPT}" "$@"
done

if [[ "${SKIP_HF_UPLOAD:-0}" != "1" ]]; then
  echo "Uploading CypherKD span ablation results to Hugging Face"
  PYTHONPATH="${BASE_PATH}" python "${UPLOAD_SCRIPT}"
fi
