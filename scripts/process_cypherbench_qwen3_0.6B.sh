#! /bin/bash
set -e

python3 process_data.py \
    --data-dir benchmarks/Cypherbench \
    --processed-data-dir processed_data/benchmarks/Cypherbench \
    --model-path Qwen/Qwen3-0.6B \
    --model-type qwen \
    --data-process-workers 8 \
    --max-prompt-length 797 --dev-num 1 --split train

python3 process_data.py \
    --data-dir benchmarks/Cypherbench \
    --processed-data-dir processed_data/benchmarks/Cypherbench \
    --model-path Qwen/Qwen3-0.6B \
    --model-type qwen \
    --data-process-workers 8 \
    --max-prompt-length 797 --dev-num 1 --split valid

python3 process_data.py \
    --data-dir benchmarks/Cypherbench \
    --processed-data-dir processed_data/benchmarks/Cypherbench \
    --model-path Qwen/Qwen3-0.6B \
    --model-type qwen \
    --data-process-workers 8 \
    --max-prompt-length 947 --dev-num 1 --split test
