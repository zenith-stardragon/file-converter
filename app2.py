import streamlit as st
from PIL import Image
import base64
import io
from moviepy.editor import VideoFileClip
import os

# Convert images using Pillow library
def convert_image(file, output_format):
    img = Image.open(file).convert('RGB')
    img_io = io.BytesIO()
    img.save(img_io, format=output_format, quality=100)
    img_io.seek(0)
    return img_io

# Convert videos to gif using MoviePy
def convert_video(file):
    tmpfile=os.path.join("temp.mp4")
    with open(tmpfile, "wb") as f:
        f.write(file.getbuffer())
    clip = VideoFileClip(tmpfile)
    gif_path = 'temp.gif'
    clip.write_gif(gif_path)
    return gif_path

# Function to create a download link
def get_download_link(file, output_format, is_video=False):
    b64 = base64.b64encode(file.read()).decode() 
    return f'<a href="data:file/{output_format};base64,{b64}" download="converted.{output_format}">Download converted file</a>'

# Streamlit Application
st.title('File Converter')

file = st.file_uploader("Upload file", type=["png", "jpg", "jpeg", "mp4"])

if file is not None:
    if file.type.startswith('image/'):
        output_format = st.selectbox('Select output format', ['png', 'jpeg'])
        output_format_pillow = 'JPEG' if output_format == 'jpeg' else output_format
        if st.button('Convert image'):
            converted_image = convert_image(file, output_format_pillow)
            st.markdown(get_download_link(converted_image, output_format), unsafe_allow_html=True)

    elif file.type.startswith('video/'):
        if st.button('Convert to gif'):
            converted_gif_path = convert_video(file)
            with open(converted_gif_path, "rb") as gif_file:
                st.markdown(get_download_link(gif_file, 'gif', is_video=True), unsafe_allow_html=True)
            os.remove("temp.mp4")
            os.remove(converted_gif_path) 


