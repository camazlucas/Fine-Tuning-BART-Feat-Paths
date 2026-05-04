import re
import json
from collections import deque
from tqdm import tqdm

# -----------------------------
# 2. Extrair entidade da pergunta
# -----------------------------
def extract_entity(question):
    match = re.search(r"\[(.*?)\]", question)
    return match.group(1) if match else None

# -----------------------------
# 3. BFS para encontrar top paths mais curtos
# -----------------------------
def find_paths(graph, start, target, max_hops=3, top_k=3):
    queue = deque([(start, [])])
    paths = []

    while queue:
        node, path = queue.popleft()

        if len(path) >= max_hops:
            continue

        for relation, neighbor in graph.get(node, []):
            # evita ciclos no path atual (não global!)
            if any(neighbor == t for (_, _, t) in path):
                continue

            new_path = path + [(node, relation, neighbor)]

            if neighbor == target:
                paths.append(new_path)

                if len(paths) >= top_k:
                    return paths

                continue

            queue.append((neighbor, new_path))

    return paths

# -----------------------------
# 4. Formatar multiplos paths
# -----------------------------
def format_reasoning_path(path):
    tokens = []
    for h, r, t in path:
        tokens.append(h)
        tokens.append(r)
    tokens.append(path[-1][2])
    return " -> ".join(tokens)


# -----------------------------
# 5. Construir dataset final
# -----------------------------
def build_dataset_2(qa_file, graph, output_file, max_hops=3):
    data = []
    skipped = 0

    with open(qa_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in tqdm(lines):
        try:
            q, a = line.strip().split("\t")
        except:
            continue

        start = extract_entity(q)
        if start is None:
            skipped += 1
            continue

        target = a

        path = find_paths(graph, start, target, max_hops)

        if path is None:
            skipped += 1
            continue
        
        formatted_paths = [format_reasoning_path(p) for p in path]

        data.append({
            "input": q.replace(f"[{start}]", start),
            "paths": formatted_paths  # ← agora múltiplos
        })


    print(f"\nTotal exemplos: {len(lines)}")
    print(f"Usados: {len(data)}")
    print(f"Descartados: {skipped}")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)