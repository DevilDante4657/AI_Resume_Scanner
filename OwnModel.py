import kagglehub
import os
import spacy
from pathlib import Path
Files = kagglehub.dataset_download("snehaanbhawal/resume-dataset")
for root, dirs, files in os.walk(Files):
    for file in files:
        if file.endswith(".pdf"):
            print("pdf")
        elif file.endswith(".docx"):
            print("docx")
        elif file.endswith((".png", ".jpg", ".gif")):
            print("image")
