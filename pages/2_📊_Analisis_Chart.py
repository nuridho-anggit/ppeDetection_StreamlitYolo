from PIL import Image
from streamlit_echarts import st_pyecharts
import streamlit as st
import time
from pyecharts import options as opts
from pyecharts.charts import Pie

import env
import func

# Load icon for the application
# This section sets up the application icon and configuration settings.
icon = Image.open("ptba-icon.png")
st.set_page_config(
    page_title="PTBA PPE Detection",  # Title of the application displayed in the browser tab
    page_icon=icon,  # Icon used for the application
    layout="centered",  # Centers the layout on the page
    initial_sidebar_state="expanded"  # Sidebar starts in expanded state
)

# Display the title of the application
# This adds a main title to the page for user clarity.
st.title("Visualisasi Data")

# Display a spinner while performing background tasks
# This provides feedback to the user while data is being processed.
with st.spinner('Connecting...'):
    time.sleep(2)  # Simulate a connection delay

# Fetch data resources using a helper function
# The data is fetched from a predefined source and then processed further.
data_resources = func.fetch_data()
print(data_resources)  # Debugging: Print fetched data to the console for verification

# Generate and display a pie chart from the fetched data
# This function processes the data and creates a pie chart visualization.
func.make_chart(func.chart_pie(data_resources))

# Example of querying a database (currently commented out)
# Uncomment and adjust as needed to integrate with a database.
# conn = func.get_connection()
# df = conn.query('SELECT value1, value2 from data;', ttl=600)
# print(df)  # Debugging: Print the queried data for verification
# func.make_chart(func.chart_pie(df))
# st.write(" ")

# Add a download button to allow users to download the generated chart
# The chart is downloaded as a PDF file with a predefined filename and MIME type.
st.download_button(
    label="Download Chart",  # Label displayed on the button
    data=env.file_bytes,  # File content to be downloaded
    file_name=env.file_doc,  # Suggested filename for the download
    mime="application/pdf"  # MIME type for the file
)
