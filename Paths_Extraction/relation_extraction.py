import json

INPUT_PATH = "train_paths_RoG2_clean.json"
OUTPUT_PATH = "train_relation_paths.json"

def extract_relations(path_str):
    tokens = path_str.split(" -> ")
    relations = tokens[1::2]  # pega só as relações
    return " -> ".join(relations)

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

new_data = []

for item in data:
    relation_paths = []

    for path in item["paths"]:
        rel_path = extract_relations(path)
        relation_paths.append(rel_path)

    # 🔥 remove duplicados mantendo formato lista
    relation_paths = list(set(relation_paths))

    # 🔒 segurança: evita entradas vazias
    if not relation_paths:
        continue

    new_data.append({
        "input": item["input"],
        "paths": relation_paths
    })

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(new_data, f, indent=2, ensure_ascii=False)

print(f"Conversão concluída! Total: {len(new_data)} exemplos")