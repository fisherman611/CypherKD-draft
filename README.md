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

## 2. Datasets:
Due to the size of the dataset, I just upload some small size dataset, for full dataset link here (https://huggingface.co/datasets/megagonlabs/cypherbench)

### Process Data

There are 2 ways to run data processing.

#### Option 1: Run Each Command Manually

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

#### Option 2: Run the Sequential Script

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

## 6. Cypherbench Graph Database Setup for Evaluation
Set Neo4j credentials before running evaluation:

```bash
export NEO4J_USERNAME=neo4j
export NEO4J_PASSWORD="<your-neo4j-password>"
```

Run Neo4j locally and create/load one database per Cypherbench graph. The scorer defaults to `neo4j://127.0.0.1:7687` and expects database names such as:

- `nba`
- `company`
- `geography`
- `movie`
- `politics`
- `fictional.character`
- `flight.accident`

Import Cypherbench graphs into Neo4j:

```bash
python3 import_db_to_neo4j.py --graphs all --overwrite
```

To import only selected graphs:

```bash
python3 import_db_to_neo4j.py --graphs nba company geography --overwrite
```

The import script reads graph files from:

```bash
benchmarks/Cypherbench/graphs/simplekg/<graph_name>_simplekg.json
```

If your Neo4j server is not running on the default host/port, override them:

```bash
python3 import_db_to_neo4j.py \
    --graphs nba \
    --overwrite \
    --host neo4j://127.0.0.1 \
    --port 7687
```

## 7. Evaluation

The inference output must be a JSON file containing `graph`, `gold_cypher`, and `pred_cypher` fields. The examples below assume the inference output was saved to:

```bash
results/Cypherbench/cypherkd_predictions.json
```

### Calculate Metrics Per Graph

Cypherbench example:

```bash
python3 src/calculate_scores_cypherbench.py \
    --input results/Cypherbench/cypherkd_predictions.json \
    --output_dir results/Cypherbench/calculated_scores_Qwen3_0.6B_cypherkd \
    --subset nba
```

Run the same command for other Cypherbench subsets by changing `--subset`, for example `company`, `geography`, `movie`, `politics`, `fictional_character`, or `flight_accident`.

Useful options:

- `--limit N`: evaluate only the first `N` samples for the selected graph
- `--metrics execution_accuracy psjs executable`: choose which metrics to compute
- `--host`, `--port`, `--database`, `--username`, `--password`: override Neo4j connection settings

### Aggregate Scores

Aggregate one scored graph file:

```bash
python3 src/calculate_scores_json.py \
    --input results/Cypherbench/calculated_scores_Qwen3_0.6B_cypherkd/nba_cyphers_result.json \
    --output results/Cypherbench/calculated_scores_Qwen3_0.6B_cypherkd/nba_summary.json
```

This reports the average of:

- `execution_accuracy`
- `psjs`
- `executable`
