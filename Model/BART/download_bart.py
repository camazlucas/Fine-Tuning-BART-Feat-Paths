from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "facebook/bart-base"

print("Baixando tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name)

print("Baixando modelo...")
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

print("Download concluído!")