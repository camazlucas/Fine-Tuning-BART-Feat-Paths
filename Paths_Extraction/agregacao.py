import json
import random

# =========================
# CONFIG
# =========================
FILE_1HOP = "../Dataset/MetaQA/1-hop/vanilla/train_multi_paths_1.json"
FILE_2HOP = "../Dataset/MetaQA/2-hop/vanilla/train_multi_paths_2.json"
FILE_3HOP = "../Dataset/MetaQA/3-hop/vanilla/train_multi_paths_3.json"

OUTPUT_FILE = "../Dataset/MetaQA/dataset_train_multi_paths.json"

N_HOP = 20000

SEED = 42

# =========================
# FUNÇÕES
# =========================
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def sample_data(data, n):
    if len(data) <= n:
        print(f"[WARN] dataset menor que {n}, usando tudo ({len(data)})")
        return data
    return random.sample(data, n)

# =========================
# MAIN
# =========================
def main():
    random.seed(SEED)

    print("Carregando datasets...")
    data_1hop = load_json(FILE_1HOP)
    data_2hop = load_json(FILE_2HOP)
    data_3hop = load_json(FILE_3HOP)

    print(f"1-hop total: {len(data_1hop)}")
    print(f"2-hop total: {len(data_2hop)}")
    print(f"3-hop total: {len(data_3hop)}")

    print("\nAmostrando...")
    sample_1hop = sample_data(data_1hop, N_HOP)
    sample_2hop = sample_data(data_2hop, N_HOP)

    print(f"1-hop usado: {len(sample_1hop)}")
    print(f"2-hop usado: {len(sample_2hop)}")
    print(f"3-hop usado: {len(data_3hop)}")

    print("\nAgregando...")
    final_data = sample_1hop + sample_2hop + data_3hop

    print("Embaralhando...")
    random.shuffle(final_data)

    print(f"\nTotal final: {len(final_data)}")

    print("Salvando...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

    print("✔ Dataset final gerado com sucesso!")


if __name__ == "__main__":
    main()