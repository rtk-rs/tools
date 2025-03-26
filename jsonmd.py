import sys
import json
from typing import Any, List

def flatten_json(data: Any, parent_key: str = "", level: int = 0) -> List[List[str]]:
    rows = []
    if isinstance(data, dict):
        for key, value in data.items():
            new_key = f"{parent_key}.{key}" if parent_key else key
            if isinstance(value, dict) and level < 2:
                sub_table = json_to_markdown(value, nested=True)
                rows.append([new_key, f"\n{sub_table}"])
            elif isinstance(value, list) and level < 2:
                rows.append([new_key, ""])  # Ajoute un titre de section
                for i, item in enumerate(value):
                    rows.extend(flatten_json(item, f"{new_key}[{i}]", level + 1))
            else:
                rows.append([new_key, str(value)])
    elif isinstance(data, list):
        for i, item in enumerate(data):
            rows.extend(flatten_json(item, f"{parent_key}[{i}]", level))
    else:
        rows.append([parent_key, str(data)])
    return rows

def json_to_markdown(json_data: Any, nested: bool = False) -> str:
    rows = flatten_json(json_data)
    markdown_table = "| Field | Value |\n| --- | --- |\n"
    for key, value in rows:
        markdown_table += f"| {key} | {value} |\n"
   
    if nested:
        return markdown_table.strip()

    return markdown_table

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as fd:
        content = fd.read()
        json_data = json.loads(content)
        markdown_output = json_to_markdown(json_data)
        print(markdown_output)
