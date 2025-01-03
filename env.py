from pathlib import Path
import sys
from PIL import Image

MODEL_DIR = Path('weights')
DETECTION_MODEL = MODEL_DIR / 'yolov8n-epoch50-lr0001.pt'
ERSGAN_MODEL = MODEL_DIR / 'RealESRGAN_x4.pth'


VIOLATION_HARDHAT_DIR = Path('violation_hardhat')
VIOLATION_SAFETY_VEST_DIR = Path('violation_safety_vest')

VIDEO = 'Video'
WEBCAM = 'Webcam'
RTSP = 'RTSP'

SOURCES_LIST = [VIDEO, WEBCAM, RTSP]

JEMBATAN = 'Jembatan'
EX1 = 'Contoh 1'
EX2 = 'Contoh 2'
EX3 = 'Contoh 3'
EX4 = 'Contoh 4'
EX5 = 'Contoh 5'

RTSP_LIST = [JEMBATAN, EX1, EX2, EX3, EX4, EX5]

file_doc = "dokumentasi.pdf"

with open(file_doc, "rb") as file:
    file_bytes = file.read()

data = [
    ("Class1", "999"),
    ("Class2", "888"),
    ("Class3", "777"),
    ("Class4", "688"),
    ("Class5", "588")
]

WEBCAM_PATH = 0
EXCAM_PATH = 1
