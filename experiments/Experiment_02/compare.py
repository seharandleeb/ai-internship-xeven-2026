import fitz

from recursive_chunking import recursive_chunking
from token_chunking import token_chunking


def extract_text(pdf_path):
    document = fitz.open(pdf_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


if __name__ == "__main__":

    pdf_path = "SBP-Act.pdf"

    text = extract_text(pdf_path)

    recursive = recursive_chunking(text)
    token = token_chunking(text)

    print("\n========== Chunking Comparison ==========\n")

    print("Recursive Character Chunking")
    print("-" * 40)
    print(f"Number of Chunks      : {recursive['num_chunks']}")
    print(f"Average Characters    : {recursive['avg_characters']}")
    print(f"Average Tokens        : {recursive['avg_tokens']}")
    print(f"Execution Time        : {recursive['time']} sec")

    print()

    print("Token Chunking")
    print("-" * 40)
    print(f"Number of Chunks      : {token['num_chunks']}")
    print(f"Average Characters    : {token['avg_characters']}")
    print(f"Average Tokens        : {token['avg_tokens']}")
    print(f"Execution Time        : {token['time']} sec")