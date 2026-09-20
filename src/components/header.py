import streamlit as st
import base64

def header_home():
    with open("attendex_logo_v2.png", "rb") as f:
        logo = base64.b64encode(f.read()).decode()

    st.markdown(f"""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom: 30px;">
            <img src="data:image/png;base64,{logo}" width="600" height="200">
        </div>
    """, unsafe_allow_html=True)

def header_dashboard():
    with open("attendex_logo_v2.png", "rb") as f:
        logo = base64.b64encode(f.read()).decode()

    st.markdown(f"""
        <div style="display:flex;  align-items:center; justify-content:center; margin-bottom: 30px;">
            <img src="data:image/png;base64,{logo}" height="100px;">
        </div>
    """, unsafe_allow_html=True)


