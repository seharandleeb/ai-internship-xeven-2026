import fitz
import time


def extract_with_pymupdf(pdf_path):
    start_time = time.perf_counter()

    document = fitz.open(pdf_path)
    extracted_text = ""

    for page in document:
        extracted_text += page.get_text()

    end_time = time.perf_counter()

    result = {
        "loader": "PyMuPDF",
        "pages": len(document),
        "characters": len(extracted_text),
        "words": len(extracted_text.split()),
        "time": round(end_time - start_time, 4),
        "text": extracted_text,
    }

    document.close()

    return result


if __name__ == "__main__":

    pdf_path = "SBP-Act.pdf"

    result = extract_with_pymupdf(pdf_path)

    print("\n===== PyMuPDF Results =====")
    print(f"Pages       : {result['pages']}")
    print(f"Characters  : {result['characters']}")
    print(f"Words       : {result['words']}")
    print(f"Time        : {result['time']} seconds")

    print("\nPreview:\n")
    print(result["text"][:500])