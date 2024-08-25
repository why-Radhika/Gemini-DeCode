from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Configure the Google Generative AI API with the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Streamlit app
st.set_page_config(page_title="GeminiDecode: Multilanguage Document Extraction by Gemini Pro")

st.header("GeminiDecode: Multilanguage Document Extraction by Gemini Pro")
text = ("Utilizing Gemini Pro AI, this project effortlessly extracts vital information "
        "from diverse multilingual documents, transcending language barriers with precision "
        "and efficiency for enhanced productivity and decision-making.")
styled_text = f"<span style='font-family:serif;'>{text}</span>"
st.markdown(styled_text, unsafe_allow_html=True)

# Function to load Google Gemini Pro Vision API and get a response
def get_gemini_response(input_text, image_parts, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, image_parts[0], prompt])
    return response.text

# Function to read the image and set the image format for Gemini Pro model input
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the file content into bytes
        image_bytes = uploaded_file.read()
        # Determine the MIME type
        mime_type = uploaded_file.type
        # Create the image parts dictionary
        image_parts = [{"mime_type": mime_type, "data": image_bytes}]
        return image_parts
    else:
        raise FileNotFoundError("An image file is required but not provided.")

# Get input from the user
input_prompt = st.text_input("Input Prompt:", key="input")
uploaded_file = st.file_uploader("Choose an image of the document:", type=["jpg", "jpeg", "png"])

# Display the uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Button to submit and analyze the document
submit = st.button("Tell me about the document")

# If submit button is clicked
if submit:
    try:
        # Setup the image input for the Gemini Pro model
        image_data = input_image_setup(uploaded_file)
        # Get response from Gemini Pro
        response = get_gemini_response(input_prompt, image_data, input_prompt)
        # Display the response
        st.subheader("The response is:")
        st.write(response)
    except FileNotFoundError as e:
        st.error(str(e))
