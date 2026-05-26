# CypherKD

## 1. Environment Setup

Running on WSL/Linux is recommended.

Install `uv` if it is not already available:

```bash
pip install uv
```

Install dependencies:

```bash
uv sync
```

Activate the environment:

```bash
source .venv/bin/activate
```

## 2. Process Data

There are 2 ways to run data processing.

### Option 1: Run Each Command Manually

Process split `train`:

```bash
python3 process_data.py \
    --data-dir benchmarks/Cypherbench \
    --processed-data-dir processed_data/benchmarks/Cypherbench \
    --model-path Qwen/Qwen3-0.6B \
    --model-type qwen \
    --data-process-workers 8 \
    --max-prompt-length 797 --dev-num 1 --split train
```

Process split `valid`:

```bash
python3 process_data.py \
    --data-dir benchmarks/Cypherbench \
    --processed-data-dir processed_data/benchmarks/Cypherbench \
    --model-path Qwen/Qwen3-0.6B \
    --model-type qwen \
    --data-process-workers 8 \
    --max-prompt-length 797 --dev-num 1 --split valid
```

Process split `test`:

```bash
python3 process_data.py \
    --data-dir benchmarks/Cypherbench \
    --processed-data-dir processed_data/benchmarks/Cypherbench \
    --model-path Qwen/Qwen3-0.6B \
    --model-type qwen \
    --data-process-workers 8 \
    --max-prompt-length 947 --dev-num 1 --split test
```

### Option 2: Run the Sequential Script

```bash
bash scripts/process_cypherbench_qwen3_0.6B.sh
```

This script runs `train`, `valid`, then `test` sequentially.

## 3. Train Teacher LoRA

Run the Finetune LoRA script for the teacher model:

```bash
bash scripts/teacher_lora/lora_qwen3_4B.sh
```

The LoRA checkpoint will be saved under `results/finetune/qwen3/sft_4B/...`. Use the final checkpoint path as the teacher adapter path for the CypherKD step.

## 4. Train CypherKD

Run CypherKD with the `teacher-peft-path` produced by the previous step:

```bash
TEACHER_PEFT_PATH="results/finetune/qwen3/sft_4B/<your-run>/<checkpoint-step>" \
bash scripts/cypherkd/cypherkd_qwen3_0.6B_4B.sh
```

Replace `<your-run>/<checkpoint-step>` with the actual teacher LoRA adapter path.

## 5. Infer

Run inference with the student model and the trained LoRA checkpoint:

```bash
python3 infer.py \
    --benchmark Cypherbench \
    --data_source local \
    --model Qwen/Qwen3-0.6B \
    --ckpt_path results/qwen3/<cypherkd-run>/<checkpoint-step> \
    --device cuda \
    --batch-size 1 \
    --max-length 1034 \
    --output_path results/Cypherbench/cypherkd_predictions.json
```

For a quick debug run on a small subset:

```bash
python3 infer.py \
    --benchmark Cypherbench \
    --data_source local \
    --model Qwen/Qwen3-0.6B \
    --ckpt_path results/qwen3/<cypherkd-run>/<checkpoint-step> \
    --device cuda \
    --batch-size 1 \
    --max-length 1034 \
    --limit 10 \
    --output_path results/Cypherbench/cypherkd_predictions_debug.json
```
