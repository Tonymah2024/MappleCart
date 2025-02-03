import streamlit as st
from pyzbar.pyzbar import decode
from PIL import Image

# Barcode Scanner
def scan_barcode(image):
    decoded_objects = decode(image)
    for obj in decoded_objects:
        return obj.data.decode('utf-8')
    return None

# Function to Check if Barcode is Canadian
def is_canadian_product(barcode):
    canadian_prefixes = tuple(str(i).zfill(3) for i in range(0, 14)) + ('754', '755')  # Updated Canadian GS1 prefixes
    return barcode.startswith(canadian_prefixes)

# Streamlit App
st.title("MapleCart - Check if a Product is Canadian")

# Barcode Scanner
st.header("Scan Barcode")
barcode_image = st.file_uploader("Upload Barcode Image", type=["png", "jpg", "jpeg"])

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
