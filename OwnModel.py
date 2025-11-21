import kagglehub
import spacy
import pytesseract
from pypdf import PdfReader
from docx import Document
from PIL import Image
import re

# Try to load the spaCy model and provide a clear error message if it's missing
nlp = spacy.load("en_core_web_lg")
Files = kagglehub.dataset_download("snehaanbhawal/resume-dataset")
#for root, dirs, files in os.walk(Files):
    #for file in files:
def PdfExtract(path):
    Read = PdfReader(path)
    DocText = ""
    for page in Read.pages:
        DocText += page.extract_text()
    return DocText

def DocExtract(path):
    Read = Document(path)
    DocText = ""
    for paragraph in Read.paragraphs:
        DocText += paragraph.text
    return DocText

def ImgExtract(path):
    Img = Image.open(path)
    DocText = pytesseract.image_to_string(Img)
    return DocText

def Identify(path):
    if path.endswith(".pdf"):
            Text = PdfExtract(path)
    elif path.endswith(".docx"):
            Text = DocExtract(path)
    elif path.endswith((".png", ".jpg", ".gif")):
            Text = ImgExtract(path)
    return Text

def ExtractSkills(doc):
    skills = set()
    for chunk in doc.noun_chunks:
        text = chunk.text.lower().strip()
        if len(text) < 3:
            continue
        if text in ["experience", "project", "team", "work", "role", "job"]:
            continue
        if text.isalpha() or text.replace(" ", "").isalpha():
            skills.add(text)
    return skills

def ExtractEdu(doc):
    EduWord = set()
    DegreeIdentifier = r"\b(bachelor|masters|master|b\.?s\.?|m\.?s\.?|mba|phd|associate|diploma)\b"
    for ent in doc.ents:
        if ent.label_ == "ORG" and any(k in ent.text.lower() for k in ["university", "college", "institute", "school"]):
            EduWord.add(ent.text.lower())
    matches = re.findall(DegreeIdentifier, doc.text.lower())
    EduWord.update(matches)
    return EduWord

def ExtractExp(doc):
    ExpWord = set()
    ExpTime = r"(\d+)\s+(years?|yrs?|year)"
    JobTitle = r"(developer|engineer|manager|designer|analyst|intern|lead)"
    Time = re.findall(ExpTime, doc.text.lower())
    ExpWord.update([d[0] + " year(s)" for d in Time])
    for token in doc:
        if token.pos_ in ["PROPN", "NOUN"] and re.search(JobTitle, token.text.lower()):
            ExpWord.add(token.text.lower())
    for ent in doc.ents:
        if ent.label_ == "ORG" and all(k not in ent.text.lower() for k in ["university", "college", "institute", "school"]):
            ExpWord.add(ent.text.lower())
    return ExpWord


def Score(items):
    if not items:
        return 0
    num_items = len(items)
    import math
    score = math.log2(num_items + 1) / math.log2(21) * 100  
    score = min(score, 100)
    return int(score)


DocText = ""
DocText = Identify("C:/Users/kingd/Downloads/AI Resume Scanner/3547447.pdf")
DocumentBeta = nlp(DocText)

skills = ExtractSkills(DocumentBeta)
education = ExtractEdu(DocumentBeta)
experience = ExtractExp(DocumentBeta)

SkillScore = Score(skills)
EduScore = Score(education)
ExpScore = Score(experience)

FinalScore = int(
    (EduScore * 0.30) +
    (ExpScore * 0.40) +
    (SkillScore * 0.30)
)

print("Detected Skills:", skills)
print("Detected Education:", education)
print("Detected Experience:", experience)

print("Skills Score:", SkillScore)
print("Education Score:", EduScore)
print("Experience Score:", ExpScore)
print("Final Resume Score:", FinalScore)
