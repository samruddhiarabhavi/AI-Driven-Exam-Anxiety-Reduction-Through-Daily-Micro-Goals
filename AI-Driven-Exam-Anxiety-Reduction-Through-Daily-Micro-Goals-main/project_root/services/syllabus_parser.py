# services/syllabus_parser.py

from PIL import Image
import pytesseract
import PyPDF2
import os

def parse_syllabus_file(file_path):
    """
    Parse a syllabus file (txt, pdf, image) and return a list of topics.
    Each topic is a dict: {"subject": ..., "chapter": ..., "topic": ...}
    
    Supports:
    - Text files (.txt)
    - PDF files (.pdf)
    - Images (.png, .jpg, .jpeg)
    
    Returns up to 50 topics for safety.
    """

    topics = []

    def clean(line):
        """
        Remove unwanted characters and whitespace
        """
        return line.strip().replace("•", "").replace("-", "").replace("_", "")

    # ---------------- TEXT FILES ----------------
    if file_path.lower().endswith(".txt"):
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if len(line) > 5:  # skip very short lines
                    topics.append({
                        "subject": "General",
                        "chapter": "General",
                        "topic": clean(line)
                    })

    # ---------------- PDF FILES ----------------
    elif file_path.lower().endswith(".pdf"):
        if not os.path.exists(file_path):
            return []
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    for line in text.split("\n"):
                        line = line.strip()
                        if len(line) > 5:
                            topics.append({
                                "subject": "Syllabus",
                                "chapter": "General",
                                "topic": clean(line)
                            })

    # ---------------- IMAGE FILES ----------------
    elif file_path.lower().endswith((".png", ".jpg", ".jpeg")):
        if not os.path.exists(file_path):
            return []
        try:
            text = pytesseract.image_to_string(Image.open(file_path))
            for line in text.split("\n"):
                line = line.strip()
                if len(line) > 5:
                    topics.append({
                        "subject": "Image Syllabus",
                        "chapter": "General",
                        "topic": clean(line)
                    })
        except Exception as e:
            print(f"Error reading image file: {e}")
            return []

    # Limit topics to 50 to avoid overwhelming the timetable
    return topics[:50]
