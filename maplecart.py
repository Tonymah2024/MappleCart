import streamlit as st
import numpy as np
from PIL import Image
import base64

# Function to Check if Barcode is Canadian
def is_canadian_product(barcode):
    canadian_prefixes = tuple(str(i).zfill(3) for i in range(0, 14)) + ('754', '755')  # Updated Canadian GS1 prefixes
    return barcode.startswith(canadian_prefixes)

# Streamlit App
st.title("MapleCart - Check if a Product is Canadian")

# Mobile Camera Barcode Scanner using HTML5 and Barcode Detection
st.header("Mobile Camera Barcode Scanner")
st.markdown('''
    <video id="video" width="300" height="200" autoplay></video>
    <canvas id="canvas" width="300" height="200" style="display:none;"></canvas>
    <script src="https://unpkg.com/@zxing/library@latest"></script>
    <script>
        const codeReader = new ZXing.BrowserMultiFormatReader();
        codeReader.decodeFromConstraints({ video: { facingMode: "environment" } }, 'video', (result, err) => {
            if (result) {
                window.parent.postMessage(result.text, '*');
            }
        });
    </script>
''', unsafe_allow_html=True)

# Receive Barcode Data from Client
barcode_data = st.text_input("Scanned Barcode (auto-filled):")

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

# Barcode Verification
if barcode_data:
    verify_product(barcode_data)

# Manual Barcode Verification
if manual_barcode:
    verify_product(manual_barcode)
