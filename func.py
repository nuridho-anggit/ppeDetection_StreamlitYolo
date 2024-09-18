import pandas as pd
from ultralytics import YOLO
import time
from time import gmtime
import streamlit as st
import cv2
import tempfile
import os
import env
from time import gmtime, strftime
from pathlib import Path
from pyecharts import options as opts
from pyecharts.charts import Pie
from streamlit_echarts import st_pyecharts
import pymysql
from sqlalchemy import create_engine, text
import torch


def load_model(model_path):
    model = YOLO(model_path)
    return model


def save_person(image, person_box, label):
    x1, y1, x2, y2 = map(int, person_box)
    cropped_image = image[y1:y2, x1:x2]

    base_directory = None

    if label == 'no-helmet':
        base_directory = Path(env.VIOLATION_HARDHAT_DIR)
        new_label = "vioHardHat_"
    elif label == 'no-vest':
        base_directory = Path(env.VIOLATION_SAFETY_VEST_DIR)
        new_label = "vioSafetyVest_"

    if base_directory is not None:
        date_directory = base_directory / strftime("%Y%m%d", gmtime())
        if not date_directory.exists():
            date_directory.mkdir(parents=True, exist_ok=True)

        filename = date_directory / f'{new_label}{strftime("%y%m%d_%H%M%S", gmtime())}.jpg'

        cv2.imwrite(str(filename), cropped_image)
    else:
        print("Error to save")


def display(conf, model, st_frame, image):
    image = cv2.resize(image, (720, int(720 * (9 / 16))))  # default
    # image = cv2.resize(image, (int(720 * (9 / 16)), 720)) #Vertikal
    results = model.track(image, conf=conf, persist=True)

    res_plotted = results[0].plot()

    persons = [det for det in results[0].boxes if model.names[int(det.cls)] == 'person']
    violations = ['no-helmet', 'no-vest']

    for det in results[0].boxes:
        class_id = int(det.cls)
        label = model.names[class_id]
        if label in violations:
            for person in persons:
                px1, py1, px2, py2 = map(int, person.xyxy[0])
                vx1, vy1, vx2, vy2 = map(int, det.xyxy[0])
                if px1 <= vx1 and py1 <= vy1 and px2 >= vx2 and py2 >= vy2:
                    save_person(image, (px1, py1, px2, py2), label)

    st_frame.image(res_plotted,
                   caption='Detected Video',
                   channels="BGR",
                   use_column_width=True
                   )


def play_rtsp(rtsp, conf, model):
    # st.title("RTSP Page")
    # source_rtsp = st.text_input("rtsp url:")
    # st.caption('Example of RTSP URL: rtsp://admin:12345@192.168.1.210:554/')
    st.text(f"RTSP URL : {rtsp}")
    if st.button('Detect Objects'):
        try:
            vid_cap = cv2.VideoCapture(rtsp)
            st_frame = st.empty()
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    display(conf, model, st_frame, image)
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            vid_cap.release()
            st.sidebar.error("Error : " + str(e))


def play_webcam(conf, model):
    st.title("Webcam Page")
    source_webcam = env.WEBCAM_PATH

    if st.button('Detect Objects'):
        try:
            vid_cap = cv2.VideoCapture(source_webcam)
            st_frame = st.empty()
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    display(conf, model, st_frame, image)
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Error : " + str(e))


def play_video(conf, model):
    st.title("Uploaded Video Page")
    uploaded_file = st.file_uploader("Choose a video file...", type=["mp4", "mov", "avi", "mkv"])

    if uploaded_file is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())
        vid_cap = cv2.VideoCapture(tfile.name)

        st_frame = st.empty()
        if st.button('Detect Video Objects'):
            try:
                while (vid_cap.isOpened()):
                    success, image = vid_cap.read()
                    if success:
                        display(conf, model, st_frame, image)
                    else:
                        vid_cap.release()
                        break
            except Exception as e:
                st.sidebar.error("Error : " + str(e))


def get_connection():
    return st.connection('mysql', type='sql')


def get_connection_pymysql():
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='st_ppe',
        charset='utf8mb4'
    )
    return connection


def get_connection_sqlalchemy():
    engine = create_engine('mysql+pymysql://root:@localhost:3306/st_ppe?charset=utf8mb4')
    return engine


def fetch_data():
    engine = get_connection_sqlalchemy()
    with engine.connect() as connect:
        sql = text("SELECT value1, value2 from data")
        df = pd.read_sql(sql, engine)
        return df


def fetch_rtsp():
    engine = get_connection_sqlalchemy()
    with engine.connect() as connect:
        sql = text("SELECT id, link, tempat FROM rtsp")
        result = connect.execute(sql)
        results = result.fetchall()
        return results


def chart_pie(df):
    data = [list(z) for z in zip(df['value1'], df['value2'])]
    c_pie = (
        Pie()
        .add(series_name="Pie", data_pair=data)
        .set_global_opts(title_opts=opts.TitleOpts(title="Pie-After"))
        .set_series_opts(label_opts=opts.LabelOpts())
    )
    return c_pie


def chart_area():
    c_area = (

    )
    return c_area


def make_chart(c):
    st_pyecharts(c)
