import json

def compare_json(obj1, obj2, path=""):
    mismatches = {}

    if isinstance(obj1, dict) and isinstance(obj2, dict):
        all_keys = set(obj1.keys()).union(obj2.keys())
        for key in all_keys:
            new_path = f"{path}.{key}" if path else key
            if key not in obj1:
                mismatches[f"Field: {new_path}"] = f"Actual value: <missing> | Expected value: {obj2[key]}"
            elif key not in obj2:
                mismatches[f"Field: {new_path}"] = f"Actual value: {obj1[key]} | Expected value: <missing>"
            else:
                nested_diff = compare_json(obj1[key], obj2[key], new_path)
                mismatches.update(nested_diff)
    elif isinstance(obj1, list) and isinstance(obj2, list):
        for i, (item1, item2) in enumerate(zip(obj1, obj2)):
            nested_diff = compare_json(item1, item2, f"{path}[{i}]")
            mismatches.update(nested_diff)
        if len(obj1) != len(obj2):
            mismatches[f"Field: {path}"] = f"List length mismatch: Actual value: {len(obj1)} | Expected value: {len(obj2)}"
    else:
        if obj1 != obj2:
            mismatches[f"Field: {path}"] = f"Actual value: {obj1} | Expected value: {obj2}"

    return mismatches
