from datasets import load_dataset
from transformers import AutoTokenizer
from transformers import AutoModelForTokenClassification
from transformers import TrainingArguments, Trainer
from transformers import pipeline
model_name = "AventIQ-AI/Resume-Parsing-NER-AI-Model"
tokenizer = AutoTokenizer.from_pretrained("AventIQ-AI/Resume-Parsing-NER-AI-Model")
model = AutoModelForTokenClassification.from_pretrained("AventIQ-AI/Resume-Parsing-NER-AI-Model")

ner_pipe = pipeline("ner", model="./resume-ner-model", tokenizer="./resume-ner-model", aggregation_strategy="simple")

text = "John worked at Infosys as an Analyst. Email: john@email.com"
print(ner_pipe(text))

for entity in ner_results:
    print(f"{entity['word']} → {entity['entity_group']} ({entity['score']:.2f})")
label_list = [
    "O",           # 0
    "B-NAME",      # 1
    "I-NAME",      # 2
    "B-EMAIL",     # 3
    "I-EMAIL",     # 4
    "B-PHONE",     # 5
    "I-PHONE",     # 6
    "B-EDUCATION", # 7
    "I-EDUCATION", # 8
    "B-SKILL",     # 9
    "I-SKILL",     # 10
    "B-COMPANY",   # 11
    "I-COMPANY",   # 12
    "B-JOB",       # 13
    "I-JOB"        # 14
]
