import streamlit as st
import os
import sys
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent))

from modules.auth import login_page, register_page
from modules.database import init_database

# Set page config
st.set_page_config(
    page_title="GUESS IT - Chatbot Game",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
init_database()

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.user_id = None

# CSS styling
st.markdown("""
    <style>
    :root {
        --primary-color: #FF1493;
        --secondary-color: #9370DB;
        --background: #1a0033;
        --text-color: #ffffff;
    }
    
    .main {
        background: linear-gradient(135deg, #1a0033 0%, #2d0052 100%);
        color: #ffffff;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #FF1493, #FF69B4);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 10px 30px;
        font-weight: bold;
    }
    
    .stButton>button:hover {
        background: linear-gradient(90deg, #FF69B4, #FFB6D9);
    }
    
    .welcome-card {
        background: linear-gradient(135deg, #FF1493, #9370DB);
        padding: 30px;
        border-radius: 15px;
        color: white;
        margin: 20px 0;
    }
    
    </style>
""", unsafe_allow_html=True)

def main():
    if not st.session_state.authenticated:
        # Show login/register page
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("<h1 style='text-align: center; color: #FF1493;'>🤖 GUESS IT</h1>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center; color: #9370DB;'>Chatbot Guessing Game</h3>", unsafe_allow_html=True)
            
            tab1, tab2 = st.tabs(["Login", "Register"])
            
            with tab1:
                login_page()
            
            with tab2:
                register_page()
    else:
        # Show authenticated pages (handled by Streamlit multi-page app)
        st.sidebar.title(f"Hi, {st.session_state.username}! 🎮")
        
        if st.sidebar.button("Logout", key="logout_btn"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.user_id = None
            st.rerun()

if __name__ == "__main__":
    main()
