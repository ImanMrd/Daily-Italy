"""
Pipeline to extract vocabulary lists and exercises from 'Le prime 3000 parole - italy perte.pdf'
using PyMuPDF and RapidOCR on demand.
"""
import os
import re
import json
import pymupdf
from rapidocr_onnxruntime import RapidOCR

PDF_CANDIDATES = [
    "Resources/Le prime 3000 parole - italy perte.pdf",
    "Le prime 3000 parole - italy perte.pdf"
]
PDF_PATH = next((p for p in PDF_CANDIDATES if os.path.exists(p)), PDF_CANDIDATES[0])


def extract_page_text(page_number: int):
    doc = pymupdf.open(PDF_PATH)
    if page_number < 1 or page_number > len(doc):
        raise ValueError(f"Page number {page_number} out of range (1 - {len(doc)})")
    
    page = doc[page_number - 1]
    pix = page.get_pixmap(dpi=150)
    img_bytes = pix.tobytes("png")
    
    ocr = RapidOCR()
    result, _ = ocr(img_bytes)
    
    lines = []
    if result:
        for item in result:
            text = item[1].strip()
            if text:
                lines.append(text)
    return lines

def parse_word_list_page(page_number: int):
    """
    Parses a vocabulary page (e.g., pages 2 to 51) where words are formatted as:
    WORD Tag (e.g. ABITARE Va, ACQUA Nf, ALBERGO Nm, BELLO Agg)
    """
    raw_lines = extract_page_text(page_number)
    words = []
    
    # Common grammar tags in the book
    tag_pattern = re.compile(r'^(.*?)\s+(Va|Vr|Nm|Nf|Agg|Avv|Nm/Nf|Nm/Agg|Va/Ve|Ve)$', re.IGNORECASE)
    
    for line in raw_lines:
        line_clean = line.strip()
        # Skip headers / footers
        if "LE PRIME" in line_clean.upper() or "DA 1 A" in line_clean.upper() or "ITALY" in line_clean.upper():
            continue
        
        match = tag_pattern.match(line_clean)
        if match:
            lemma = match.group(1).strip().capitalize()
            tag = match.group(2).strip()
            words.append({"italian": lemma, "type": tag})
        elif len(line_clean) > 2 and line_clean.isalpha():
            words.append({"italian": line_clean.capitalize(), "type": ""})
            
    return words

if __name__ == "__main__":
    print("Testing OCR extraction on Page 2...")
    extracted = parse_word_list_page(2)
    print(f"Extracted {len(extracted)} words from Page 2. First 10:")
    for w in extracted[:10]:
        print(f" - {w['italian']} ({w['type']})")
