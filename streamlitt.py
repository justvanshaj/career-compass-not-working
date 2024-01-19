import streamlit as st
from PIL import Image
from google.generativeai import configure as genai_configure
from google.generativeai import GenerativeModel
from google.ai.generativelanguage import Content, Part, Blob
from dotenv import load_dotenv
import io

load_dotenv()
genai_configure(api_key="AIzaSyCPlu3JJT2sw3PCQFpKvs_LB-zxS_mnhqo")

def image_to_byte_array(image: Image) -> bytes:
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=image.format)
    return img_byte_arr.getvalue()

def generate_language_response(prompt, model):
    try:
        response = model.generate_content(prompt)
        st.write("")
        st.header(":blue[Response]")
        st.write("")
        st.markdown(response.text)
    except Exception as e:
        st.error(f"Error generating language response: {str(e)}")

def generate_vision_response(image_prompt, uploaded_file, model):
    if uploaded_file is not None:
        st.image(Image.open(uploaded_file), use_column_width=True)
        st.markdown("""<style>img { border-radius: 10px; }</style>""", unsafe_allow_html=True)

        if image_prompt != "":
            image = Image.open(uploaded_file)
            response = model.generate_content(Content(parts=[
                Part(text=image_prompt),
                Part(inline_data=Blob(mime_type="image/jpeg", data=image_to_byte_array(image)))
            ]))
            response.resolve()
            st.write("")
            st.write(":blue[Response]")
            st.write("")
            st.markdown(response.text)
        else:
            st.write("")
            st.header(":red[Please provide a prompt]")
    else:
        st.write("")
        st.header(":red[Please provide an image]")

def main():
    st.image("./Counsel.png", width=800)
    st.write("")

    gemini_pro, gemini_vision = st.tabs(["Counsel with Prompt", "Counsel with Image"])

    with gemini_pro:
        st.header("Chat with Bot")
        st.write("")
        prompt = st.text_input("Type your query to begin with counseling!!!", placeholder="Prompt", label_visibility="visible")
        model = GenerativeModel("Prompt Version")
        if st.button("Let me read and kickstart your career", use_container_width=True):
            generate_language_response(prompt, model)

    with gemini_vision:
        st.header("Interact with Bot")
        st.write("")
        image_prompt = st.text_input("Upload your query to begin with counseling!!!", placeholder="Prompt", label_visibility="visible")
        uploaded_file = st.file_uploader("Choose an image", accept_multiple_files=False, type=["png", "jpg", "jpeg", "img", "webp"])

        if st.button("Let me see and kickstart your career", use_container_width=True):
            model = GenerativeModel("gemini-pro-vision")
            generate_vision_response(image_prompt, uploaded_file, model)

if __name__ == "__main__":
    main()
