TECH_SKILLS = [
    "python", "java", "c++", "c", "sql", "mysql",
    "html", "css", "javascript", "react",
    "node.js", "mongodb", "git", "github",
    "linux", "docker", "aws", "azure",
    "machine learning", "deep learning",
    "tensorflow", "opencv", "numpy",
    "pandas", "flask", "django",
    "cyber security", "networking"
]


import pdfplumber
from colorama import Fore, init
from skills import TECH_SKILLS

init(autoreset=True)


def extract_text(pdf):
    text = ""

    with pdfplumber.open(pdf) as file:
        for page in file.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted.lower() + "\n"

    return text


def find_skills(text):
    found = []

    for skill in TECH_SKILLS:
        if skill in text:
            found.append(skill)

    return found


def ats_score(found):
    return round((len(found) / len(TECH_SKILLS)) * 100)


def suggest(found):
    return [s for s in TECH_SKILLS if s not in found]


pdf = input("Enter Resume PDF Path: ")

try:

    resume = extract_text(pdf)

    detected = find_skills(resume)

    score = ats_score(detected)

    print(Fore.CYAN + "\n========= AI RESUME REPORT =========")

    print(Fore.GREEN + f"\nATS Score : {score}%")

    print(Fore.YELLOW + "\nDetected Skills:\n")

    for skill in detected:
        print("✔", skill.title())

    print(Fore.RED + "\nSuggested Skills:\n")

    for skill in suggest(detected)[:10]:
        print("➜", skill.title())

except FileNotFoundError:
    print("Resume file not found.")
