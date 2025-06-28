import streamlit as st
from PIL import Image
import pytesseract

# Dummy chat function – replace with real LLM integration
def chat_with_llm(prompt):
    return f"LLM says: You said '{prompt}'"

st.title("📄 Chat with LLM + OCR Image Upload")

# Sidebar for uploading image
with st.sidebar:
    st.header("Upload a JPG Image")
    uploaded_file = st.file_uploader("Choose a .jpg image", type=["jpg", "webp", "jpeg", "png"])

    ocr_text = ""
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Perform OCR using pytesseract
        ocr_text = pytesseract.image_to_string(image)
        st.subheader("🧾 OCR Result:")
        st.text_area("Extracted Text", ocr_text, height=200)

# Main chat area
st.header("💬 Chat Interface")
chat_history = st.session_state.get("chat_history", [])

user_input = st.text_input("You:", key="user_input")

if st.button("Send") and user_input.strip():
    # Call LLM (dummy or real)
    response = chat_with_llm(user_input)
    chat_history.append(("You", user_input))
    chat_history.append(("LLM", response))
    st.session_state.chat_history = chat_history

if ocr_text:
    if st.button("Send OCR Text to LLM"):
        response = chat_with_llm(ocr_text)
        chat_history.append(("You (from OCR)", ocr_text))
        chat_history.append(("LLM", response))
        st.session_state.chat_history = chat_history

# Display chat
if chat_history:
    st.subheader("🗨️ Chat Log")
    for speaker, text in chat_history:
        st.markdown(f"**{speaker}:** {text}")
