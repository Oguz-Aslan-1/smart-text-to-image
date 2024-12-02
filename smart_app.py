import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

# Configure Google Gemini API using Streamlit secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel(model_name='gemini-1.5-flash')

def analyze_menu_image(image):
    prompt = """
    You are a menu analyzer. Look at this menu image carefully and extract:
    1. All food and drink items
    2. Their corresponding prices
    Format your response as a JSON with this exact structure:
    {
        "items": [
            {"name": "item name", "price": "price value"}
        ]
    }
    Be precise and include every visible menu item.
    """

    response = model.generate_content([prompt, image])
    
    # Display response 
    st.write(response.text)
    
    # Add download button
    st.download_button(
        label="Download Results",
        data=response.text,
        file_name="menu_items.txt",
        mime="text/plain"
    )

def main():
    st.title("Smart Menu Scanner")
    st.write("Take a photo of a menu to extract items and prices")

    camera_input = st.camera_input("Take a photo of the menu")

    if camera_input is not None:
        image = Image.open(camera_input)

        if st.button('Analyze Menu'):
            with st.spinner('Analyzing menu items and prices...'):
                result = analyze_menu_image(image)

if __name__ == '__main__':
    main()
