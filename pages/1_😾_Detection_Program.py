import streamlit as st
import env
import func
from PIL import Image
from pathlib import Path
import PIL

# Load icon for the application
# This section loads the application icon and sets up the initial configurations for the Streamlit app.
icon = Image.open("ptba-icon.png")
st.set_page_config(
    page_title="PTBA PPE Detection",  # Title displayed in the browser tab
    page_icon=icon,  # Icon for the browser tab
    layout="wide",  # Sets the layout to wide for better utilization of space
    initial_sidebar_state="expanded"  # Sidebar starts in expanded state
)

# Sidebar configuration
# Configure the sidebar to select the confidence threshold for detection.
st.sidebar.header("Confidence!")
confidence = float(st.sidebar.slider(
    "Pilih Nilai Confidence", 25, 100, 75)) / 100  # Convert slider value to a float (0.25 to 1.0)

# Load the detection model
# Loads the detection model from the specified path in the environment variables.
model_path = Path(env.DETECTION_MODEL)
model = func.load_model(model_path)

# Sidebar source selection
# Adds a checkbox and dropdown to select the input source for detection (RTSP, video, or webcam).
source = st.sidebar.checkbox("Show RTSP List", True)  # Checkbox to display the RTSP source list
if source:
    source_radio = st.sidebar.selectbox(
        "Pilih Source", env.SOURCES_LIST  # Dropdown for selecting the source type
    )

    if source_radio == env.RTSP:
        # If RTSP is selected, provide a text input for the RTSP link.
        rtsp_link = st.text_input("RTSP Link", "rtsp://example.com/stream")

        # Ensure all inputs are provided before calling the RTSP stream processing function.
        if rtsp_link:
            func.play_rtsp(rtsp_link, confidence, model)
    else:
        # Handle other source types: VIDEO and WEBCAM.
        if source_radio == env.VIDEO:
            func.play_video(confidence, model)  # Call the function to process video files
        elif source_radio == env.WEBCAM:
            func.play_webcam(confidence, model)  # Call the function to process webcam input
