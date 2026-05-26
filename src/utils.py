import json


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
