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
        rf"^{heading}\s*(.*?)(?=\n[A-Z][A-Z &/]+?\s*$|\Z)",
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

    "python", "java", "javascript","typescript","c", "c++",
    "c#", "go", "rust", "swift", "kotlin", "ruby", "php", "scala", "haskell", "dart", "objective-c", "r",
    "assembly",  "x86 assembly",  "arm assembly", "verilog", "vhdl", "matlab", "fortran"

    "windows", "linux", "mysql", "opengl", "asp.net", "win32", "api/gui",
    "git", "django", "android", "latex", "springboot"
    "data structures", "software design patterns",

    "assembly", "x86 assembly", "arm assembly", "verilog", "vhdl",
    "matlab", "fortran",

    "sql", "mysql", "postgresql", "sqlite", "mongodb", "redis",
    "cassandra", "graphql", "dynamodb",

    "pytorch", "tensorflow", "numpy", "pandas", "scikit-learn",
    "matplotlib", "keras", "jupyter",
   #cloud
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
    "jenkins", "linux", "bash", "powershell",
    "android", "android studio", "xcode", "react native", "flutter",
}

GENERIC_WORDS = {
    "experience", "education", "projects", "activities", "links",
    "coursework", "objective", "skills", "languages", "tools",
    "frameworks", "technologies", "environment", "programming",
    "scripting"
}
STOPWORDS = {
    "and", "or", "in", "on", "at", "for", "to", "from", "of", "the", "a", "an",
    "with", "through", "using", "use", "used",
    "have", "has", "had", "been", "be", "is", "are", "was", "were",
    "as", "by", "that", "this", "these", "those",
    "skills", "skill", "experience", "experiences", "understanding",
    "knowledge", "ability", "abilities",
    "basic", "advanced", "intermediate",
    "programming", "scripting", "development", "developer",
    "front", "back", "end",
    "on", "into", "over", "under", "between", "across", "along", "within",
    "without", "about", "per", "via",
    "have", "been", "developed", "develop", "developing"
}

SKILL_HEADERS = [
    "SKILLS",
    "TECHNICAL SKILLS",
    "TECHNICAL SKILLS & TOOLS",
    "PROGRAMMING LANGUAGES",
    "PROFICIENCIES",
    "TECHNOLOGIES",
    "TOOLS"
]
# term causing errors in model
def Generic_T(term: str) -> bool:
    t = term.lower().strip()

    if not t or t in GENERIC_WORDS:
        return False

    if len(t.split()) > 3:
        return False

    if not re.match(r"^[a-z0-9 +#.\-/]+$", t):
        return False

    GENERIC_PARTS = {"problems", "solutions", "customers",
                     "foundation", "industry", "position", "mission"}

    if any(g in t for g in GENERIC_PARTS):
        return False

    return True

def ExtractSkills(doc):
    full_text = doc.text.lower()
    skills = set()

    # ------------------------------
    # 1) Try to get SKILLS section
    # ------------------------------
    skills_text = ""
    for h in SKILL_HEADERS:
        section = get_section(doc.text, h)
        if section:
            skills_text = section
            break

    if skills_text:
        raw_items = re.split(r"[•\|\n,;/]+", skills_text)

        for item in raw_items:
            line = item.strip(" -\t").lower()
            if not line:
                continue

            # remove "Programming Languages:" etc
            if ":" in line:
                line = line.split(":", 1)[1].strip()

            # split on whitespace to isolate tokens
            tokens = [t.strip("()[]") for t in line.split() if t.strip("()[]")]

            # join for multi-word tech phrases
            joined = " ".join(tokens)

            # strict checks
            if joined in SKILL_WHITELIST:
                skills.add(joined)

            for tok in tokens:
                if tok in SKILL_WHITELIST:
                    skills.add(tok)

        return skills

    text = full_text

    for skill in SKILL_WHITELIST:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text):
            skills.add(skill.lower())


    CONTEXT = [
        "programming", "language", "develop", "built", "coded",
        "software", "technical", "implementation"
    ]

    words = set(re.findall(r"[a-zA-Z0-9+#.-]+", text))

    for w in words:
        if Generic_T(w):
            # must appear near tech context to count
            context_pattern = rf"{w}.{{0,20}}({'|'.join(CONTEXT)})|" \
                              rf"({'|'.join(CONTEXT)}).{{0,20}}{w}"
            if re.search(context_pattern, text):
                skills.add(w)

    return skills




def ExtractEducation(doc):
    # Accept spaCy Doc or raw text
    if hasattr(doc, "text"):
        text = doc.text
    else:
        text = str(doc)

    # 1) Focus on the EDUCATION section if present
    edu_section = get_section(text, "EDUCATION")
    if not edu_section:
        # fallback: use whole doc (last resort)
        edu_section = text

    lines = [ln.strip() for ln in edu_section.splitlines() if ln.strip()]

    SCHOOL_KEYWORDS = ("university", "college", "institute", "school")
    DEGREE_PATTERN = re.compile(
        r"(bachelor|master|associate|ph\.?d|phd|mba)[^,\n]*",
        re.IGNORECASE
    )

    schools = set()
    degrees = set()

    for line in lines:
        lower = line.lower()

        # --------- SCHOOLS ---------
        if any(k in lower for k in SCHOOL_KEYWORDS):
            cleaned = lower

            # remove any month/year blobs on that line
            cleaned = re.sub(
                r"(spring|summer|fall|winter)\s+\d{4}.*", "", cleaned
            )
            cleaned = re.sub(
                r"(january|february|march|april|may|june|july|august|"
                r"september|october|november|december)\s+\d{4}.*",
                "",
                cleaned,
            )
            # ALSO just strip season words themselves in case year is on another line
            cleaned = re.sub(r"\b(spring|summer|fall|winter)\b", "", cleaned)

            cleaned = re.sub(r"\s{2,}", " ", cleaned)
            cleaned = cleaned.strip(" ,;-")
            if cleaned:
                schools.add(cleaned)

        # --------- DEGREES ---------
        m = DEGREE_PATTERN.search(lower)
        if m:
            degree_line = lower

            # Strip trailing locations like "towson, md"
            degree_line = re.sub(r",\s*[a-z .]+,\s*[a-z]{2}\s*$", "", degree_line)

            degree_line = re.sub(r"\s{2,}", " ", degree_line)
            degree_line = degree_line.strip(" ,;-")
            if degree_line:
                degrees.add(degree_line)

    EduWord = schools.union(degrees)
    return EduWord

def ExtractExperience(doc):
    full_text = doc.text
    ExpWord = set()

    # 1) Restrict to likely experience sections
    POSSIBLE_EXP_HEADINGS = [
        "EXPERIENCE",
        "RELEVANT EXPERIENCE",
        "WORK EXPERIENCE",
        "PROFESSIONAL EXPERIENCE",
        "INDUSTRY EXPERIENCE",
        "RESEARCH EXPERIENCE"
    ]

    exp_blocks = []
    for heading in POSSIBLE_EXP_HEADINGS:
        section = get_section(full_text, heading)
        if section:
            exp_blocks.append(section)

    if exp_blocks:
        exp_text = "\n".join(exp_blocks)
    else:
        # If no explicit experience heading, fall back to full doc (last resort)
        exp_text = full_text

    lines = [ln.strip() for ln in exp_text.splitlines()]
    current_company = None

    for line in lines:
        if not line:
            continue

        # Ignore pure bullet lines – they just describe duties
        if line.lstrip().startswith("•"):
            continue

        # Company line heuristic:
        #   e.g. "IBM- Minneapolis, Minnesota"
        #   e.g. "NDSU IT- Fargo, North Dakota"
        if "-" in line and "--" not in line:
            company = line.split("-", 1)[0].strip(" •–—\t")
            if company:
                ExpWord.add(company)
                current_company = company
            continue

        # Role line heuristic:
        #   e.g. "Software Engineering Intern -- May 20XX-August 20XX"
        if "--" in line:
            title_part = line.split("--", 1)[0].strip(" •–—\t")
            if title_part:
                ExpWord.add(title_part)
                if current_company:
                    ExpWord.add(f"{title_part} @ {current_company}")
            continue

    # Optional: if we got absolutely nothing, fall back to your old spaCy-based logic
    if not ExpWord:
        exp_doc = nlp(exp_text)

        # simple backup: any ORG + "intern"/"engineer" words
        for ent in exp_doc.ents:
            if ent.label_ == "ORG":
                ExpWord.add(ent.text.strip())

        for token in exp_doc:
            t = token.text.lower()
            if t in {"intern", "engineer", "developer"}:
                ExpWord.add(token.text.strip())

    skip_exp = set()
    for item in ExpWord:
        lower = item.lower()
        # Skip if it is a skill
        if lower in SKILL_WHITELIST:
            continue
        # Skip basic tech words
        if lower in {"css", "html", "api", "ui", "python", "java", "javascript"}:
            continue
        # Skip IDEs unless you want them as experience
        if lower in {"android studio", "visual studio", "xcode"}:
            continue

        skip_exp.add(item)

    return skip_exp

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
DocText = Identify("Victoria-computer-engineering.pdf")
DocumentBeta = nlp(DocText)


skills = ExtractSkills(DocumentBeta)
education = ExtractEducation(DocumentBeta)
experience = ExtractExperience(DocumentBeta)

SkillScore = Score(skills)
EduScore = Score(education)
ExpScore = Score(experience)

FinalScore = int(
    (EduScore * 0.30) +
    (ExpScore * 0.40) +
    (SkillScore * 0.30))

print("Detected Skills:", skills)
print("Detected Education:", education)
print("Detected Experience:", experience)

print("Skills Score:", SkillScore)
print("Education Score:", EduScore)
print("Experience Score:", ExpScore)
print("Final Resume Score:", FinalScore)
