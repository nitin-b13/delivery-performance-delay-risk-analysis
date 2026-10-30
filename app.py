import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(page_title="Delivery Performance & Delay Risk", layout="wide")

html_path = Path(__file__).parent / "dashboard.html"

if html_path.exists():
    components.html(html_path.read_text(encoding="utf-8"), height=3200, scrolling=True)
else:
    st.error("dashboard.html was not found. Upload it to the same folder as app.py in the GitHub repo.")
