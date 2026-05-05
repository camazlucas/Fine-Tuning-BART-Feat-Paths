from collections import defaultdict
from short_extraction import build_dataset_1
from multi_extraction import build_dataset_2

# -----------------------------
# 1. Carregar KG
# -----------------------------
def load_kg(path):
    graph = defaultdict(list)

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            h, r, t = line.strip().split("|")

            graph[h].append((r, t))
            graph[t].append((r + "_inv", h))  # aresta reversa

    return graph


# -----------------------------
# MAIN (execução)
# ----------------------------- 
if __name__ == "__main__":

    KG_PATH = "../Dataset/MetaQA/kb.txt"
    QA_PATH = "../Dataset/MetaQA/3-hop/vanilla/qa_dev.txt"
    OUTPUT_PATH = "../Dataset/MetaQA/3-hop/vanilla/valid_multi_paths_3.json"

    print("Carregando KG...")
    graph = load_kg(KG_PATH)

    print("Gerando dataset com paths...")
    # build_dataset_1(QA_PATH, graph, OUTPUT_PATH)
    build_dataset_2(QA_PATH, graph, OUTPUT_PATH)