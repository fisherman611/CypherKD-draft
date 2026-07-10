import os
from pathlib import Path

from huggingface_hub import HfApi, create_repo


DEFAULT_REPO_ID = "distillation-sql/ablation_spans_cypherkd"
DEFAULT_REPO_TYPE = "model"
DEFAULT_RESULT_FOLDERS = (
    "results/qwen3/cypherkd_cypherkd_cypherkd_qwen3_0.6B_4B_wo_clause",
    "results/qwen3/cypherkd_cypherkd_cypherkd_qwen3_0.6B_4B_wo_node",
    "results/qwen3/cypherkd_cypherkd_cypherkd_qwen3_0.6B_4B_wo_expression",
)


def _split_env_list(value):
    if not value:
        return []
    return [item.strip() for item in value.replace(";", ",").split(",") if item.strip()]


def _resolve_result_folders(repo_root):
    configured = _split_env_list(os.getenv("HF_UPLOAD_FOLDERS"))
    folders = configured or list(DEFAULT_RESULT_FOLDERS)
    return [Path(path) if Path(path).is_absolute() else repo_root / path for path in folders]


def main():
    repo_root = Path(__file__).resolve().parent
    repo_id = os.getenv("HF_UPLOAD_REPO_ID", DEFAULT_REPO_ID)
    repo_type = os.getenv("HF_UPLOAD_REPO_TYPE", DEFAULT_REPO_TYPE)
    token = os.getenv("HF_TOKEN_UPLOAD") or os.getenv("HF_TOKEN")
    strict = os.getenv("HF_UPLOAD_STRICT", "1") != "0"

    api = HfApi(token=token)
    create_repo(repo_id=repo_id, repo_type=repo_type, token=token, exist_ok=True)

    folders = _resolve_result_folders(repo_root)
    missing = [folder for folder in folders if not folder.is_dir()]
    if missing and strict:
        missing_lines = "\n".join(f"  - {folder}" for folder in missing)
        raise FileNotFoundError(
            "Missing result folder(s) for Hugging Face upload:\n"
            f"{missing_lines}\n"
            "Run the ablation training first, or set HF_UPLOAD_STRICT=0 to skip missing folders."
        )

    for folder in folders:
        if not folder.is_dir():
            print(f"Skip missing folder: {folder}")
            continue

        path_in_repo = f"qwen3/{folder.name}"
        print(f"Uploading {folder} -> {repo_id}/{path_in_repo}")
        api.upload_folder(
            folder_path=str(folder),
            path_in_repo=path_in_repo,
            repo_id=repo_id,
            repo_type=repo_type,
            token=token,
        )

    print("Upload complete.")


if __name__ == "__main__":
    main()
