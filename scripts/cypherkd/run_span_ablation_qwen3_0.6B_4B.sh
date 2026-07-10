#! /bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_PATH="$(cd "${SCRIPT_DIR}/../.." && pwd)"
TRAIN_SCRIPT="${SCRIPT_DIR}/cypherkd_qwen3_0.6B_4B.sh"
UPLOAD_SCRIPT="${BASE_PATH}/upload_to_hf.py"
LOG_DIR="${SPAN_ABLATION_LOG_DIR:-${BASE_PATH}/run_logs/span_ablation_$(date +%Y%m%d_%H%M%S)}"

ABLATIONS=(
  "wo_clause:clause"
  "wo_node:node_pattern"
  "wo_expression:expression"
)

mkdir -p "${LOG_DIR}"
echo "Span ablation logs: ${LOG_DIR}"

for ablation in "${ABLATIONS[@]}"; do
  tag="${ablation%%:*}"
  excluded_span_type="${ablation#*:}"
  log_file="${LOG_DIR}/${tag}.log"

  echo "Running CypherKD span ablation: ${tag} (exclude ${excluded_span_type})"
  echo "Log: ${log_file}"
  if SPAN_ABLATION_TAG="${tag}" \
    EXCLUDE_SPAN_TYPES="${excluded_span_type}" \
    bash "${TRAIN_SCRIPT}" "$@" 2>&1 | tee "${log_file}"; then
    echo "Finished CypherKD span ablation: ${tag}"
  else
    status=$?
    echo "Failed CypherKD span ablation: ${tag}. See log: ${log_file}" >&2
    exit "${status}"
  fi
done

if [[ "${SKIP_HF_UPLOAD:-0}" != "1" ]]; then
  upload_log="${LOG_DIR}/upload_to_hf.log"
  echo "Uploading CypherKD span ablation results to Hugging Face"
  echo "Upload log: ${upload_log}"
  PYTHONPATH="${BASE_PATH}" python "${UPLOAD_SCRIPT}" 2>&1 | tee "${upload_log}"
fi
