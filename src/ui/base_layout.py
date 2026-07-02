import streamlit as st


def style_background_home():
    st.markdown("""
        <style>
            .stApp {
                background: #F8FAFC !important;
            }
            .stApp div[data-testid="stColumn"] {
                background-color: #ffffff !important;
                padding: 2.5rem !important;
                border-radius: 5rem !important;
                box-shadow: 0 4px 24px rgba(88,101,242,0.10) !important;
            }
        </style>
    """, unsafe_allow_html=True)


def style_background_dashboard():
    st.markdown("""
        <style>
            .stApp {
                background: #F8FAFC !important;
            }
        </style>
    """, unsafe_allow_html=True)


def style_base_layout():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

        #MainMenu, footer, header {
            visibility: hidden;
        }

        .block-container {
            padding-top: 1.5rem !important;
        }

        h1 {
            font-family: 'Sora', sans-serif !important;
            font-weight: 800 !important;
            font-size: 3rem !important;
            line-height: 1.1 !important;
            margin-bottom: 0rem !important;
            color: #1e1b4b !important;
        }

        h2 {
            font-family: 'Sora', sans-serif !important;
            font-weight: 700 !important;
            font-size: 1.8rem !important;
            line-height: 1.1 !important;
            margin-bottom: 0rem !important;
            color: #1e1b4b !important;
        }

        h3 {
            font-family: 'Outfit', sans-serif;
            color: #1e293b !important;
        }

        h4, p {
            font-family: 'Outfit', sans-serif;
            color: #334155 !important;
        }

        /* Input fields — white bg, dark text */
        .stTextInput > div > div > input {
            background-color: #ffffff !important;
            color: #1e293b !important;
            border: none !important;
            border-radius: 0.75rem !important;
            font-family: 'Outfit', sans-serif !important;
            font-size: 1rem !important;
            padding: 0.6rem 1rem !important;
            box-shadow: 0 1px 4px rgba(0,0,0,0.10) !important;
        }

        .stTextInput > div > div > input:focus {
            border: none !important;
            box-shadow: 0 0 0 3px #5865F240 !important;
            outline: none !important;
        }

        .stTextInput > label {
            color: #475569 !important;
            font-family: 'Outfit', sans-serif !important;
            font-size: 0.9rem !important;
            font-weight: 600 !important;
        }

        /* Selectbox */
        .stSelectbox > div > div {
            background-color: #ffffff !important;
            color: #1e293b !important;
            border: none !important;
            border-radius: 0.75rem !important;
            box-shadow: none !important;
        }

        .stSelectbox > label {
            color: #475569 !important;
            font-family: 'Outfit', sans-serif !important;
            font-size: 0.9rem !important;
            font-weight: 600 !important;
        }

        /* Buttons */
        button {
            border-radius: 1.5rem !important;
            background-color: #5865F2 !important;
            color: white !important;
            padding: 10px 20px !important;
            border: none !important;
            transition: transform 0.25s ease-in-out !important;
            font-family: 'Outfit', sans-serif !important;
            font-weight: 600 !important;
        }

        button[kind="secondary"] {
            border-radius: 1.5rem !important;
            background-color: #EB459E !important;
            color: white !important;
            padding: 10px 20px !important;
            border: none !important;
            transition: transform 0.25s ease-in-out !important;
        }

        button[kind="tertiary"] {
            border-radius: 1.5rem !important;
            background-color: #dde1ff !important;
            color: #1e1b4b !important;
            padding: 10px 20px !important;
            border: none !important;
            transition: transform 0.25s ease-in-out !important;
        }

        button:hover {
            transform: scale(1.03);
        }

        /* Dataframe toolbar — reset global button override */
        div[data-testid="stDataFrame"] button,
        div[data-testid="stDataFrameToolbarContainer"] button,
        div[class*="toolbar"] button {
            background-color: transparent !important;
            color: #475569 !important;
            border-radius: 0.4rem !important;
            padding: 4px 8px !important;
            box-shadow: none !important;
            min-width: unset !important;
            border: 1px solid #e2e8f0 !important;
        }

        div[data-testid="stDataFrame"] button:hover,
        div[data-testid="stDataFrameToolbarContainer"] button:hover {
            background-color: #f1f5f9 !important;
            transform: none !important;
        }

        /* Alerts — full width, centered text */
        div[data-testid="stAlert"] {
            width: 100% !important;
            text-align: center !important;
        }

        div[data-testid="stAlert"] p {
            text-align: center !important;
        }

        /* Remove ALL internal borders/separators inside text inputs */
        div[data-testid="stTextInput"] *,
        div[data-testid="stTextInput"] *::before,
        div[data-testid="stTextInput"] *::after {
            border-left: none !important;
            border-right: none !important;
            outline: none !important;
        }

        /* Password visibility toggle — icon only, no pill */
        div[data-testid="stTextInput"] button {
            background-color: transparent !important;
            color: #94a3b8 !important;
            border-radius: 0.4rem !important;
            padding: 2px 4px !important;
            box-shadow: none !important;
            border: none !important;
            min-width: unset !important;
            width: auto !important;
        }

        div[data-testid="stTextInput"] button:hover {
            background-color: transparent !important;
            color: #5865F2 !important;
            transform: none !important;
        }

        /* Hide browser native password reveal + autofill icons */
        input[type="password"]::-ms-reveal,
        input[type="password"]::-ms-clear,
        input::-webkit-credentials-auto-fill-button,
        input::-webkit-contacts-auto-fill-button {
            display: none !important;
            visibility: hidden !important;
        }

        /* Hide "Press Enter to apply" tooltip */
        small[data-testid="InputInstructions"],
        div[data-testid="InputInstructions"],
        [data-testid="stTextInput"] small,
        .stTextInput small {
            display: none !important;
            visibility: hidden !important;
        }

        /* Dialog close (X) button — keep neutral, not indigo pill */
        div[data-testid="stDialog"] button[aria-label="Close"] {
            background-color: transparent !important;
            color: #475569 !important;
            border-radius: 0.5rem !important;
            padding: 4px !important;
        }

        div[data-testid="stDialog"] button[aria-label="Close"]:hover {
            background-color: #eef2ff !important;
            transform: none !important;
        }

        div[data-testid="stDialog"] button[aria-label="Close"] svg {
            fill: #475569 !important;
        }
        </style>
    """, unsafe_allow_html=True)


def form_card(content_fn):
    """Render content inside a white card for forms."""
    st.markdown("""
        <div style="
            background: white;
            border-radius: 1.5rem;
            padding: 2.5rem 2rem;
            box-shadow: 0 4px 24px #5865F215;
            margin: 1rem 0;
        ">
    """, unsafe_allow_html=True)
    content_fn()
    st.markdown("</div>", unsafe_allow_html=True)
