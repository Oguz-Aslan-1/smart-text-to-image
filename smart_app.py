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
    
    # Display raw response for debugging
    st.write("Raw AI Response:")
    st.write(response.text)
    
    try:
        json_str = response.text
        parsed_result = json.loads(json_str)
        st.write("Parsed JSON:")
        st.write(parsed_result)
        return parsed_result
    except json.JSONDecodeError:
        st.write("JSON Parsing Error - Raw Response:")
        st.write(json_str)
        return {"items": []}

def main():
    st.title("Smart Menu Scanner")
    st.write("Take a photo of a menu to extract items and prices")
    
    camera_input = st.camera_input("Take a photo of the menu")
    
    if camera_input is not None:
        image = Image.open(camera_input)
        
        if st.button('Analyze Menu'):
            with st.spinner('Analyzing menu items and prices...'):
                result = analyze_menu_image(image)
                
                # Create two columns for display
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Simple Text Format")
                    text_content = ""
                    for item in result["items"]:
                        text_content += f"{item['name']}: ${item['price']}\n"
                    st.text_area("Menu Items", value=text_content, height=300)
                    
                    st.download_button(
                        label="Download as Text",
                        data=text_content,
                        file_name="menu_items.txt",
                        mime="text/plain"
                    )
                
                with col2:
                    st.subheader("JSON Format")
                    json_str = json.dumps(result, indent=2)
                    st.text_area("JSON Data", value=json_str, height=300)
                    
                    st.download_button(
                        label="Download as JSON",
                        data=json_str,
                        file_name="menu_items.json",
                        mime="application/json"
                    )
                
                # Display data in a table format below the columns
                if result["items"]:
                    st.subheader("Menu Items Table")
                    st.table(result["items"])

if __name__ == '__main__':
    main()
