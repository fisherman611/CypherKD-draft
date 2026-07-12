"""Select 50 cases reproducing the first two full-test taxonomy columns."""

from __future__ import annotations

import argparse
import json
import math
import random
from collections import Counter
from pathlib import Path

from scripts.analyze_cypher_errors import MODEL_DIRS, load_json, question_lookup, repair_mojibake


GROUPS = ("schema_grounding", "graph_pattern_construction")


def objective(counts: list[int], targets: list[int]) -> int:
    return sum(abs(value - target) for value, target in zip(counts, targets))


def optimize(vectors: list[list[int]], size: int, targets: list[int], seed: int) -> set[int]:
    rng = random.Random(seed)
    best_selection: set[int] = set()
    best_score = math.inf
    all_indices = list(range(len(vectors)))

    for restart in range(30):
        selected = set(rng.sample(all_indices, size))
        counts = [sum(vectors[index][dimension] for index in selected) for dimension in range(len(targets))]
        score = objective(counts, targets)
        temperature = 2.0

        for _ in range(150_000):
            if score == 0:
                return selected
            remove = rng.choice(tuple(selected))
            add = rng.randrange(len(vectors))
            if add in selected:
                continue
            proposed_counts = [
                counts[dimension] - vectors[remove][dimension] + vectors[add][dimension]
                for dimension in range(len(targets))
            ]
            proposed_score = objective(proposed_counts, targets)
            delta = proposed_score - score
            if delta <= 0 or rng.random() < math.exp(-delta / max(temperature, 0.01)):
                selected.remove(remove)
                selected.add(add)
                counts = proposed_counts
                score = proposed_score
            temperature *= 0.99995
            if score < best_score:
                best_selection = set(selected)
                best_score = score
        rng.seed(seed + restart + 1)

    if best_score != 0:
        raise RuntimeError(f"Could not reach exact rounded marginal targets; best L1 error={best_score}")
    return best_selection


def analyze(args: argparse.Namespace) -> None:
    root = args.root.resolve()
    cases = [
        json.loads(line)
        for line in (root / args.cases).read_text(encoding="utf-8").splitlines()
        if line
    ]
    result_root = root / args.results
    model_rows = {
        model: load_json(result_root / directory / "test_result.json")
        for model, directory in MODEL_DIRS.items()
    }
    n = len(next(iter(model_rows.values())))
    benchmark = load_json(root / args.benchmark)
    lookup = question_lookup(benchmark)

    flags = {
        index: {model: {group: 0 for group in GROUPS} for model in MODEL_DIRS}
        for index in range(n)
    }
    local_indices: dict[int, int] = {}
    local_counter: Counter[str] = Counter()
    teacher_rows = model_rows[next(iter(MODEL_DIRS))]
    for index, row in enumerate(teacher_rows):
        local_indices[index] = local_counter[row["graph"]]
        local_counter[row["graph"]] += 1
    for case in cases:
        index = case["global_index"]
        for group in GROUPS:
            flags[index][case["model"]][group] = int(group in case["grouped_categories"])

    dimensions = [(model, group) for model in MODEL_DIRS for group in GROUPS]
    full_counts = [sum(flags[index][model][group] for index in range(n)) for model, group in dimensions]
    targets = [int(count * args.size / n + 0.5) for count in full_counts]
    vectors = [
        [flags[index][model][group] for model, group in dimensions]
        for index in range(n)
    ]
    selected = optimize(vectors, args.size, targets, args.seed)
    selected_counts = [sum(vectors[index][dimension] for index in selected) for dimension in range(len(dimensions))]

    samples = []
    for index in sorted(selected):
        gold = model_rows[next(iter(MODEL_DIRS))][index]["gold_cypher"]
        benchmark_row = lookup.get(gold) or lookup.get(repair_mojibake(gold)) or {}
        samples.append(
            {
                "global_index": index,
                "local_index_zero_based": local_indices.get(index),
                "graph": model_rows[next(iter(MODEL_DIRS))][index]["graph"],
                "qid": benchmark_row.get("qid"),
                "question": benchmark_row.get("nl_question"),
                "gold_cypher": gold,
                "predicted_cyphers": {
                    model: model_rows[model][index].get("pred_cypher")
                    for model in MODEL_DIRS
                },
                "metrics": {
                    model: model_rows[model][index].get("metrics", {})
                    for model in MODEL_DIRS
                },
                "labels": {
                    model: {group: bool(flags[index][model][group]) for group in GROUPS}
                    for model in MODEL_DIRS
                },
            }
        )

    output = {
        "selection_type": "representative_marginal_match",
        "seed": args.seed,
        "full_n": n,
        "selected_n": args.size,
        "groups": list(GROUPS),
        "samples": samples,
    }
    output_json = root / args.output_json
    output_json.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    output_jsonl = root / args.output_jsonl
    with output_jsonl.open("w", encoding="utf-8", newline="\n") as handle:
        for sample in samples:
            handle.write(json.dumps(sample, ensure_ascii=False) + "\n")

    lines = [
        "# Representative 50-sample subset for the first two taxonomy columns",
        "",
        "The subset matches the nearest feasible integer counts implied by the full 2,348-query rates. Selection uses only the two requested marginal labels.",
        "",
        "| Method | Full Schema | 50-sample Schema | Δ pp | Full Graph | 50-sample Graph | Δ pp |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for model_index, model in enumerate(MODEL_DIRS):
        schema_position = model_index * 2
        graph_position = schema_position + 1
        full_schema_rate = 100 * full_counts[schema_position] / n
        subset_schema_rate = 100 * selected_counts[schema_position] / args.size
        full_graph_rate = 100 * full_counts[graph_position] / n
        subset_graph_rate = 100 * selected_counts[graph_position] / args.size
        lines.append(
            f"| {model} | {full_counts[schema_position]} ({full_schema_rate:.2f}%) | "
            f"{selected_counts[schema_position]} ({subset_schema_rate:.2f}%) | {subset_schema_rate-full_schema_rate:+.2f} | "
            f"{full_counts[graph_position]} ({full_graph_rate:.2f}%) | "
            f"{selected_counts[graph_position]} ({subset_graph_rate:.2f}%) | {subset_graph_rate-full_graph_rate:+.2f} |"
        )

    lines.extend(
        [
            "",
            "## Selected cases",
            "",
            "| # | Graph / local index | QID | Question |",
            "|---:|---|---|---|",
        ]
    )
    for number, sample in enumerate(samples, start=1):
        question = (sample["question"] or "").replace("|", "\\|")
        lines.append(
            f"| {number} | {sample['graph']} #{sample['local_index_zero_based']} | "
            f"`{sample['qid']}` | {question} |"
        )
    lines.extend(
        [
            "",
            f"Machine-readable labels, metrics, and predictions: `{args.output_json}` and `{args.output_jsonl}`.",
            "",
        ]
    )
    output_md = root / args.output_md
    output_md.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    print(f"Selected {len(selected)} cases with exact rounded targets: {targets}")
    print(f"Saved {output_md}")
    print(f"Saved {output_json}")
    print(f"Saved {output_jsonl}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--cases", default="rebuttal/full_error_taxonomy_cases_seed42.jsonl")
    parser.add_argument("--results", default="results/qwen/42")
    parser.add_argument("--benchmark", default="benchmarks/Cypherbench/test.json")
    parser.add_argument("--size", type=int, default=50)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output-md", default="rebuttal/representative_50_first_two_columns_seed42.md")
    parser.add_argument("--output-json", default="rebuttal/representative_50_first_two_columns_seed42.json")
    parser.add_argument("--output-jsonl", default="rebuttal/representative_50_first_two_columns_seed42.jsonl")
    return parser.parse_args()


if __name__ == "__main__":
    analyze(parse_args())
