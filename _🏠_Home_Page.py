import streamlit as st
import cv2
import env
from streamlit_image_comparison import image_comparison
from PIL import Image

icon = Image.open("ptba-icon.png")
st.set_page_config(
    page_title="PTBA PPE Detection",
    page_icon=icon,
    # layout="wide",
    layout="centered",
    initial_sidebar_state="expanded",
)
st.title("Home Page - Panduan Menggunakan Program")
st.sidebar.header("Download!")

before_image = cv2.cvtColor(cv2.imread("before_img.jpg"), cv2.COLOR_BGR2GRAY)
after_image = cv2.cvtColor(cv2.imread("after_img.jpg"), cv2.COLOR_BGR2RGB)

image_comparison(
    img1=before_image,
    img2=after_image,
    label1="before Detection",
    label2="After Detection",
    width=700,
    starting_position=50,
    show_labels=True,
    make_responsive=True,
    in_memory=True,
)

lorem_ipsum_text = """
# Documentation

## Overview
This Streamlit application is designed for Personal Protective Equipment (PPE) detection using machine learning models. The application allows users to input RTSP streams, videos, or webcam feeds for real-time or batch analysis.

## Features
1. **Confidence Adjustment:** Users can set a confidence threshold for detection results via the sidebar slider.
2. **Source Selection:** Supports multiple input sources including:
   - RTSP streams
   - Uploaded videos
   - Webcam feeds
3. **Model Integration:** Leverages a pre-trained detection model to analyze input sources.

## Code Walkthrough

### Initialization
- The application icon and page configuration are set using Streamlit's `st.set_page_config`.
- A sidebar slider is used to adjust the detection confidence threshold.

### Model Loading
- The detection model is loaded from a specified path using the `func.load_model` function.

### Source Selection
- Users can toggle the display of the RTSP list.
- Depending on the source selected, the application processes:
  - **RTSP Stream:** Users can input an RTSP link for real-time analysis.
  - **Video:** Users can analyze a pre-recorded video.
  - **Webcam:** The application can access a connected webcam for live detection.

### Functions
- **`play_rtsp`:** Streams and analyzes RTSP feeds.
- **`play_video`:** Processes video files.
- **`play_webcam`:** Captures and analyzes webcam feeds.

## Dependencies
- `Streamlit`: For building the web application.
- `Pillow`: For image handling.
- Custom modules: `env` and `func` for configuration and utility functions.

## Usage
1. Launch the application.
2. Adjust the confidence threshold using the sidebar slider.
3. Select the desired source (RTSP, video, or webcam).
4. Provide the necessary inputs (e.g., RTSP link).
5. View detection results in real-time or as output images.

## Notes
- Ensure the environment (`env`) and utility (`func`) modules are correctly configured.
- The detection model file must be available at the specified path.

## Future Enhancements
- Add support for uploading custom models.
- Implement advanced analytics and visualization for detection results.
- Improve UI/UX for a more user-friendly experience.
"""
# st.header("Heading 1")
st.write(lorem_ipsum_text)

# st.subheader("Sub-Heading 2")
#
# st.text(lorem_ipsum_text)

file_path = "dokumentasi.pdf"

with open(file_path, "rb") as file:
    file_bytes = file.read()

st.sidebar.download_button(label="Download Documentation",
                           data=file_bytes,
                           file_name='dokumentasi.pdf',
                           mime="application/pdf"
                           )
