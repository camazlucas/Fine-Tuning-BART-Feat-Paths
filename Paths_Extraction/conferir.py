import json

# carregar arquivos
with open("Dataset/MetaQA/3-hop/vanilla/train_paths_3.json", "r", encoding="utf-8") as f:
    shortest = json.load(f)

with open("Dataset/MetaQA/3-hop/vanilla/train_paths_RoG3_clean.json", "r", encoding="utf-8") as f:
    multi = json.load(f)

# transformar em sets de perguntas
shortest_q = set(x["input"] for x in shortest)
multi_q = set(x["input"] for x in multi if x["paths"])

# diferenças
missing_in_multi = shortest_q - multi_q
extra_in_multi = multi_q - shortest_q

print(f"Total shortest: {len(shortest_q)}")
print(f"Total multi (com paths): {len(multi_q)}")
print(f"Missing in multi: {len(missing_in_multi)}")
print(f"Extra in multi: {len(extra_in_multi)}")