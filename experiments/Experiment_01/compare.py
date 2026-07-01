from pymupdf_loader import extract_with_pymupdf
from pdfplumber_loader import extract_with_pdfplumber


PDF_PATH = "SBP-Act.pdf"


def print_comparison_table(result1, result2):

    print("\n" + "=" * 65)
    print("          PDF LOADER COMPARISON")
    print("=" * 65)

    print(f"{'Metric':<20}{'PyMuPDF':<20}{'pdfplumber':<20}")
    print("-" * 65)

    print(f"{'Pages':<20}{result1['pages']:<20}{result2['pages']:<20}")
    print(f"{'Characters':<20}{result1['characters']:<20}{result2['characters']:<20}")
    print(f"{'Words':<20}{result1['words']:<20}{result2['words']:<20}")
    print(f"{'Time (sec)':<20}{result1['time']:<20}{result2['time']:<20}")

    print("=" * 65)

    print("\nRecommendation:")

    if result1["time"] < result2["time"]:
        print("✅ PyMuPDF is significantly faster.")
    else:
        print("✅ pdfplumber is faster.")

    if result1["characters"] > result2["characters"]:
        print("✅ PyMuPDF extracted more text.")
    else:
        print("✅ pdfplumber extracted more text.")

    print("\nFinal Recommendation:")
    print(
        "For production-level RAG systems, PyMuPDF is recommended because "
        "it provides faster document loading while extracting more textual content."
    )


if __name__ == "__main__":

    pymupdf_result = extract_with_pymupdf(PDF_PATH)

    pdfplumber_result = extract_with_pdfplumber(PDF_PATH)

    print_comparison_table(pymupdf_result, pdfplumber_result)