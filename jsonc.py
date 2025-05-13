import json

def compare_json(obj1, obj2, path=""):
    mismatches = []

    if isinstance(obj1, dict) and isinstance(obj2, dict):
        all_keys = set(obj1.keys()).union(obj2.keys())
        for key in all_keys:
            new_path = f"{path}.{key}" if path else key
            if key not in obj1:
                mismatches.append(f"Missing in first: {new_path}")
            elif key not in obj2:
                mismatches.append(f"Missing in second: {new_path}")
            else:
                mismatches.extend(compare_json(obj1[key], obj2[key], new_path))
    elif isinstance(obj1, list) and isinstance(obj2, list):
        for i, (item1, item2) in enumerate(zip(obj1, obj2)):
            mismatches.extend(compare_json(item1, item2, f"{path}[{i}]"))
        if len(obj1) != len(obj2):
            mismatches.append(f"List length mismatch at {path}: {len(obj1)} != {len(obj2)}")
    else:
        if obj1 != obj2:
            mismatches.append(f"Value mismatch at {path}: {obj1} != {obj2}")

    return mismatches

# Load the JSON files
with open("file1.json") as f1, open("file2.json") as f2:
    json1 = json.load(f1)
    json2 = json.load(f2)

# Compare
diffs = compare_json(json1, json2)

# Show differences
if diffs:
    print("Mismatches found:")
    for diff in diffs:
        print("-", diff)
else:
    print("JSONs are identical.")
