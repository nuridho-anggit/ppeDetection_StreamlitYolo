from PIL import Image
from streamlit_echarts import st_pyecharts
import streamlit as st
import time
from pyecharts import options as opts
from pyecharts.charts import Pie


import env
import func

icon = Image.open("ptba-icon.png")
st.set_page_config(
    page_title="PTBA PPE Detection",
    page_icon=icon,
    # layout="wide",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Menampilkan judul aplikasi
st.title("Visualisasi Data")

with st.spinner('Connecting...'):
    time.sleep(2)


data_resources = func.fetch_data()
print(data_resources)
func.make_chart(func.chart_pie(data_resources))

# conn = func.get_connection()
# df = conn.query('SELECT value1, value2 from data;', ttl=600)
# print(df)
# func.make_chart(func.chart_pie(df))
# st.write(" ")

st.download_button(label="Download Chart",
                   data=env.file_bytes,
                   file_name=env.file_doc,
                   mime="application/pdf"
                   )

