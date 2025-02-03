import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Barcode Scanner using OpenCV
def scan_barcode(image):
    image_np = np.array(image)
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(image_np)
    return data if data else None

# Function to Check if Barcode is Canadian
def is_canadian_product(barcode):
    canadian_prefixes = tuple(str(i).zfill(3) for i in range(0, 14)) + ('754', '755')  # Updated Canadian GS1 prefixes
    return barcode.startswith(canadian_prefixes)

# Streamlit App
st.title("MapleCart - Check if a Product is Canadian")

# Barcode Scanner
st.header("Scan Barcode")
barcode_image = st.file_uploader("Upload Barcode Image", type=["png", "jpg", "jpeg"])

# Real-Time Camera Barcode Scanner
st.header("Real-Time Camera Barcode Scanner")
start_camera = st.button("Start Camera")

if start_camera:
    cap = cv2.VideoCapture(0)
    stframe = st.empty()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture from camera")
            break

        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(frame)

        if data:
            st.success(f"Detected Barcode: {data}")
            if is_canadian_product(data):
                st.success("✅ This product is Canadian.")
            else:
                st.warning("⚠️ This product is not recognized as Canadian.")
            break

        stframe.image(frame, channels="BGR")

    cap.release()

# Manual Verification
st.header("Manual Product Verification")
manual_barcode = st.text_input("Enter Barcode Number Manually")

# Function to Verify Product
def verify_product(barcode):
    if barcode:
        st.success(f"Entered Barcode: {barcode}")
        if is_canadian_product(barcode):
            st.success("✅ This product is Canadian.")
        else:
            st.warning("⚠️ This product is not recognized as Canadian.")
    else:
        st.info("Please enter a barcode to verify.")

# Barcode Image Upload Verification
if barcode_image:
    image = Image.open(barcode_image)
    barcode = scan_barcode(image)
    verify_product(barcode)

# Manual Barcode Verification
if manual_barcode:
    verify_product(manual_barcode)
