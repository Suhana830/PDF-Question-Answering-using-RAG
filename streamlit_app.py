import streamlit as st
import os
from my_RAG import function_upload_pdf, function_get_response

st.set_page_config(page_title="PDF RAG APP", layout="centered")

st.title("📄 PDF Question Answering (RAG)")
st.write("Upload a PDF and ask questions using Retrieval-Augmented Generation.")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

#-----------pdf upload---------
st.header("Upload PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])


if uploaded_file is not None:
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("Indexing PDF........."):
        chunks = function_upload_pdf(file_path)
    
    st.success(f"✅ PDF indexed successfully ({chunks} chunks added)")

#---------ASK Question---------
st.header("Ask a Question")

query = st.text_input("Enter your question")

if st.button("Ask"):
    if not query:
        st.warning("Please enter a question")
    else:
        with st.spinner("Thinking...."):
            answer = function_get_response(query)
        st.subheader("Answer")
        st.write(answer)

