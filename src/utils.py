import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PROMPT_DIR = PROJECT_ROOT / "prompts" / "generator"

DEFAULT_SYSTEM_PROMPT = """You are a Cypher Query Generator.

Your task is to generate a valid Cypher query that answers the user's natural language question using only the provided graph schema.

Rules:
- Use only labels, relationships, and properties that exist in the schema.
- Do not invent any schema elements.
- Return only the fields needed to answer the question.
- If duplicates are possible, use DISTINCT when appropriate.
- If the question requires aggregation, sorting, or limiting, use the correct Cypher clauses.
- Ensure the query is syntactically valid.

Output format:
{
  "cypher": "The complete Cypher query"
}

Return only the JSON object and nothing else."""

DEFAULT_USER_PROMPT = """QUESTION:
{question}

SCHEMA:
{schema}

Generate a Cypher query that answers the question using only the provided schema.
Return only the JSON object in the required format."""


def read_json_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"File {filepath} không tồn tại.")
        return None
    except json.JSONDecodeError:
        print(f"File {filepath} không phải JSON hợp lệ.")
        return None


def _read_text_file(filepath, default):
    path = Path(filepath)
    try:
        return path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return default


def build_messages(question, schema):
    """Build chat messages for Text-to-Cypher generation."""
    system_prompt = _read_text_file(
        GENERATOR_PROMPT_DIR / "system_prompt.txt",
        DEFAULT_SYSTEM_PROMPT,
    )
    user_prompt_template = _read_text_file(
        GENERATOR_PROMPT_DIR / "user_prompt.txt",
        DEFAULT_USER_PROMPT,
    )
    user_prompt = user_prompt_template.format(
        question=question or "",
        schema=schema or "",
    )
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
