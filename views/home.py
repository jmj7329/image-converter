import streamlit as st

st.set_page_config(page_title="Free Converters", page_icon="🛠️", layout="centered")

st.markdown("<h1 style='text-align: center;'>Free Online Utilities</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>No sign-up required. Fast, free, and completely browser-based.</p>", unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns(2, gap="medium")

with col1:
    with st.container(border=True):
        st.subheader("🖼️ Image Converter")
        st.write("Convert PNG, JPEG, WEBP, TIFF, and BMP images instantly.")
        if st.button("Open Image Converter", key="btn_image", use_container_width=True, type="primary"):
            st.switch_page("views/image_app.py")

with col2:
    with st.container(border=True):
        st.subheader("📄 PDF Converter")
        st.write("Coming soon...")
        st.button("Open PDF Converter", key="btn_pdf", use_container_width=True, disabled=True)
