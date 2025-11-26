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

def get_section(text: str, heading: str) -> str:

    pattern = re.compile(
        rf"{heading}\s*(.*?)(?=\n[A-Z][A-Z &/]+?\s*$|\Z)",
        re.IGNORECASE | re.DOTALL | re.MULTILINE
    )
    match = pattern.search(text)
    return match.group(1) if match else ""

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

SKILL_WHITELIST = {
    # languages
    "c", "c++", "c/c++", "java", "python", "javascript", "js",
    "html", "html5", "css", "sml", "ruby", "perl", "php", "c#",
    "x86", "x86 assembly",

    # tools / tech
    "windows", "linux", "mysql", "opengl", "asp.net", "win32", "api/gui",
    "git", "django", "android", "latex",

    # concepts
    "data structures", "software design patterns",
}

GENERIC_WORDS = {
    "experience", "education", "projects", "activities", "links",
    "coursework", "objective", "position", "industry", "skills",
    "project", "team", "work", "role", "job"
}

def looks_like_tech(term: str) -> bool:
    """Heuristic to allow new skills not in the whitelist."""
    t = term.lower().strip()

    if not t or t in GENERIC_WORDS:
        return False

    # too long → probably a sentence, not a skill
    if len(t.split()) > 4:
        return False

    # only allow reasonable characters: letters, digits, +, #, ., -, /
    if not re.match(r"^[a-z0-9 +#.\-/]+$", t):
        return False

    # avoid very generic nouns
    GENERIC_PARTS = {"problems", "solutions", "email", "customers",
                     "foundation", "industry", "position", "mission"}
    if any(g in t for g in GENERIC_PARTS):
        return False

    return True

def ExtractSkills(doc):
    full_text = doc.text
    skills_text = get_section(full_text, "SKILLS")
    if not skills_text:
        skills_text = full_text  # fallback

    raw_items = re.split(r"[•\|\n,;/]+", skills_text)

    skills = set()

    for item in raw_items:
        line = item.strip(" -\t")
        if not line:
            continue

        # if there's a colon (e.g. "Coding: C/C++, Java"), use the right side
        if ":" in line:
            line = line.split(":", 1)[1].strip()

        tokens = re.split(r"\s+", line)
        buffer = []
        for tok in tokens:
            tok = tok.strip("()[]")
            if not tok:
                continue
            buffer.append(tok)

        joined = " ".join(buffer).lower()

        # 1) phrase-level check
        if joined in SKILL_WHITELIST or looks_like_tech(joined):
            skills.add(joined)

        # 2) token-level check (for things like "java", "c/c++")
        for tok in buffer:
            t = tok.lower().rstrip(".")
            if t in SKILL_WHITELIST or looks_like_tech(t):
                skills.add(t)

    return skills

def ExtractEdu(doc):
    EduWord = set()
    DegreeIdentifier = r"\b(bachelor(?:'s)?|master(?:'s)?|b\.?s\.?|bsc|m\.?s\.?|msc|mba|ph\.?d\.?|associate(?:'s)?|diploma)\b"
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
DocText = Identify("MayTrix2.pdf")
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
print("Final Resume Score:", Final
