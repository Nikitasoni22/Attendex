import streamlit as st


def style_background_home():
    st.markdown(
        """
        <style>
        .stApp {
            background: #DCE2F7 !important;
        }

        /* Cards */
        .stApp div[data-testid="stColumn"] {
            background: #EEF1FC !important;
            border-radius: 5rem !important;
            padding: 2.5rem 2rem !important;

            /* Make everything inside the card centered */
            text-align: center !important;
        }

        /* Center images */
        .stApp div[data-testid="stColumn"] img {
            display: block !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }

        /* Center buttons */
        .stApp div[data-testid="stColumn"] div[data-testid="stButton"] {
            display: flex !important;
            justify-content: center !important;
        }

        /* Center the button itself */
        .stApp div[data-testid="stColumn"] div[data-testid="stButton"] button {
            margin-left: auto !important;
            margin-right: auto !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def style_background_dashboard():
    st.markdown(
        """
        <style>
        .stApp {
            background: #CFD7F2 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def style_base_layout():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Sora:wght@100..800&display=swap');

        @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&family=Roboto:ital,wght@0,100..900;1,100..900&family=Sora:wght@100..800&display=swap');

        /* Main Streamlit heading */
        h2 {
            font-family: 'Sora', sans-serif !important;
            font-size: 36px !important;
            font-weight: 800 !important;
            line-height: 1.1 !important;
            margin-bottom: 0 !important;
            color:#1E2130 !important;
        }

        h3,h4,p{
            font-family:'Roboto', sans-serif !important;
        }

/* Default / primary buttons */
button[kind="primary"] {
    background: #3B4CCA !important;
    border-radius: 1.5rem !important;
    color: white !important;
    padding: 10px 20px !important;
    border: none !important;
}

/* Secondary buttons */
button[kind="secondary"] {
    background: #2EC4B6 !important;
    border-radius: 1.5rem !important;
    color: white !important;
    padding: 10px 20px !important;
    border: none !important;
}

/* Tertiary buttons */
button[kind="tertiary"] {
    background: #FF6B35 !important;
    border-radius: 1.5rem !important;
    color: white !important;
    padding: 10px 20px !important;
    border: none !important;
}

button:hover{
transform:scale(1.05)
}

        /* Hide Streamlit UI */
        #MainMenu,
        footer,
        header {
            visibility: hidden;
        }

        .block-container {
            padding-top: 1.5rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )