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
# 3. BFS para encontrar path mais curto
# -----------------------------
def find_path(graph, start, target, max_hops=3):
    queue = deque([(start, [])])
    visited = set([start])

    while queue:
        node, path = queue.popleft()

        if len(path) >= max_hops:
            continue

        for relation, neighbor in graph.get(node, []):
            if neighbor in visited:
                continue

            new_path = path + [(node, relation, neighbor)]

            if neighbor == target:
                return new_path

            visited.add(neighbor)
            queue.append((neighbor, new_path))

    return None

# -----------------------------
# 4. Formatar path
# -----------------------------
def format_path(path):
    if path is None:
        return None

    tokens = []
    for h, r, t in path:
        tokens.append(h)
        tokens.append(r)

    tokens.append(path[-1][2])

    return " -> ".join(tokens)

# -----------------------------
# 5. Construir dataset final
# -----------------------------
def build_dataset_1(qa_file, graph, output_file, max_hops=3):
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

        path = find_path(graph, start, target, max_hops)


        if path is None:
            skipped += 1
            continue
        
        formatted = format_path(path)

        data.append({
            "input": q.replace(f"[{start}]", start),
            "output": formatted
        })


    print(f"\nTotal exemplos: {len(lines)}")
    print(f"Usados: {len(data)}")
    print(f"Descartados: {skipped}")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)