import json
from typing import List


def write_data(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as fp:
        json.dump(data, fp, indent=4, ensure_ascii=False)


def reload_data(json_path: str) -> List[dict]:
    """Reload the data from the file"""
    try:
        with open(json_path, "r") as fp:
            data = json.load(fp)
        return data
    except:
        return []
