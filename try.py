# import cv2
# from ultralytics import YOLO
# import numpy as np
# import env
# import func
# from pathlib import Path
# import streamlit as st
# from streamlit_echarts import JsCode
# from streamlit_echarts import st_echarts
# from streamlit_echarts import st_pyecharts
#
# # img = cv2.imread("contoh1.jpg")
# # height, width = img.shape[:2]
# # res_img = cv2.resize(img, (width * 10, height * 10), interpolation=cv2.INTER_AREA)
# #
# # cv2.imshow("Real Image", res_img)
# # cv2.imwrite(filename="contoh1_resized3.jpg", img=res_img)
# # cv2.waitKey(0)
# #
# # kernel = np.array([[-1, -1, -1, -1, -1],
# #                    [-1, -1, 15, -1, -1],
# #                    [-1, -1, -1, -1, -1]
# #                    ])
# #
# # sharp_img = cv2.filter2D(res_img, -1, kernel)
# # cv2.imshow("Sharpened", sharp_img)
# # cv2.waitKey(0)
# #
# # canny_img = cv2.Canny(res_img, 50, 210)
# # cv2.imshow("Canny", canny_img)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()
# #
# # import time
# #
# # # Get the current time
# # current_time = time.localtime()
# #
# # # Format the time using strftime()
# # formatted_time = time.strftime("%H:%M:%S", current_time)
# # formatted_time_am_pm = time.strftime("%I:%M:%S %p", current_time)
# #
# # # Print the formatted time
# # print("Formatted Time (24-hour format):", formatted_time)
# # print("Formatted Time (12-hour format):", formatted_time_am_pm)
#
# # from datetime import datetime
# #
# # # get current date and time
# # current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
# # print("Current date & time : ", current_datetime)
# #
# # # convert datetime obj to string
# # str_current_datetime = str(current_datetime)
# #
# # # create a file object along with extension
# # file_name = str_current_datetime + ".txt"
# # file = open(file_name, 'w')
# #
# # print("File created : ", file.name)
# # file.close()
#
# # from time import gmtime, strftime
# # print(strftime("%a, %d %b %Y %X", gmtime()))
#
# # import face_recognition
#
# # import streamlit as st
# # from vega_datasets import data
# #
# # source = data.barley()
# #
# # st.bar_chart(source, x="variety", y="yield", color="site", horizontal=True)
#
# # model_path = Path(env.DETECTION_MODEL)
# #
# # model = func.load_model(model_path)
#
# # model.track("before_img.jpg", conf=0.5, show=True, save=True)
#
#
# # import streamlit as st
# # from streamlit_image_comparison import image_comparison
# #
# # # set page config
# # st.set_page_config(page_title="Image-Comparison Example", layout="centered")
# #
# # # render image-comparison
# # image_comparison(
# #     img1="before_img.jpg",
# #     img2="after_img.jpg",
# #     label1="text1",
# #     label2="text1",
# #     width=700,
# #     starting_position=50,
# #     show_labels=True,
# #     make_responsive=True,
# #     in_memory=True,
# # )
#
# from sqlalchemy import create_engine
# # import streamlit as st
# #
# # df = env.conn.query('SELECT value1, value2 from data;', ttl=600)
# # st.line_chart(df)


# import torch
# from ultralytics import YOLO
#
# # Check for CUDA device and set it
# # device = 'cuda' if torch.cuda.is_available() else 'cpu'
# print(torch.cuda.is_available())

# import torch
#
# print(torch.__version__)
# print(torch.version.cuda)
# print(torch.cuda.is_available())
# print(torch.cuda.device_count())
# print(torch.cuda.get_device_name(0))
# import torch
# from ultralytics import YOLO
#
# import env
#
# device = 'cuda' if torch.cuda.is_available() else 'cpu'
# print(f'Using device: {device}')
# # model = YOLO(env.DETECTION_MODEL, 'gpu')
# model = YOLO(env.DETECTION_MODEL).to(device)
#
# # model.track("rtsp://admin:Tarahan17@10.5.4.159:554/axis-media/media.amp", show=True, conf=0.7, plots=True)
# model.track("rtsp://viewer:Ptba100%@10.5.4.215:554/axis-media/media.amp", show=True, conf=0.7, plots=True)

# from ultralytics import YOLO
#
# import env
#
# model = YOLO(env.DETECTION_MODEL)
#
# class_names = model.names
# print(class_names)

# def perhitungan_bmi(berat_udin, tinggi_udin, berat_nanang, tinggi_nanang):
#     def hitung(berat, tinggi):
#         bmi = berat / tinggi
#         return bmi
#
#     bmi_udin = hitung(berat_udin, tinggi_udin)
#     bmi_nanang = hitung(berat_nanang, tinggi_nanang)
#
#     udin_menang = bmi_udin > bmi_nanang
#     nanang_menang = bmi_nanang > bmi_udin
#
#     if (udin_menang == True):
#         print(f"BMI Udin({bmi_udin}) lebih tinggi dari Nanang ({bmi_nanang})!")
#     elif (nanang_menang == True):
#         print(f"BMI Nanang({bmi_nanang})lebih tinggi dari Udin ({bmi_udin}) !")
#
#
# print("Data Uji")
# print("Data 1 :")
# perhitungan_bmi(78, 1.69, 92, 1.95)
# print("Data 2 : ")
# perhitungan_bmi(95, 1.88, 85, 1.76)

import torch
from PIL import Image
import numpy as np
from RealESRGAN import RealESRGAN

import env

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print(device)
model = RealESRGAN(device, scale=4)
model.load_weights(env.ERSGAN_MODEL)

path_to_image = 'vioHardHat_240812_081801.jpg'
image = Image.open(path_to_image).convert("RGB")

sr_image = model.predict(image)

sr_image.save('sr_image.png')

# import torch
#
# print(torch.__version__)
# print(torch.version.cuda)
# print(torch.cuda.is_available())
# print(torch.cuda.device_count())
# print(torch.cuda.get_device_name(0))
