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
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
"""
st.header("Heading 1")
st.write(lorem_ipsum_text)

st.subheader("Sub-Heading 2")

st.text(lorem_ipsum_text)

file_path = "dokumentasi.pdf"

with open(file_path, "rb") as file:
    file_bytes = file.read()

st.sidebar.download_button(label="Download Documentation",
                           data=file_bytes,
                           file_name='dokumentasi.pdf',
                           mime="application/pdf"
                           )
