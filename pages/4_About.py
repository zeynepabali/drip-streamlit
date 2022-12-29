import streamlit as st
from PIL import Image

about_image = Image.open("data/about_dippi.jfif")
st.image(about_image, width=600)