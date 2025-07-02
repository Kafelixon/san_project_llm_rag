import streamlit as st
from sentence_transformers import SentenceTransformer
import json
import faiss
import os
import tempfile
from pathlib import Path
import tesserocr
from PIL import Image
import requests

# CONFIG
MODEL_NAME = "llama3.2:1b"
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"


# Initialize once
@st.cache_resource
def load_embedder():
    return SentenceTransformer(EMBED_MODEL_NAME)


embedder = load_embedder()
index = faiss.IndexFlatL2(384)  # dim of MiniLM
documents = []

# Upload
st.title("📄 RAG Chat with Ollama")

uploaded_files = st.file_uploader(
    "Upload your PDFs, TXTs, or Images", accept_multiple_files=True
)


def extract_text_from_file(file):
    suffix = Path(file.name).suffix.lower()
    if suffix in [".txt"]:
        return file.read().decode()
    elif suffix in [".jpg", ".jpeg", ".png"]:
        # TODO: Fix tesseract
        img = Image.open(file)
        return tesserocr.image_to_text(img)
    elif suffix == ".pdf":
        # TODO: Fix situation with PDF as picture, maybe change to use OCRMYPDF
        try:
            import fitz  # PyMuPDF

            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(file.read())
                tmp_path = tmp.name
            doc = fitz.open(tmp_path)
            text = "\n".join([page.get_text() for page in doc])
            doc.close()
            os.remove(tmp_path)
            return text
        except:
            return "Failed to parse PDF."
    return ""


def get_ollama_response_stream(prompt):
    """
    Yields chunks of the response from Ollama API with streaming.
    """
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": MODEL_NAME, "prompt": prompt, "stream": True},
            stream=True,  # Ensure streaming is enabled
        )
        response.raise_for_status()  # Raise an exception for bad status codes

        if response.ok:
            for chunk in response.iter_lines():
                if chunk:
                    try:
                        json_chunk = json.loads(chunk.decode("utf-8"))
                        if "response" in json_chunk:
                            yield json_chunk["response"]
                        if json_chunk.get("done"):
                            break
                    except json.JSONDecodeError:
                        st.warning("Could not decode JSON chunk from Ollama.")
            else:
                st.error("Ollama failed to respond completely.")
        else:
            st.error(
                f"Ollama returned an error: {response.status_code} - {response.text}"
            )

    except requests.exceptions.RequestException as e:
        st.error(
            f"Failed to connect to Ollama. Please ensure it is running. Error: {e}"
        )
        yield ""  # Yield an empty string to ensure the generator completes
    except Exception as e:
        st.error(f"An unexpected error occurred during streaming: {e}")
        yield ""  # Yield an empty string to ensure the generator completes


if uploaded_files:
    for file in uploaded_files:
        text = extract_text_from_file(file)
        if text:
            docs = text.split("\n\n")
            embeddings = embedder.encode(docs)
            index.add(embeddings)
            documents.extend(docs)
    st.success("Documents processed and indexed!")

# Chat input
query = st.chat_input("Ask something based on your documents...")

if query and documents:
    with st.chat_message("user"):
        st.markdown(query)

    query_vec = embedder.encode([query])
    D, I = index.search(query_vec, k=5)
    context = "\n".join([documents[i] for i in I[0] if i < len(documents)])

    prompt = f"""You are a helpful assistant. Use the following context to answer the question.

Context:
{context}

Question: {query}
Answer:"""
    with st.chat_message("assistant"):
        st.write_stream(get_ollama_response_stream(prompt))


elif query:
    st.warning("Please upload and process documents first.")
