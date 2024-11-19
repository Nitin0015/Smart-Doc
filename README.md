# SmartQuest: Document Insights & Q&A

SmartQuest is an intelligent document analysis and question-answering system that allows users to extract insights, summarize content, and interact with their documents through natural language queries.

## Features

- Document upload support for PDF, TXT, DOCX, XLS, and XLSX files
- Automatic text extraction from uploaded documents
- Text summarization using Cohere API
- Sentiment analysis and tone detection
- Question-answering system powered by Cohere API
- Automatic redaction of sensitive information

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/smartquest.git
cd smartquest

```
2.Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
3.Install the required dependencies:
```bash
pip install -r requirements.txt
```
4. Set up your Cohere API key::

- Create a .env file in the project root
- Add your Cohere API key: API_SECRET_KEY=your_api_key_here

## Usage
1. Run the Streamlit app:
```bash
streamlit run ui.py
```
2. Open your web browser and navigate to the URL provided by Streamlit (usually http://localhost:8501)

3. Use the application:
- Upload a document using the file uploader
- View the extracted text and summary
- Analyze the document's sentiment
- Ask questions about the document content

4.For command-line testing of core functionalities:
```bash
python app.py
```

## Project Structure
- ui.py: Main Streamlit user interface
- text_summarization.py: Text summarization using Cohere API
- text_extraction.py: Functions for extracting text from various file formats
- qa_system.py: Question-answering system using Cohere API
- app.py: Command-line interface for testing core functionalities
- requirements.txt: List of project dependencies

## Dependencies
Key dependencies include:
- streamlit
- cohere
- PyMuPDF (fitz)
- python-docx
- pandas
- numpy
- plotly
- textblob

For a complete list of dependencies and their versions, refer to the requirements.txt file.

