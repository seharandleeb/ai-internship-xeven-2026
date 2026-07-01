import pdfplumber
import time


def extract_with_pdfplumber(pdf_path):
    """
    Extract text from a PDF using pdfplumber.
    Returns extraction statistics.
    """

    start_time = time.perf_counter()

    extracted_text = ""

    with pdfplumber.open(pdf_path) as pdf:

        pages = len(pdf.pages)

        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                extracted_text += page_text

    end_time = time.perf_counter()

    return {
        "loader": "pdfplumber",
        "pages": pages,
        "characters": len(extracted_text),
        "words": len(extracted_text.split()),
        "time": round(end_time - start_time, 4),
        "text": extracted_text,
    }


if __name__ == "__main__":

    pdf_path = "SBP-Act.pdf"

    result = extract_with_pdfplumber(pdf_path)

    print("\n===== pdfplumber Results =====")
    print(f"Pages       : {result['pages']}")
    print(f"Characters  : {result['characters']}")
    print(f"Words       : {result['words']}")
    print(f"Time        : {result['time']} seconds")

    print("\nPreview:\n")
    print(result["text"][:500])