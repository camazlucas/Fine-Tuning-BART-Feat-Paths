import json

INPUT_PATH = "Dataset/MetaQA/3-hop/vanilla/train_paths_RoG3.json"
OUTPUT_PATH = "Dataset/MetaQA/3-hop/vanilla/train_paths_RoG3_clean.json"

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# filtra apenas exemplos com paths não vazios
clean_data = [x for x in data if x.get("paths")]

print(f"Original: {len(data)}")
print(f"Após limpeza: {len(clean_data)}")
print(f"Removidos: {len(data) - len(clean_data)}")

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(clean_data, f, indent=2, ensure_ascii=False)