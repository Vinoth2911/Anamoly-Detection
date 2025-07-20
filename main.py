import streamlit as st
from inference_sdk import InferenceHTTPClient
from PIL import Image, ImageDraw
from auth import login_page, register_page, logout



# Handle Authentication
query_params = st.experimental_get_query_params()
current_page = query_params.get("page", ["login"])[0]
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
if not st.session_state.logged_in:
    if current_page == "register":
        register_page()
    else:
        login_page()
    st.stop()

# Logout button
st.sidebar.button("Logout", on_click=logout)

# Set background image function
def set_background(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set background for the main page
set_background("https://www.insight.veltris.com/wp-content/uploads/2022/12/Anomaly-detection-mobile-banner.png")

# Initialize the Inference Client
CLIENT = InferenceHTTPClient(
    api_url="https://classify.roboflow.com",
    api_key="AUriIUOQuEbHt8npqPyt"
)

# Streamlit UI
st.title("Abnormal Behaviour Detection")

# File Upload
uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Open image
    image = Image.open(uploaded_file)
    
    # Save image temporarily
    image_path = "temp_image.jpg"
    image.save(image_path)

    # Send image to Roboflow API
    result = CLIENT.infer(image_path, model_id="abnormal-behaviour/1")
    
    # Extract the detected class and confidence score
    detected_class = result['top']
    confidence = result['confidence']

    # Display the results
    st.image(image, caption=f"Detected: {detected_class} ({confidence * 100:.2f}%)", use_column_width=True)

    # Draw the confidence on the image
    draw = ImageDraw.Draw(image)
    text = f"{detected_class}: {confidence * 100:.2f}%"
    draw.text((10, 10), text, fill="red")

    # Show modified image
    st.image(image, caption="Detection Result", use_column_width=True)

