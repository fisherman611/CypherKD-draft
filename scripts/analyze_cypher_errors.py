"""Deterministic CypherBench error-taxonomy analysis.

The script compares each prediction with its gold Cypher only when execution
accuracy is not 1. A case may receive more than one grouped label. It writes an
auditable JSONL file containing every failing case and a Markdown summary table.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


MODEL_DIRS = {
    "Qwen3-4B (Teacher)": "calculated_scores_Qwen3_4B_Instruct_2507",
    "Qwen3-0.6B (SFT)": "calculated_scores_Qwen3_0.6B",
    "CSD": "calculated_scores_Qwen3_0.6B_4B_csd",
    "DistiLLM": "calculated_scores_Qwen3_0.6B_distill_distillm",
    "CypherKD": "cypherkd_qwen_kd0.6_wrel0.6",
}

GROUPS = (
    "schema_grounding",
    "graph_pattern_construction",
    "constraint_aggregation_logic",
    "result_formulation",
)

REL_RE = re.compile(r"(?P<left><-|-)\s*\[(?P<body>[^\]]*)\]\s*(?P<right>->|-)")
LABEL_RE = re.compile(r"\(\s*(?:[A-Za-z_]\w*\s*)?:\s*([A-Za-z_]\w*)")
DOT_PROPERTY_RE = re.compile(r"\b[A-Za-z_]\w*\.([A-Za-z_]\w*)\b")
MAP_PROPERTY_RE = re.compile(r"\{([^{}]*)\}")
NAME_VALUE_RE = re.compile(r"\bname\s*:\s*'((?:\\'|[^'])*)'")
AGG_RE = re.compile(r"\b(count|sum|avg|min|max|collect)\s*\(([^)]*)\)", re.I)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def execution_correct(value: Any) -> bool:
    try:
        return float(value) == 1.0
    except (TypeError, ValueError):
        return False


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def declared_variables(query: str) -> list[str]:
    variables: list[str] = []
    for match in re.finditer(r"\(\s*([A-Za-z_]\w*)\s*(?=[:{)])", query):
        if match.group(1) not in variables:
            variables.append(match.group(1))
    for match in re.finditer(r"\[\s*([A-Za-z_]\w*)\s*(?=[:{\]])", query):
        if match.group(1) not in variables:
            variables.append(match.group(1))
    return variables


def canonical(query: str) -> str:
    result = compact(query)
    for index, variable in enumerate(declared_variables(query)):
        result = re.sub(rf"\b{re.escape(variable)}\b", f"v{index}", result)
    return result


def relationship_features(query: str) -> tuple[list[str], list[str]]:
    types: list[str] = []
    directions: list[str] = []
    for match in REL_RE.finditer(query):
        rel_type = re.search(r":\s*([A-Za-z_]\w*)", match.group("body"))
        types.append(rel_type.group(1) if rel_type else "<untyped>")
        if match.group("left") == "<-":
            directions.append("left")
        elif match.group("right") == "->":
            directions.append("right")
        else:
            directions.append("undirected")
    return types, directions


def properties(query: str) -> set[str]:
    result = set(DOT_PROPERTY_RE.findall(query))
    for body in MAP_PROPERTY_RE.findall(query):
        result.update(re.findall(r"(?:^|,)\s*([A-Za-z_]\w*)\s*:", body))
    return result


def clauses(query: str) -> Counter[str]:
    upper = query.upper()
    return Counter(
        {
            "match": len(re.findall(r"(?<!OPTIONAL )\bMATCH\b", upper)),
            "optional_match": len(re.findall(r"\bOPTIONAL\s+MATCH\b", upper)),
            "call": len(re.findall(r"\bCALL\s*\{", upper)),
            "union": len(re.findall(r"\bUNION\b", upper)),
            "union_all": len(re.findall(r"\bUNION\s+ALL\b", upper)),
            "unwind": len(re.findall(r"\bUNWIND\b", upper)),
        }
    )


def filters(query: str) -> list[str]:
    matches = re.findall(
        r"\bWHERE\b(.*?)(?=\bWITH\b|\bRETURN\b|\bORDER\s+BY\b|\bUNION\b|}|$)",
        query,
        flags=re.I | re.S,
    )
    return [canonical(match) for match in matches]


def aggregate_features(query: str) -> list[tuple[str, bool, str]]:
    result = []
    canonical_query = canonical(query)
    for function, argument in AGG_RE.findall(canonical_query):
        argument = compact(argument)
        distinct = bool(re.match(r"(?i)DISTINCT\b", argument))
        argument = re.sub(r"(?i)^DISTINCT\s+", "", argument)
        result.append((function.lower(), distinct, argument))
    return result


def final_return(query: str) -> str:
    returns = re.findall(
        r"\bRETURN\b(.*?)(?=\bORDER\s+BY\b|\bLIMIT\b|\bUNION\b|}|$)",
        canonical(query),
        flags=re.I | re.S,
    )
    return compact(returns[-1]) if returns else ""


def schema_vocabulary(gold_rows: list[dict[str, Any]]) -> dict[str, set[str]]:
    vocab: dict[str, dict[str, set[str]]] = defaultdict(
        lambda: {"labels": set(), "relationships": set(), "properties": set()}
    )
    for row in gold_rows:
        graph = row["graph"]
        query = row["gold_cypher"]
        vocab[graph]["labels"].update(LABEL_RE.findall(query))
        vocab[graph]["relationships"].update(relationship_features(query)[0])
        vocab[graph]["properties"].update(properties(query))
    return dict(vocab)


def classify(
    gold: str,
    prediction: str,
    graph: str,
    vocab: dict[str, dict[str, set[str]]],
) -> tuple[list[str], dict[str, list[str]]]:
    labels: dict[str, list[str]] = {group: [] for group in GROUPS}

    gold_labels = LABEL_RE.findall(gold)
    pred_labels = LABEL_RE.findall(prediction)
    gold_rels, gold_dirs = relationship_features(gold)
    pred_rels, pred_dirs = relationship_features(prediction)
    gold_props = properties(gold)
    pred_props = properties(prediction)
    gold_entities = NAME_VALUE_RE.findall(gold)
    pred_entities = NAME_VALUE_RE.findall(prediction)

    if Counter(gold_labels) != Counter(pred_labels):
        labels["schema_grounding"].append("wrong_entity_type")
    if Counter(gold_rels) != Counter(pred_rels):
        labels["schema_grounding"].append("wrong_relationship_type")
    if gold_props != pred_props:
        labels["schema_grounding"].append("wrong_property_type")
    if Counter(gold_entities) != Counter(pred_entities):
        labels["schema_grounding"].append("entity_linking")

    graph_vocab = vocab.get(graph, {})
    unknown = {
        "labels": sorted(set(pred_labels) - graph_vocab.get("labels", set())),
        "relationships": sorted(set(pred_rels) - graph_vocab.get("relationships", set())),
        "properties": sorted(pred_props - graph_vocab.get("properties", set())),
    }
    if any(unknown.values()):
        details = "; ".join(f"{key}={','.join(value)}" for key, value in unknown.items() if value)
        labels["schema_grounding"].append(f"schema_violation({details})")

    if gold_dirs != pred_dirs:
        labels["graph_pattern_construction"].append("reversed_or_changed_direction")
    gold_clauses = clauses(gold)
    pred_clauses = clauses(prediction)
    structural_keys = ("match", "optional_match", "call", "union", "union_all")
    if len(gold_rels) != len(pred_rels) or any(
        gold_clauses[key] != pred_clauses[key] for key in structural_keys
    ):
        labels["graph_pattern_construction"].append("pattern_not_aligned")

    if filters(gold) != filters(prediction):
        labels["constraint_aggregation_logic"].append("incorrect_filtering")
    gold_aggregates = aggregate_features(gold)
    pred_aggregates = aggregate_features(prediction)
    if gold_aggregates != pred_aggregates:
        labels["constraint_aggregation_logic"].append("incorrect_grouping_or_aggregation")
    elif gold_aggregates and gold_clauses["optional_match"] != pred_clauses["optional_match"]:
        labels["constraint_aggregation_logic"].append("incorrect_aggregation_scope")

    if final_return(gold) != final_return(prediction):
        labels["result_formulation"].append("results_not_aligned_with_question")
    dedup_signature_gold = (
        len(re.findall(r"\bDISTINCT\b", gold, re.I)),
        gold_clauses["unwind"],
        gold_clauses["union_all"],
    )
    dedup_signature_pred = (
        len(re.findall(r"\bDISTINCT\b", prediction, re.I)),
        pred_clauses["unwind"],
        pred_clauses["union_all"],
    )
    if dedup_signature_gold != dedup_signature_pred:
        labels["result_formulation"].append("incorrect_deduplication")

    labels = {group: reasons for group, reasons in labels.items() if reasons}
    return list(labels), labels


def repair_mojibake(text: str) -> str:
    try:
        return text.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text


def question_lookup(benchmark: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    result = {}
    for row in benchmark:
        result[row["gold_cypher"]] = row
        result[repair_mojibake(row["gold_cypher"])] = row
    return result


def analyze(args: argparse.Namespace) -> None:
    root = args.root.resolve()
    result_root = root / args.results
    benchmark = load_json(root / args.benchmark)
    lookup = question_lookup(benchmark)

    model_rows = {
        model: load_json(result_root / directory / "test_result.json")
        for model, directory in MODEL_DIRS.items()
    }
    lengths = {model: len(rows) for model, rows in model_rows.items()}
    if len(set(lengths.values())) != 1:
        raise ValueError(f"Model result lengths differ: {lengths}")
    n = next(iter(lengths.values()))
    for index in range(n):
        golds = {rows[index]["gold_cypher"] for rows in model_rows.values()}
        if len(golds) != 1:
            raise ValueError(f"Gold queries are not aligned at global index {index}")

    gold_rows = model_rows["Qwen3-4B (Teacher)"]
    vocab = schema_vocabulary(gold_rows)
    local_indices: list[int] = []
    local_counter: Counter[str] = Counter()
    for row in gold_rows:
        local_indices.append(local_counter[row["graph"]])
        local_counter[row["graph"]] += 1

    counts = {model: Counter({group: 0 for group in GROUPS}) for model in MODEL_DIRS}
    failing = Counter()
    unclassified = Counter()
    cases: list[dict[str, Any]] = []

    for model, rows in model_rows.items():
        for index, row in enumerate(rows):
            metric = row.get("metrics", {}).get("execution_accuracy")
            if execution_correct(metric):
                continue
            failing[model] += 1
            gold = row["gold_cypher"]
            prediction = row.get("pred_cypher") or ""
            grouped, evidence = classify(gold, prediction, row["graph"], vocab)
            if not grouped:
                unclassified[model] += 1
            for group in grouped:
                counts[model][group] += 1
            benchmark_row = lookup.get(gold) or lookup.get(repair_mojibake(gold)) or {}
            cases.append(
                {
                    "model": model,
                    "global_index": index,
                    "local_index_zero_based": local_indices[index],
                    "graph": row["graph"],
                    "qid": benchmark_row.get("qid"),
                    "question": benchmark_row.get("nl_question"),
                    "execution_accuracy": metric,
                    "psjs": row.get("metrics", {}).get("psjs"),
                    "used_in_summary": bool(grouped),
                    "taxonomy_version": "deterministic-v1",
                    "grouped_categories": grouped,
                    "evidence": evidence,
                    "gold_cypher": gold,
                    "pred_cypher": prediction,
                }
            )

    cases_path = root / args.cases_output
    cases_path.parent.mkdir(parents=True, exist_ok=True)
    with cases_path.open("w", encoding="utf-8", newline="\n") as handle:
        for case in cases:
            handle.write(json.dumps(case, ensure_ascii=False) + "\n")

    headers = [
        "Method",
        "n",
        "Schema grounding ↓",
        "Graph-pattern construction ↓",
        "Constraint/aggregation logic ↓",
        "Result formulation ↓",
    ]
    table = ["| " + " | ".join(headers) + " |", "|---|---:|---:|---:|---:|---:|"]
    for model in MODEL_DIRS:
        values = []
        for group in GROUPS:
            value = counts[model][group]
            values.append(f"{value} ({100 * value / n:.2f}%)")
        display_model = f"**{model}**" if model == "CypherKD" else model
        table.append(f"| {display_model} | {n} | " + " | ".join(values) + " |")

    table_text = "\n".join(table)
    report = f"""# Preliminary rule-based CypherBench error taxonomy (Qwen, seed 42)

{table_text}

## Audit information

- A query is counted in a grouped category only when `execution_accuracy != 1` and a deterministic gold/prediction comparison detects that category.
- Categories are multi-label: one failing query may contribute to multiple columns.
- Percentages use the full test set (`n = {n}`) as denominator, matching the requested table format.
- The Teacher remains the upper bound; comparisons among student/KD systems should focus on SFT, CSD, DistiLLM, and CypherKD.
- Full case-level labels and evidence are saved in `{args.cases_output}`.
- Rows with `used_in_summary: true` are the exact cases contributing to the four grouped counts; unclassified execution failures are retained for audit but do not contribute.

| Method | EX failures | Classified failures | Unclassified failures |
|---|---:|---:|---:|
"""
    for model in MODEL_DIRS:
        report += (
            f"| {model} | {failing[model]} | {failing[model] - unclassified[model]} "
            f"| {unclassified[model]} |\n"
        )
    report += """

## Important limitation

These labels are produced by transparent deterministic rules, not by human annotation or an LLM judge. They are suitable for a reproducible first-pass analysis and case retrieval. Before using the counts as final paper numbers, manually audit a stratified sample from every model/category and report the annotation protocol.

The [original CypherBench paper](https://aclanthology.org/2025.acl-long.438/) developed this taxonomy through manual annotation and reports an error analysis on 50 randomly sampled incorrect predictions for each of two models. It does not establish a deterministic full-test labeling procedure. Therefore, this full-test table is an extension of the original protocol and should be described as such.
"""
    report_path = root / args.report_output
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8", newline="\n")

    print(f"Saved {len(cases)} failing model-query cases to {cases_path}")
    print(f"Saved report to {report_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--results", default="results/qwen/42")
    parser.add_argument("--benchmark", default="benchmarks/Cypherbench/test.json")
    parser.add_argument("--cases-output", default="rebuttal/error_taxonomy_cases_seed42.jsonl")
    parser.add_argument("--report-output", default="rebuttal/error_taxonomy_seed42.md")
    return parser.parse_args()


if __name__ == "__main__":
    analyze(parse_args())
