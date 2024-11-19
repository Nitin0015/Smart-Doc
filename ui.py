import re
import streamlit as st
from text_summarization import summarize_long_text_cohere
from qa_system import answer_question_with_cohere
from textblob import TextBlob
import plotly.graph_objects as go
from text_extraction import extract_text_from_pdf, extract_text_from_txt, extract_text_from_docx, extract_text_from_excel


def redact_sensitive_info(text):
    """Redact sensitive information from the text."""
    patterns = {
        "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
        "Bank Account": r"\b\d{8,12}\b",
        "Phone Number": r"\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b",
        "Credit Card": r"\b(?:\d{4}[ -]?){3}\d{4}\b",  
        "Email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    }

    for label, pattern in patterns.items():
        text = re.sub(pattern, f"[REDACTED {label}]", text)
    
    return text

def extract_text(file, file_extension):
    """Extract text based on the file type."""
    # Mapping file extensions to corresponding extraction functions
    extractors = {
        "pdf": extract_text_from_pdf,
        "txt": extract_text_from_txt,
        "docx": extract_text_from_docx,
        "xls": extract_text_from_excel,
        "xlsx": extract_text_from_excel

    }

    if file_extension not in extractors:
        raise ValueError(f"Unsupported file type: {file_extension}")

    
    return extractors[file_extension](file)

# Helper Functions
def preprocess_text(raw_text):
    """
    Clean, preprocess, and redact sensitive information from extracted text.
    """
    if not raw_text:
        raise ValueError("No text to preprocess.")
    
    # Remove multiple spaces and page numbers
    cleaned_text = re.sub(r'\s+', ' ', raw_text)
    cleaned_text = re.sub(r'Page \d+ of \d+', '', cleaned_text)
    
    # Redact sensitive information
    cleaned_text = redact_sensitive_info(cleaned_text)
    
    return cleaned_text.strip()



def analyze_sentiment(text):
    """Analyze sentiment and return polarity and tone."""
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.1:
        tone = "Positive"
    elif polarity < -0.1:
        tone = "Negative"
    else:
        tone = "Neutral"
    return polarity, tone

def filter_sensitive_responses(response):
    """
    Redact sensitive information from the generated answer.
    """
    return redact_sensitive_info(response)

def create_gauge(polarity, tone):
    """Create a smaller speedometer-like gauge."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=polarity,
        gauge={
            'axis': {'range': [-1, 1]},
            'bar': {'color': "black"},
            'steps': [
                {'range': [-1, -0.1], 'color': "red"},
                {'range': [-0.1, 0.1], 'color': "yellow"},
                {'range': [0.1, 1], 'color': "green"}
            ],
        },
        title={'text': f"Tone: {tone}"}
    ))

    
    fig.update_layout(
        width=280,  
        height=280,  
        margin=dict(t=10, b=10, l=10, r=10)  
    )

    return fig


st.markdown(
    """
    <style>
    body {
        background-color: #1c1e21; /* Dark background for a clean look */
        color: #e8e8e8; /* Light text for contrast */
    }
    .title {
        text-align: center; 
        font-size: 42px; 
        font-family: 'Arial', sans-serif; 
        color: #4CAF50; 
        margin-bottom: 20px;
    }
    .steps {
        font-size: 20px; 
        line-height: 1.8; 
        color: #e8e8e8; 
        font-family: 'Arial', sans-serif;
        margin-top: 20px;
        text-align: left;
    }
    .upload-section {
        text-align: center; 
        font-size: 20px; 
        margin-top: 30px; 
        padding: 20px;
        border: 2px dashed #4CAF50;
        border-radius: 10px;
        background-color: #2a2d31; /* Slightly lighter background for contrast */
        color: #ffffff;
        font-family: 'Arial', sans-serif;
        cursor: pointer;
    }
    .upload-section:hover {
        background-color: #333333;
        border-color: #FFDC5A; /* Golden yellow on hover */
    }
    .footer {
        text-align: center; 
        font-size: 14px; 
        margin-top: 50px; 
        color: #a9a9a9;
    }
    .highlight {
        color: #FFDC5A; /* Golden yellow for highlighting important elements */
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown('<div class="title">SmartQuest: Document Insights & Q&A</div>', unsafe_allow_html=True)


st.markdown(
    """
    <div class="steps">
    <strong>Steps to Use:</strong> <br><br>
    <span class="highlight">1.</span> Upload a document using the uploader below.<br>
    <span class="highlight">2.</span> View the extracted text or summary in the respective sections.<br>
    <span class="highlight">3.</span> Type a question to interact with the Q&A system.
    </div>
    """,
    unsafe_allow_html=True,
)


uploaded_file = st.file_uploader(
    label="",
    type=["pdf", "txt", "docx", "xls", "xlsx"],
    label_visibility="visible"
)


if "preprocessed_text" not in st.session_state:
    st.session_state["preprocessed_text"] = None

if "summary" not in st.session_state:
    st.session_state["summary"] = None

if "sentiment" not in st.session_state:
    st.session_state["sentiment"] = None

if "qa_history" not in st.session_state:
    st.session_state["qa_history"] = []

if "current_question" not in st.session_state:
    st.session_state["current_question"] = None

if "current_answer" not in st.session_state:
    st.session_state["current_answer"] = None

if uploaded_file is not None:
    file_extension = uploaded_file.name.split('.')[-1].lower()  #
    st.info(f"**Uploaded File:** {uploaded_file.name} ({uploaded_file.size} bytes)")

    if st.session_state["preprocessed_text"] is None:
        try:
            # Extract and preprocess text
            with st.spinner("🔍 Extracting text... Please wait."):
                raw_text = extract_text(uploaded_file, file_extension)  
                preprocessed_text = preprocess_text(raw_text)  # Apply preprocessing
                st.session_state["preprocessed_text"] = preprocessed_text
        except ValueError as e:
            st.error(f"Error: {e}")
        except Exception as e:
            st.error("Something went wrong while processing the file.")



    
    if st.session_state["preprocessed_text"]:
        with st.expander("📜 View Extracted Text"):
            st.write(st.session_state["preprocessed_text"])


    
    if st.session_state["sentiment"] is None:
        with st.spinner("🧠 Analyzing sentiment... Hang tight!"):
            try:
                if st.session_state["preprocessed_text"]:
                    polarity, tone = analyze_sentiment(st.session_state["preprocessed_text"])
                    st.session_state["sentiment"] = (polarity, tone)
                else:
                    raise ValueError("No valid text found to analyze.")
            except Exception as e:
                st.error(f"Sentiment analysis failed: {e}")
                st.session_state["sentiment"] = None



    st.subheader("🔍 Sentiment Analysis and Tone Detection")
    if st.session_state["sentiment"] is not None:
        polarity, tone = st.session_state["sentiment"]
        st.write(f"**Tone:** {tone}")

    
        fig = create_gauge(polarity, tone)
        st.plotly_chart(fig, use_container_width=True, key="sentiment_gauge")
    else:
        st.error("Sentiment analysis failed or not completed.")



    # Summarization Section
    if st.session_state["summary"] is None:
        with st.spinner("🧠 Summarizing... Hang tight!"):
            st.session_state["summary"] = summarize_long_text_cohere(st.session_state["preprocessed_text"])

    st.subheader("🔗 Summary")
    st.write(st.session_state["summary"])

# Question Answering Section
if st.session_state["preprocessed_text"]:
    st.subheader("❓ Ask a Question")
    question = st.text_input("Type your question below:")

    if question:
        st.session_state["current_question"] = question
        with st.spinner("🤔 Thinking..."):
            
            raw_answer = answer_question_with_cohere(st.session_state["preprocessed_text"], question)
        
           
            filtered_answer = filter_sensitive_responses(raw_answer)
        
            
            st.session_state["current_answer"] = filtered_answer
        
            
            st.session_state["qa_history"].append(
                (st.session_state["current_question"], st.session_state["current_answer"])
            )


    
    if st.session_state["current_question"] and st.session_state["current_answer"]:
        st.markdown(f"<strong>Q:</strong> {st.session_state['current_question']}", unsafe_allow_html=True)
        st.markdown(f"<strong>A:</strong> {st.session_state['current_answer']}", unsafe_allow_html=True)

    # Q&A History Section
    st.subheader("📚 Q&A History")
    if st.session_state["qa_history"]:
        for i, (q, a) in enumerate(st.session_state["qa_history"], 1):
            st.write(f"**Q{i}:** {q}")
            st.write(f"**A{i}:** {a}")
            st.markdown("---")
    else:
        st.write("No questions asked yet.")

    if st.button("Clear Q&A History"):
        st.session_state["qa_history"] = []
        st.session_state["current_question"] = None
        st.session_state["current_answer"] = None


st.markdown('<div class="footer">🚀 Built with ❤️ by Team Supernova</div>', unsafe_allow_html=True)
