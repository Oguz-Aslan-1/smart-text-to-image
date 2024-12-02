import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

# Configure Google Gemini API using Streamlit secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-pro-vision')

def analyze_menu_image(image):
    prompt = """
    Analyze this menu image and extract all food/drink items with their prices.
    Return the data as a JSON string with this format:
    {
        "items": [
            {"name": "item name", "price": "price"}
        ]
    }
    Only return the JSON string, no other text.
    """
    
    response = model.generate_content([prompt, image])
    try:
        # Extract JSON string from response and parse it
        json_str = response.text
        return json.loads(json_str)
    except json.JSONDecodeError:
        return {"items": []}

def main():
    st.title("Smart Menu Scanner")
    st.write("Take a photo of a menu to extract items and prices")
    
    # Camera input
    camera_input = st.camera_input("Take a photo of the menu")
    
    if camera_input is not None:
        image = Image.open(camera_input)
        
        if st.button('Analyze Menu'):
            with st.spinner('Analyzing menu items and prices...'):
                result = analyze_menu_image(image)
                
                st.subheader("Menu Items and Prices:")
                for item in result["items"]:
                    st.write(f"📍 {item['name']}: ${item['price']}")
                
                # Create downloadable JSON file
                json_str = json.dumps(result, indent=2)
                st.download_button(
                    label="Download as JSON",
                    data=json_str,
                    file_name="menu_items.json",
                    mime="application/json"
                )
                
                # Display data in a table format
                if result["items"]:
                    st.subheader("Menu Items Table")
                    st.table(result["items"])

if __name__ == '__main__':
    main()
