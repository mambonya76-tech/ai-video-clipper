import streamlit as st
import os
from moviepy.editor import VideoFileClip

st.set_page_config(page_title="AI Video Clipper Proto", layout="centered")

st.title("🎬 AI Video Clipper (Prototype)")
st.write("I-upload ang iyong mahabang video at subukan ang manual na paggupit nito.")

uploaded_file = st.file_uploader("Pumili ng MP4 video...", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    temp_input_path = "temp_input.mp4"
    temp_output_path = "temp_output.mp4"
    
    with open(temp_input_path, "wb") as f:
        f.write(uploaded_file.read())
        
    st.subheader("Original Video")
    st.video(temp_input_path)
    
    try:
        clip = VideoFileClip(temp_input_path)
        duration = clip.duration
        clip.close()
        
        st.success(f"Matagumpay na na-load ang video! Haba: {duration:.2f} segundo.")
        
        st.subheader("Subukan ang Pag-cut")
        col1, col2 = st.columns(2)
        with col1:
            start_time = st.number_input("Magsimula sa (segundo):", min_value=0.0, max_value=float(duration), value=0.0)
        with col2:
            end_time = st.number_input("Matapos sa (segundo):", min_value=0.0, max_value=float(duration), value=min(15.0, float(duration)))
        
        if st.button("Gupitin ang Video"):
            if start_time >= end_time:
                st.error("Ang start time ay dapat mas mababa sa end time.")
            else:
                with st.spinner("Ginugupit ang video... Mangyaring maghintay..."):
                    try:
                        with VideoFileClip(temp_input_path) as video:
                            subclip = video.subclip(start_time, end_time)
                            subclip.write_videofile(
                                temp_output_path, 
                                codec="libx264", 
                                audio_codec="aac",
                                temp_audiofile="temp-audio.m4a", 
                                remove_temp=True
                            )
                        
                        st.success("Tapos na ang paggupit!")
                        st.subheader("Short Video Output")
                        st.video(temp_output_path)
                        
                        with open(temp_output_path, "rb") as file:
                            st.download_button(
                                label="I-download ang Short Video",
                                data=file,
                                file_name="short_clip.mp4",
                                mime="video/mp4"
                            )
                    except Exception as e:
                        st.error(f"Nagka-error sa pag-cut: {e}")
                        
    except Exception as e:
        st.error(f"Hindi mabasa ang video file: {e}")
