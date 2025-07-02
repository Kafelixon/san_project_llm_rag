# RAG Chat with Ollama

This Streamlit app allows you to upload documents (PDF, TXT, images), extract their content, create embeddings with Sentence Transformers, index them with FAISS, and chat with an Ollama language model augmented with your document context (RAG - Retrieval Augmented Generation).

---

## Prerequisites

* Python 3.8 or newer
* [Ollama](https://ollama.com/) running locally on port `11434`
* `tesseract` OCR installed (for image text extraction)
* Required Python packages installed (see below)

---

## Installation

1. Clone or download the repo with the Streamlit app code.

2. Create and activate a virtual environment (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

3. Install Python dependencies:

```bash
pip install streamlit sentence-transformers faiss-cpu Pillow tesserocr pymupdf requests
```

4. Make sure `tesseract` is installed on your system:

* On macOS with Homebrew:

```bash
brew install tesseract
```

* On Ubuntu/Debian:

```bash
sudo apt-get install tesseract-ocr
```

* On Windows, download the installer from [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)

---

## Running the app

Run the Streamlit app with:

```bash
streamlit run your_script_name.py
```

Replace `your_script_name.py` with the filename of your app.

---

## How to use

1. Upload your PDF, TXT, or image files (JPEG, PNG).

2. Wait for documents to be processed and indexed.

3. Enter your question in the chat input box.

4. The app will retrieve relevant document context and generate an answer via Ollama.

---

## Notes

* Ollama API should be running locally and accessible at `http://localhost:11434/api/generate`.

* The embedding model used is `all-MiniLM-L6-v2` from Sentence Transformers.

* The app currently processes PDFs as text and uses OCR only for images.

* Make sure your files are not too large to avoid memory issues.

