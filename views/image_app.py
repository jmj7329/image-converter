with st.popover("☰"):
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("views/home.py")
    st.link_button("1. Go to Google", "https://www.google.com", use_container_width=True)
    st.link_button("2. Go to GitHub", "https://github.com", use_container_width=True)
