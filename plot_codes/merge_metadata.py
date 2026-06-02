from pathlib import Path
import json

input_dir = Path("../run/data/temp")
output_file = Path("../run/data/metadata_DUcore.json")

merged = {}

for file_path in input_dir.glob("metadata_*.json"):
    # Extract key from filename: metadata_{key}.json
    key = file_path.stem[len("metadata_"):]

    with open(file_path, "r", encoding="utf-8") as f:
        merged[key] = json.load(f)

# Write merged JSON
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(merged, f, indent=2, ensure_ascii=False)

print(f"Merged {len(merged)} files into {output_file}")