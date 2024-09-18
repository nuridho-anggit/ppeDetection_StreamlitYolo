import streamlit as st
import env
import func
from PIL import Image
from pathlib import Path
import PIL

icon = Image.open("ptba-icon.png")
st.set_page_config(
    page_title="PTBA PPE Detection",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="expanded"
)
# st.title("Detection Page")
st.sidebar.header("Confidence!")

confidence = float(st.sidebar.slider(
    "Pilih Nilai Confidnce ", 25, 100, 75)) / 100

# st.sidebar.header("Input")
# source_radio = st.sidebar.radio(
#     "Pilih source", env.SOURCES_LIST)

model_path = Path(env.DETECTION_MODEL)

model = func.load_model(model_path)

# popover = st.popover("Filter Items")

add_source = st.sidebar.checkbox("Show Add RTSP", False)

if add_source:
    with st.sidebar.popover("Open "):
        st.markdown("Add")
        rtspLink = st.text_input("Insert RTSP Link")

source = st.sidebar.checkbox("Show RTSP List", True)
if source:
    # source_rtsp = st.sidebar.selectbox(
    #     "Pilih RTSP", env.RTSP_LIST
    # )

    # source_radio = st.sidebar.selectbox(
    #     "Pilih Source", env.SOURCES_LIST
    # )
    #
    # if source_rtsp == env.JEMBATAN:
    #     func.play_rtsp("rtsp://admin:Tarahan17@10.5.4.159:554/axis-media/media.amp", confidence, model)

    # ====================================================================================
    # rtsp_sources = func.fetch_rtsp()

    # rtsp_options = [source[2] for source in rtsp_sources]

    # source_rtsp = st.sidebar.selectbox(
    #     "Pilih RTSP", rtsp_options
    # )

    # selected_source = next((source for source in rtsp_sources if source[2] == source_rtsp),
    #                        None)

    # if selected_source:
    #     rtsp_url = selected_source[1]
    #     func.play_rtsp(rtsp_url, confidence, model)

    # ======================================================================================

    if source_radio == env.VIDEO:
        func.play_video(confidence, model)
    elif source_radio == env.WEBCAM:
        func.play_webcam(confidence, model)
    elif source_radio == env.RTSP:
        func.play_rtsp(confidence, model)

# if source_radio == env.VIDEO:
#     func.play_video(confidence, model)
# elif source_radio == env.WEBCAM:
#     func.play_webcam(confidence, model)
# elif source_radio == env.RTSP:
#     func.play_rtsp(confidence, model)
