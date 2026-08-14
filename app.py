import streamlit as st
from PIL import Image
import io
import os
import html

# 1. Page Configuration
st.set_page_config(
    page_title="Image Converter", 
    page_icon="🖼️", 
    layout="centered"
)

# --- Session State Initialization ---
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0
if "persisted_file" not in st.session_state:
    st.session_state.persisted_file = None
if "converted_bytes" not in st.session_state:
    st.session_state.converted_bytes = None
if "converted_format" not in st.session_state:
    st.session_state.converted_format = None
if "download_file_name" not in st.session_state:
    st.session_state.download_file_name = None
if "current_file_name" not in st.session_state:
    st.session_state.current_file_name = None
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# --- Top Right Navigation (Toggle + Popover Menu) ---
toggle_label = "🌙 Dark" if not st.session_state.dark_mode else "☀️ Light"
dark_mode = st.toggle(toggle_label, value=st.session_state.dark_mode, key="dark_mode_widget")
st.session_state.dark_mode = dark_mode

# Circular popover button with icon
with st.popover("☰"):
    st.link_button("1. Go to Google", "https://www.google.com", use_container_width=True)
    st.link_button("2. Go to GitHub", "https://github.com", use_container_width=True)
    st.link_button("3. Streamlit Docs", "https://docs.streamlit.io", use_container_width=True)
    st.link_button("4. YouTube", "https://www.youtube.com", use_container_width=True)

# --- Dynamic Color Variables for Light & Dark Mode ---
if dark_mode:
    bg_gradient = "linear-gradient(180deg, #1e293b 0%, #0f172a 220px, #0f172a 100%)"
    text_color = "#f8fafc"
    sub_color = "#94a3b8"
    card_bg = "#1e293b"
    card_border = "#334155"
    uploader_bg = "#1e293b"
    uploader_border = "#475569"
    input_bg = "#0f172a"
    btn_sec_bg = "#334155"
    btn_sec_text = "#f8fafc"
    btn_sec_border = "#475569"
    hover_bg = "rgba(255, 255, 255, 0.1)"
else:
    bg_gradient = "#ffffff"
    text_color = "#1e293b"
    sub_color = "#64748b"
    card_bg = "#ffffff"
    card_border = "#e2e8f0"
    uploader_bg = "#f8fafc"
    uploader_border = "#cbd5e1"
    input_bg = "#ffffff"
    btn_sec_bg = "#f1f5f9"
    btn_sec_text = "#475569"
    btn_sec_border = "#cbd5e1"
    hover_bg = "rgba(0, 0, 0, 0.05)"

# 2. Custom CSS Injection
st.markdown(f"""
    <style>
    /* 1. Solid Top Bar matching theme (50px high) */
    .stApp::after {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 50px;
        background-color: {card_bg};
        border-bottom: 1px solid {card_border};
        z-index: 999;
        pointer-events: none;
    }}

    /* 2. Top Gradient Fade starting below top bar */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 50px;
        left: 0;
        width: 100%;
        height: 30px;
        background: linear-gradient(to bottom, {card_bg}, transparent);
        z-index: 998;
        pointer-events: none;
    }}

    /* 3. Push main page content down below top bar */
    .block-container {{
        padding-top: calc(2rem + 50px) !important; 
        position: relative;
    }}

    /* Hide Streamlit default header bar */
    header[data-testid="stHeader"] {{
        display: none !important;
    }}

    /* Pin Dark Mode Toggle to top-right bar */
    div[data-testid="stToggle"] {{
        position: fixed !important;
        top: 10px !important;
        right: 65px !important;
        z-index: 999999 !important;
    }}

    /* Pin Menu Popover to far right of top bar */
    div[data-testid="stPopover"] {{
        position: fixed !important;
        top: 6px !important;
        right: 12px !important;
        z-index: 999999 !important;
    }}

    /* Circular Minimalist Popover Menu Button */
    div[data-testid="stPopover"] > button {{
        background-color: transparent !important;
        color: {text_color} !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        width: 38px !important;
        height: 38px !important;
        border-radius: 50% !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 1.2rem !important;
    }}

    div[data-testid="stPopover"] > button:hover,
    div[data-testid="stPopover"] > button:focus {{
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        background-color: {hover_bg} !important;
        color: #4f46e5 !important;
    }}

    /* Popover Dropdown Container Styling */
    div[data-testid="stPopoverBody"],
    div[data-baseweb="popover"] > div {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
        border: 1px solid {card_border} !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15) !important;
    }}

    /* Fix Menu Choice Items inside Popover Dropdown */
    div[data-testid="stPopoverBody"] a,
    div[data-testid="stPopoverBody"] button {{
        background-color: {btn_sec_bg} !important;
        color: {btn_sec_text} !important;
        border: 1px solid {btn_sec_border} !important;
        border-radius: 8px !important;
    }}

    div[data-testid="stPopoverBody"] a:hover,
    div[data-testid="stPopoverBody"] button:hover {{
        border-color: #4f46e5 !important;
        color: #4f46e5 !important;
    }}

    div[data-testid="stPopoverBody"] p,
    div[data-testid="stPopoverBody"] span {{
        color: {btn_sec_text} !important;
    }}

    /* Global Background */
    .stApp {{
        background: {bg_gradient};
    }}

    /* Header text styling */
    .title-text {{
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        color: {text_color} !important;
        margin-bottom: 0px;
    }}
    
    .subtitle-text {{
        text-align: center;
        font-size: 1.2rem;
        color: {sub_color} !important;
        margin-bottom: 30px;
    }}

    /* Toggle Label Color */
    div[data-testid="stWidgetLabel"] p,
    label[data-testid="stWidgetLabel"] span {{
        color: {text_color} !important;
        font-weight: 600 !important;
        opacity: 1 !important;
    }}

    /* Success message text color */
    div[data-testid="stAlert"] *,
    div[data-testid="stAlert"] p,
    div[data-testid="stAlert"] span {{
        color: #000000 !important;
        font-weight: 600 !important;
    }}

    /* Drag & Drop Upload Container */
    div[data-testid="stFileUploader"] {{
        background-color: {uploader_bg} !important;
        border: 2px dashed {uploader_border} !important;
        border-radius: 16px !important;
        padding: 35px 20px !important;
    }}

    div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"],
    div[data-testid="stFileUploaderDropzone"] {{
        display: flex !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }}

    /* Hide Streamlit default file badge list */
    div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] ~ *,
    div[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"],
    div[data-testid="stFileUploader"] [data-testid="stFileUploaderFileData"],
    div[data-testid="stFileUploader"] [data-testid="stFileUploaderFileName"],
    div[data-testid="stFileUploader"] [data-testid="stFileUploaderDeleteBtn"],
    div[data-testid="stFileUploader"] ul,
    div[data-testid="stFileUploader"] [role="list"],
    div[data-testid="stFileUploader"] [role="listitem"] {{
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
        margin: 0px !important;
        padding: 0px !important;
        overflow: hidden !important;
    }}

    /* Centered Upload Button */
    div[data-testid="stFileUploader"] button {{
        width: 140px !important;
        height: 60px !important;
        background-color: #4f46e5 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 16px !important;
        font-weight: 700 !important;
        font-size: 3rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25) !important;
        margin: 0 auto !important;
    }}

    div[data-testid="stFileUploader"] button:hover {{
        background-color: #4338ca !important;
    }}

    div[data-testid="stFileUploaderDropzoneInstructions"] span,
    div[data-testid="stFileUploaderDropzoneInstructions"] small {{
        font-size: 0.72rem !important;
        color: {sub_color} !important;
        opacity: 0.85 !important;
    }}

    .terms-text {{
        text-align: center;
        font-size: 0.78rem;
        color: {sub_color} !important;
        margin-top: 12px;
        margin-bottom: 30px;
    }}

    .file-preview-title {{
        color: {sub_color} !important;
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 8px;
        word-break: break-all;
    }}

    /* Selectbox styling */
    div[data-baseweb="select"] > div {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border-color: {card_border} !important;
        border-radius: 8px !important;
    }}
    
    div[data-baseweb="select"] span {{
        color: {text_color} !important;
    }}

    div[data-testid="stSelectbox"] label p {{
        color: {sub_color} !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
    }}

    /* Buttons */
    button[kind="primary"] {{
        background-color: #4f46e5 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }}
    
    button[kind="primary"]:hover {{
        background-color: #4338ca !important;
    }}

    button[kind="secondary"] {{
        background-color: {btn_sec_bg} !important;
        color: {btn_sec_text} !important;
        border: 1px solid {btn_sec_border} !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }}

    /* Feature card */
    .feature-card {{
        background-color: {card_bg};
        border: 1px solid {card_border};
        border-radius: 12px;
        padding: 24px;
        margin-top: 40px;
    }}
    
    .feature-title {{
        color: {text_color} !important;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 12px;
    }}

    .feature-list {{
        color: {sub_color} !important;
        font-size: 0.9rem;
        line-height: 1.6;
        margin: 0;
        padding-left: 18px;
    }}

    div[data-testid="stImage"] img {{
        border: 2px solid {card_border} !important;
        border-radius: 12px !important;
        padding: 4px !important;
        background-color: {card_bg} !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown('<h1 class="title-text">Image Converter</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Convert images online, for free.</p>', unsafe_allow_html=True)

# --- Drag & Drop Upload Zone ---
uploader_placeholder = st.empty()
terms_placeholder = st.empty()

if st.session_state.persisted_file is None:
    uploaded_file = uploader_placeholder.file_uploader(
        "Choose Files", 
        type=["png", "jpg", "jpeg", "webp", "bmp", "tiff"],
        label_visibility="collapsed",
        key=f"uploader_{st.session_state.uploader_key}"
    )

    terms_placeholder.markdown(
        '<p class="terms-text">By proceeding, you confirm you own the rights to the files you upload and agree to our Terms of Use.</p>', 
        unsafe_allow_html=True
    )
    
    if uploaded_file is not None:
        st.session_state.persisted_file = uploaded_file
        st.rerun()

# --- Converter Logic ---
if st.session_state.persisted_file is not None:
    
    uploader_placeholder.empty()
    terms_placeholder.empty()

    working_file = st.session_state.persisted_file

    if st.session_state.current_file_name != working_file.name:
        st.session_state.current_file_name = working_file.name
        st.session_state.converted_bytes = None
        st.session_state.converted_format = None
        st.session_state.download_file_name = None

    st.divider()

    # Reset the read pointer before every Image.open() call. Streamlit reruns
    # this script on every interaction (selecting a format, clicking a
    # button, etc.), and PIL leaves the underlying buffer's cursor at EOF
    # after decoding pixel data once. Without this seek, the second rerun
    # would try to read a PNG/JPEG header starting from EOF and raise
    # UnidentifiedImageError.
    working_file.seek(0)

    try:
        image = Image.open(working_file)
        image.load()  # force full decode now so any corruption surfaces here
    except Exception:
        st.error(
            "We couldn't read this file as an image. It may be corrupted "
            "or not a valid image file. Please remove it and try another."
        )
        image = None

    if image is not None:
        file_ext = working_file.name.split('.')[-1].upper()
        if file_ext == "JPG":
            file_ext = "JPEG"
        elif file_ext == "TIF":
            file_ext = "TIFF"

        all_formats = ["PNG", "JPEG", "WEBP", "BMP", "TIFF"]
        available_formats = [fmt for fmt in all_formats if fmt != file_ext]

        col1, col2 = st.columns([1, 1], gap="large")

        with col1:
            # Escape the filename before injecting it into raw HTML. The
            # filename is fully attacker-controlled (a user can upload a
            # file literally named "<img src=x onerror=alert(1)>.png"), and
            # markdown() is called with unsafe_allow_html=True, so without
            # escaping this is a reflected-XSS vector.
            safe_name = html.escape(working_file.name)
            st.markdown(
                f'<div class="file-preview-title">{safe_name}</div>',
                unsafe_allow_html=True
            )
            st.image(image, width="stretch")

        with col2:
            st.markdown('<div style="height: 32px;"></div>', unsafe_allow_html=True)

            if st.button("✕ Remove File", width="stretch", type="secondary"):
                st.session_state.uploader_key += 1
                st.session_state.persisted_file = None
                st.session_state.converted_bytes = None
                st.session_state.converted_format = None
                st.session_state.download_file_name = None
                st.session_state.current_file_name = None
                st.rerun()

            target_format = st.selectbox(
                "Convert to:",
                available_formats
            )

            # If the user changes the target format after already converting,
            # clear the stale result so the success message / download button
            # don't linger showing a conversion for a different format than
            # the one currently selected in the dropdown.
            if (
                st.session_state.converted_format is not None
                and st.session_state.converted_format != target_format
            ):
                st.session_state.converted_bytes = None
                st.session_state.converted_format = None
                st.session_state.download_file_name = None

            if st.button("Convert File", width="stretch", type="primary"):
                try:
                    buffer = io.BytesIO()
                    img_to_save = image.copy()

                    # JPEG and BMP can't store an alpha channel or a palette
                    # in Pillow — both raise OSError unless flattened to RGB
                    # first.
                    if target_format in ("JPEG", "BMP") and img_to_save.mode in ("RGBA", "P"):
                        img_to_save = img_to_save.convert("RGB")

                    img_to_save.save(buffer, format=target_format)

                    base_name = os.path.splitext(working_file.name)[0]

                    st.session_state.converted_bytes = buffer.getvalue()
                    st.session_state.converted_format = target_format
                    st.session_state.download_file_name = f"converted-{base_name}.{target_format.lower()}"
                except Exception:
                    st.error(
                        f"Sorry, we couldn't convert this image to {target_format}. "
                        "Please try a different format."
                    )

            if st.session_state.converted_bytes is not None:
                st.success("Conversion complete!")
                st.download_button(
                    label=f"Download .{st.session_state.converted_format.lower()}",
                    data=st.session_state.converted_bytes,
                    file_name=st.session_state.download_file_name,
                    mime=f"image/{st.session_state.converted_format.lower()}",
                    width="stretch"
                )

# --- Footer Info Card ---
st.markdown(f"""
    <div class="feature-card">
        <div class="feature-title">Fast, Private & Free Image Conversions</div>
        <ul class="feature-list">
            <li><strong>100% In-Memory Processing:</strong> Your images are processed instantly without being saved permanently.</li>
            <li><strong>Multiple Formats:</strong> Convert seamlessly between PNG, JPEG, WEBP, BMP, and TIFF.</li>
            <li><strong>No Software Required:</strong> Works directly in your browser across mobile and desktop.</li>
        </ul>
    </div>
""", unsafe_allow_html=True)
