# image_filter_app.py
import streamlit as st
from PIL import Image, ImageFilter, ImageOps
import io

st.title("🖼️ Image Filter App")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_column_width=True)

    filter_option = st.selectbox("Choose a filter", ["Grayscale", "Blur", "Contour", "Edge Enhance"])

    if filter_option == "Grayscale":
        filtered_img = ImageOps.grayscale(image)
    elif filter_option == "Blur":
        filtered_img = image.filter(ImageFilter.BLUR)
    elif filter_option == "Contour":
        filtered_img = image.filter(ImageFilter.CONTOUR)
    elif filter_option == "Edge Enhance":
        filtered_img = image.filter(ImageFilter.EDGE_ENHANCE)

    st.image(filtered_img, caption=f"{filter_option} Image", use_column_width=True)

    
