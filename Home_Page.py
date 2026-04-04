import webbrowser
import sys

#! --- REDIRECT JIKA TIDAK PUNYA STREAMLIT ATAU RUN TANPA STREAMLIT ---
def redirect_to_web():
    print("🚀 Library Streamlit tidak ditemukan atau dijalankan sebagai script biasa.")
    print("Mengarahkan ke: https://matkul-semester4-maliq.streamlit.app/")
    webbrowser.open("https://matkul-semester4-maliq.streamlit.app/Keamanan_Data")
    sys.exit()

try:
    import streamlit as st
    if not st.runtime.exists():
        redirect_to_web()
except ImportError:
    redirect_to_web()

st.set_page_config(
    page_title="Main Page",
    page_icon="assets/logo.webp",
)

st.logo("assets/LOGO_UNESA.png")

with st.sidebar:    
    st.title("🎓 Learning Dashboard")
    st.markdown("""
    <div style="display: grid; grid-template-columns: 60px auto; gap: 5px; margin-bottom: 1rem;">
        <div>Nama</div><div>: <b>Maliq Rafaldo</b></div>
        <div>NIM</div><div>: <b>24051204132</b></div>
        <div>Kelas</div><div>: <b>TI 2024 D</b></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()

st.write("# Welcome to Streamlit! 👋")

st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)