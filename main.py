import streamlit as st

# Configure pages and set explicit URL subpaths
home_page = st.Page(
    "views/home.py", 
    title="Home", 
    icon="🌐", 
    default=True
)

image_page = st.Page(
    "views/image_app.py", 
    title="Image Converter", 
    icon="🖼️", 
    url_path="image"  # Creates the /image URL path
)

# Initialize navigation (hidden sidebar if you want full custom UI control)
pg = st.navigation([home_page, image_page], position="hidden")
pg.run()
