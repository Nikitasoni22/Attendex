import streamlit as st
from src.components.header import header_home
from src.ui.base_layout import style_background_home
from src.ui.base_layout import style_base_layout
from src.components.footer import footer
def home_screen():
    header_home()
    style_background_home()
    style_base_layout()

    col1,col2=st.columns(2,gap="large")

    with col1:
        st.header("I'm Teacher")
        st.image("search_image.png",width=150)
        if st.button('Teacher portal',type='primary',icon=':material/arrow_outward:',icon_position='right'):
            st.session_state['login_type']='teacher'
            st.rerun()

    with col2:
        st.header("I'm Student")
        st.image("thinking_image.png",width=155)
        if st.button('Student portal',type='secondary',icon=':material/arrow_outward:',icon_position='right'):
            st.session_state['login_type']='student'
            st.rerun()


    footer()