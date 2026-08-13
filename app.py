import streamlit as st
from PIL import Image
import io
import os

# 1. Page Configuration
st.set_page_config(
    page_title="Image Converter", 
    page_icon="🖼️", 
    layout="centered"
)

# --- Session State Initialization ---
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0
# Add a state to hold the uploaded file object itself
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

# --- Theme Toggle ---
top_col1, top_col2 = st.columns([4, 1])
with top_col2:
    dark_mode = st.toggle("🌙 Dark", value=False)

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
else:
    bg_gradient = "linear-gradient(180deg, #e8f0fe 0%, #ffffff 220px, #ffffff 100%)"
    text_color = "#1e293b"
    sub_color = "#64748b"
    card_bg = "#f8fafc"
    card_border = "#e2e8f0"
    uploader_bg = "#f8fafc"
    uploader_border = "#cbd5e1"
    input_bg = "#ffffff"
    btn_sec_bg = "#f1f5f9"
    btn_sec_text = "#475569"
    btn_sec_border = "#cbd5e1"

# 2. Inject Custom CSS
st.markdown(f"""
    <style>
    /* Global Page Background Gradient */
    .stApp {{
        background: {bg_gradient};
    }}

    /* Title & Subtitle styling */
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

    /* Dark/Light Mode Toggle Label Visibility */
    div[data-testid="stWidgetLabel"] p,
    label[data-testid="stWidgetLabel"] span {{
        color: {text_color} !important;
        font-weight: 600 !important;
        opacity: 1 !important;
    }}

    /* FORCE BLACK TEXT IN GREEN CONVERSION COMPLETE (ST.SUCCESS) BOX */
    div[data-testid="stAlert"] *,
    div[data-testid="stAlert"] p,
    div[data-testid="stAlert"] span {{
        color: #000000 !important;
        font-weight: 600 !important;
    }}

    /* Outer Dashed Drop Box Container */
    div[data-testid="stFileUploader"] {{
        background-color: {uploader_bg} !important;
        border: 2px dashed {uploader_border} !important;
        border-radius: 16px !important;
        padding: 35px 20px !important;
    }}

    /* ALWAYS FORCE DROPZONE CONTAINER TO STAY VISIBLE */
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

    /* COMPLETELY REMOVE STREAMLIT'S UPLOADED FILE PILL WIDGET & BADGES */
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

    /* Centered Square Upload Button styling */
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

    /* File limits text */
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

    /* Custom File Name Title Above Image */
    .file-preview-title {{
        color: {sub_color} !important;
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 8px;
        word-break: break-all;
    }}

    /* Dropdown / Selectbox Styling */
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

    /* Primary Action Button (Convert) */
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

    /* Secondary Action Button (Remove File) */
    button[kind="secondary"] {{
        background-color: {btn_sec_bg} !important;
        color: {btn_sec_text} !important;
        border: 1px solid {btn_sec_border} !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }}

    /* Feature info card */
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
    /* Preview Image Styling */
    div[data-testid="stImage"] img {{
        border: 2px solid {card_border} !important;
        border-radius: 12px !important;
        padding: 4px !important; /* Optional: adds a slight gap between image and border */
        background-color: {card_bg} !important; /* Matches your theme */
    }}
    </style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown('<h1 class="title-text">Image Converter</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Convert images online, for free.</p>', unsafe_allow_html=True)

# --- Drag & Drop Upload Zone ---
uploader_placeholder = st.empty()
terms_placeholder = st.empty()

# Only show the uploader if there is no file in session state
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
    
    # When a file is selected via the widget, save it to session state and rerun
    if uploaded_file is not None:
        st.session_state.persisted_file = uploaded_file
        st.rerun()

# --- Converter Logic ---
# Base everything off the persisted_file in session_state, not the widget directly
if st.session_state.persisted_file is not None:
    
    # Hide the uploader and terms by completely clearing their placeholders
    uploader_placeholder.empty()
    terms_placeholder.empty()

    # Get the file from session state
    working_file = st.session_state.persisted_file

    # Reset conversion state if a brand new file is uploaded
    if st.session_state.current_file_name != working_file.name:
        st.session_state.current_file_name = working_file.name
        st.session_state.converted_bytes = None
        st.session_state.converted_format = None
        st.session_state.download_file_name = None

    st.divider()
    image = Image.open(working_file)
    
    file_ext = working_file.name.split('.')[-1].upper()
    if file_ext == "JPG":
        file_ext = "JPEG"
    elif file_ext == "TIF":
        file_ext = "TIFF"

    all_formats = ["PNG", "JPEG", "WEBP", "BMP", "TIFF"]
    available_formats = [fmt for fmt in all_formats if fmt != file_ext]
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown(
            f'<div class="file-preview-title">{working_file.name}</div>', 
            unsafe_allow_html=True
        )
        st.image(image, width="stretch")
        
    with col2:
        st.markdown('<div style="height: 32px;"></div>', unsafe_allow_html=True)

        if st.button("✕ Remove File", width="stretch", type="secondary"):
            # Clean up EVERYTHING to return to the original upload state
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
        
        if st.button("Convert File", width="stretch", type="primary"):
            buffer = io.BytesIO()
            img_to_save = image.copy()
            
            if target_format in ["JPEG", "JPG"] and img_to_save.mode in ("RGBA", "P"):
                img_to_save = img_to_save.convert("RGB")
                
            img_to_save.save(buffer, format=target_format)
            
            # Custom filename processing logic
            master_string = os.path.splitext(working_file.name)[0]
                
            # Store in session_state to persist across dark/light mode toggles
            st.session_state.converted_bytes = buffer.getvalue()
            st.session_state.converted_format = target_format
            st.session_state.download_file_name = f"converted-{master_string}.{target_format.lower()}"

        # Persistent Display of Download Button
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