from PIL import Image
import pytesseract
import PyPDF2


def parse_syllabus_file(file_path):
    topics = []

    def clean(line):
        return line.strip().replace("•", "").replace("-", "")

    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if len(line.strip()) > 5:
                    topics.append({
                        "subject": "General",
                        "topic": clean(line)
                    })

    elif file_path.endswith(".pdf"):
        reader = PyPDF2.PdfReader(open(file_path, "rb"))
        for page in reader.pages:
            text = page.extract_text()
            if text:
                for line in text.split("\n"):
                    if len(line.strip()) > 5:
                        topics.append({
                            "subject": "Syllabus",
                            "topic": clean(line)
                        })

    elif file_path.endswith((".png", ".jpg", ".jpeg")):
        text = pytesseract.image_to_string(Image.open(file_path))
        for line in text.split("\n"):
            if len(line.strip()) > 5:
                topics.append({
                    "subject": "Image Syllabus",
                    "topic": clean(line)
                })

    return topics[:15]  # limit for safety
