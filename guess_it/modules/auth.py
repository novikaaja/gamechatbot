import streamlit as st
import json
import hashlib
from pathlib import Path
from datetime import datetime
from modules.database import get_user, create_user, update_user_profile

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def login_page():
    """Login page"""
    st.subheader("🔐 Login")
    
    col1, col2 = st.columns(2)
    
    with col1:
        username = st.text_input("Username", placeholder="Masukkan username")
        password = st.text_input("Password", type="password", placeholder="Masukkan password")
        
        if st.button("LOGIN", use_container_width=True, key="login_btn"):
            if not username or not password:
                st.error("Username dan password harus diisi!")
            else:
                user = get_user(username)
                if user and user['password'] == hash_password(password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.user_id = user['user_id']
                    st.success("Login berhasil! 🎉")
                    st.rerun()
                else:
                    st.error("Username atau password salah!")
        
        st.markdown("---")
        st.markdown("**Belum punya akun?** Daftar di tab Register →")

def register_page():
    """Register page"""
    st.subheader("📝 Register")
    
    col1, col2 = st.columns(2)
    
    with col1:
        username = st.text_input("Username", placeholder="Masukkan username", key="reg_username")
        email = st.text_input("Email", placeholder="Masukkan email", key="reg_email")
        password = st.text_input("Password", type="password", placeholder="Masukkan password", key="reg_password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Konfirmasi password", key="reg_confirm")
        
        if st.button("REGISTER", use_container_width=True, key="register_btn"):
            if not all([username, email, password, confirm_password]):
                st.error("Semua field harus diisi!")
            elif password != confirm_password:
                st.error("Password dan konfirmasi password tidak cocok!")
            elif len(password) < 6:
                st.error("Password minimal 6 karakter!")
            else:
                existing_user = get_user(username)
                if existing_user:
                    st.error("Username sudah terdaftar!")
                else:
                    hashed_password = hash_password(password)
                    user_data = {
                        "username": username,
                        "email": email,
                        "password": hashed_password,
                        "created_at": datetime.now().isoformat(),
                        "points": 0,
                        "level": 1,
                        "win_rate": 0,
                        "total_plays": 0,
                        "avatar": "😸"
                    }
                    create_user(user_data)
                    st.success("Registrasi berhasil! Silakan login. ✅")
