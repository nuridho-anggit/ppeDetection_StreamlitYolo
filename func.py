import pandas as pd
from ultralytics import YOLO
import time
from time import gmtime, strftime
import streamlit as st
import cv2
import tempfile
import os
import env
from pathlib import Path
from pyecharts import options as opts
from pyecharts.charts import Pie
from streamlit_echarts import st_pyecharts
import pymysql
from sqlalchemy import create_engine, text
import torch

# Load YOLO model from a given path
def load_model(model_path):
    """
    Load the YOLO model from the specified file path.

    Args:
        model_path (str): Path to the YOLO model file.

    Returns:
        YOLO: The loaded YOLO model.
    """
    model = YOLO(model_path)
    return model

# Save cropped image of detected person with violation
def save_person(image, person_box, label):
    """
    Save the cropped image of a detected person based on their bounding box and label.

    Args:
        image (numpy.ndarray): Original image containing the detected person.
        person_box (tuple): Coordinates of the bounding box (x1, y1, x2, y2).
        label (str): Violation label ('no-helmet' or 'no-vest').
    """
    x1, y1, x2, y2 = map(int, person_box)
    cropped_image = image[y1:y2, x1:x2]

    base_directory = None

    # Determine the directory based on the violation type
    if label == 'no-helmet':
        base_directory = Path(env.VIOLATION_HARDHAT_DIR)
        new_label = "vioHardHat_"
    elif label == 'no-vest':
        base_directory = Path(env.VIOLATION_SAFETY_VEST_DIR)
        new_label = "vioSafetyVest_"

    if base_directory is not None:
        # Create directory structure based on the current date
        date_directory = base_directory / strftime("%Y%m%d", gmtime())
        if not date_directory.exists():
            date_directory.mkdir(parents=True, exist_ok=True)

        # Save the cropped image with a timestamped filename
        filename = date_directory / f'{new_label}{strftime("%y%m%d_%H%M%S", gmtime())}.jpg'
        cv2.imwrite(str(filename), cropped_image)
    else:
        print("Error to save")

# Display detected objects on an image
def display(conf, model, st_frame, image):
    """
    Process the image for object detection, display the results, 
    and save cropped images of persons with violations.

    Args:
        conf (float): Confidence threshold for detection.
        model (YOLO): YOLO model for object detection.
        st_frame (Streamlit.empty): Streamlit placeholder for displaying frames.
        image (numpy.ndarray): Image to process.
    """
    # Resize image to maintain aspect ratio
    image = cv2.resize(image, (720, int(720 * (9 / 16))))
    results = model.track(image, conf=conf, persist=True)  # Perform object detection

    res_plotted = results[0].plot()  # Visualize detection results

    # Filter detections for persons
    persons = [det for det in results[0].boxes if model.names[int(det.cls)] == 'person']
    violations = ['no-helmet', 'no-vest']  # Violation classes to check

    # Check and save persons with violations
    for det in results[0].boxes:
        class_id = int(det.cls)
        label = model.names[class_id]
        if label in violations:
            for person in persons:
                px1, py1, px2, py2 = map(int, person.xyxy[0])
                vx1, vy1, vx2, vy2 = map(int, det.xyxy[0])
                if px1 <= vx1 and py1 <= vy1 and px2 >= vx2 and py2 >= vy2:
                    save_person(image, (px1, py1, px2, py2), label)

    # Display the processed frame in Streamlit
    st_frame.image(res_plotted, caption='Detected Video', channels="BGR", use_column_width=True)

# Play and detect objects in RTSP streams
def play_rtsp(rtsp, conf, model):
    """
    Process and display object detection on RTSP video streams.

    Args:
        rtsp (str): RTSP URL for the video stream.
        conf (float): Confidence threshold for detection.
        model (YOLO): YOLO model for object detection.
    """
    st.text(f"RTSP URL : {rtsp}")
    if st.button('Detect Objects'):
        try:
            vid_cap = cv2.VideoCapture(rtsp)
            st_frame = st.empty()
            while vid_cap.isOpened():
                success, image = vid_cap.read()
                if success:
                    display(conf, model, st_frame, image)
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            vid_cap.release()
            st.sidebar.error("Error : " + str(e))

# Play and detect objects from webcam
def play_webcam(conf, model):
    """
    Process and display object detection on a webcam feed.

    Args:
        conf (float): Confidence threshold for detection.
        model (YOLO): YOLO model for object detection.
    """
    st.title("Webcam Page")
    source_webcam = env.WEBCAM_PATH

    if st.button('Detect Objects'):
        try:
            vid_cap = cv2.VideoCapture(source_webcam)
            st_frame = st.empty()
            while vid_cap.isOpened():
                success, image = vid_cap.read()
                if success:
                    display(conf, model, st_frame, image)
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Error : " + str(e))

# Play and detect objects from uploaded video
def play_video(conf, model):
    """
    Process and display object detection on an uploaded video file.

    Args:
        conf (float): Confidence threshold for detection.
        model (YOLO): YOLO model for object detection.
    """
    st.title("Uploaded Video Page")
    uploaded_file = st.file_uploader("Choose a video file...", type=["mp4", "mov", "avi", "mkv"])

    if uploaded_file is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())
        vid_cap = cv2.VideoCapture(tfile.name)

        st_frame = st.empty()
        if st.button('Detect Video Objects'):
            try:
                while vid_cap.isOpened():
                    success, image = vid_cap.read()
                    if success:
                        display(conf, model, st_frame, image)
                    else:
                        vid_cap.release()
                        break
            except Exception as e:
                st.sidebar.error("Error : " + str(e))

# Create a database connection using pymysql
def get_connection_pymysql():
    """
    Create and return a MySQL database connection using pymysql.

    Returns:
        pymysql.connections.Connection: The pymysql connection object.
    """
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='st_ppe',
        charset='utf8mb4'
    )
    return connection

# Create a database connection using SQLAlchemy
def get_connection_sqlalchemy():
    """
    Create and return a MySQL database connection using SQLAlchemy.

    Returns:
        sqlalchemy.engine.base.Engine: The SQLAlchemy engine object.
    """
    engine = create_engine('mysql+pymysql://root:@localhost:3306/st_ppe?charset=utf8mb4')
    return engine

# Fetch data from a database table
def fetch_data():
    """
    Fetch data from the database and return it as a pandas DataFrame.

    Returns:
        pandas.DataFrame: DataFrame containing the fetched data.
    """
    engine = get_connection_sqlalchemy()
    with engine.connect() as connect:
        sql = text("SELECT value1, value2 from data")
        df = pd.read_sql(sql, engine)
        return df

# Fetch RTSP URLs from the database
def fetch_rtsp():
    """
    Fetch RTSP URLs from the database.

    Returns:
        list: List of RTSP URLs and their associated metadata.
    """
    engine = get_connection_sqlalchemy()
    with engine.connect() as connect:
        sql = text("SELECT id, link, tempat FROM rtsp")
        result = connect.execute(sql)
        results = result.fetchall()
        return results

# Generate a pie chart using pyecharts
def chart_pie(df):
    """
    Generate a pie chart from a pandas DataFrame.

    Args:
        df (pandas.DataFrame): DataFrame containing the chart data.

    Returns:
        Pie: The generated Pie chart object.
    """
    data = [list(z) for z in zip(df['value1'], df['value2'])]
    c_pie = (
        Pie()
        .add(series_name="Pie", data_pair=data)
        .set_global_opts(title_opts=opts.TitleOpts(title="Pie-After"))
        .set_series_opts(label_opts=opts.LabelOpts())
    )
    return c_pie

# Render a pyecharts chart in Streamlit
def make_chart(c):
    """
    Render a pyecharts chart in a Streamlit app.

    Args:
        c (pyecharts.charts.Chart): The chart object to render.
    """
    st_pyecharts(c)
