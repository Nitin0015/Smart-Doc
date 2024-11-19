import re
from text_extraction import extract_text_from_pdf
from text_summarization import summarize_long_text_cohere  
from qa_system import answer_question_with_cohere  


def preprocess_text(raw_text):
    """
    Clean and preprocess extracted text from any document type.
    """
    
    cleaned_text = re.sub(r'\s+', ' ', raw_text)  
    
    # Remove common document artifacts (e.g., "Page X of Y")
    cleaned_text = re.sub(r'Page \d+ of \d+', '', cleaned_text)  
    
    # Strip leading and trailing whitespace
    cleaned_text = cleaned_text.strip()
    
    # Remove extra artifacts specific to DOCX (if observed, customize as needed)
    cleaned_text = re.sub(r'\x0c', '', cleaned_text)  # Form feed characters
    return cleaned_text



def main():
    pdf_path = "data/sample.pdf"
    
    raw_text = extract_text_from_pdf(pdf_path)
    print("Raw Extracted Text:")
    print(raw_text)
    
    preprocessed_text = preprocess_text(raw_text)
    print("\nPreprocessed Text:")
    print(preprocessed_text)

    # Summarize the text using Cohere API
    print("\nGenerating Summary...")
    final_summary = summarize_long_text_cohere(preprocessed_text)  
    print("\nSummary:")
    print(final_summary)

    # Answer a question using the extracted text
    question = "Which companies dominate the premium smartphone market?"
    print(f"\nQuestion: {question}")
    answer = answer_question_with_cohere(preprocessed_text, question)  
    print("\nAnswer:")
    print(answer)


if __name__ == "__main__":
    main()
