import streamlit as st
import time
from modules.game_logic import game_logic
from modules.database import update_user_profile, get_user

st.set_page_config(page_title="Game - GUESS IT", layout="wide")

# CSS
st.markdown("""
    <style>
    .game-container {
        background: linear-gradient(135deg, #FF1493, #9370DB);
        padding: 30px;
        border-radius: 15px;
        color: white;
        margin: 20px 0;
    }
    .stat-box {
        background: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

def check_authentication():
    if not st.session_state.get("authenticated"):
        st.warning("Silakan login terlebih dahulu!")
        st.stop()

check_authentication()

# Page header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(f"<h1 style='text-align: center; color: #FF1493;'>🎮 GAME</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #9370DB;'>Hi, {st.session_state.username}!</p>", unsafe_allow_html=True)

# Navigation
st.markdown("---")
st.subheader("Pilih Game")

game_col1, game_col2, game_col3 = st.columns(3)

with game_col1:
    if st.button("🖼️ TEBAK GAMBAR", use_container_width=True, key="guess_image_btn"):
        st.session_state.current_game = "guess_image"
        st.rerun()

with game_col2:
    if st.button("🔤 SAMBUNG KATA", use_container_width=True, key="guess_word_btn"):
        st.session_state.current_game = "guess_word"
        st.rerun()

with game_col3:
    if st.button("💬 CHAT BOT", use_container_width=True, key="chat_bot_btn"):
        st.session_state.current_game = "chat_bot"
        st.rerun()

# Game logic
if "current_game" in st.session_state:
    game_type = st.session_state.current_game
    
    st.markdown("---")
    
    if game_type == "guess_image":
        st.subheader("🖼️ Tebak Gambar")
        
        if "game_data" not in st.session_state or st.session_state.game_type != game_type:
            st.session_state.game_data = game_logic.get_random_game("guess_image")
            st.session_state.start_time = time.time()
            st.session_state.game_type = game_type
        
        game = st.session_state.game_data
        
        # Display stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='stat-box'>⭐ <br> <b>+50</b> Poin</div>", unsafe_allow_html=True)
        with col2:
            elapsed = int(time.time() - st.session_state.start_time)
            st.markdown(f"<div class='stat-box'>⏱️ <br> <b>{elapsed}s</b></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='stat-box'>❤️ <br> <b>3/3</b> Nyawa</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Display image
        st.markdown(f"<h2 style='text-align: center; font-size: 100px;'>{game['image']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #9370DB;'>Petunjuk: {game['hint']}</p>", unsafe_allow_html=True)
        
        # Answer input
        answer = st.text_input("Jawaban Anda:", placeholder="Ketik jawaban di sini")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ SUBMIT", use_container_width=True):
                if game_logic.check_answer("guess_image", answer, game['answer']):
                    st.success("🎉 Jawaban Benar!")
                    elapsed = time.time() - st.session_state.start_time
                    points = game_logic.calculate_points("guess_image", elapsed)
                    
                    # Update user points
                    user = get_user(st.session_state.username)
                    new_points = user.get('points', 0) + points
                    new_level = max(1, new_points // 1000 + 1)
                    update_user_profile(st.session_state.username, {
                        'points': new_points,
                        'level': new_level,
                        'total_plays': user.get('total_plays', 0) + 1
                    })
                    
                    st.info(f"Anda mendapatkan **{points}** poin! 🏆")
                    time.sleep(2)
                    del st.session_state.game_data
                    st.rerun()
                else:
                    st.error(f"❌ Jawaban Salah! Jawaban yang benar adalah: **{game['answer']}**")
        
        with col2:
            if st.button("⏭️ SKIP", use_container_width=True):
                del st.session_state.game_data
                st.rerun()
    
    elif game_type == "guess_word":
        st.subheader("🔤 Sambung Kata")
        
        if "game_data" not in st.session_state or st.session_state.game_type != game_type:
            st.session_state.game_data = game_logic.get_random_game("guess_word")
            st.session_state.start_time = time.time()
            st.session_state.game_type = game_type
        
        game = st.session_state.game_data
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='stat-box'>⭐ <br> <b>+80</b> Poin</div>", unsafe_allow_html=True)
        with col2:
            elapsed = int(time.time() - st.session_state.start_time)
            st.markdown(f"<div class='stat-box'>⏱️ <br> <b>{elapsed}s</b></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='stat-box'>❤️ <br> <b>3/3</b> Nyawa</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown(f"<h2 style='text-align: center; color: #FF1493;'>{game['word']} → ?</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #9370DB;'>Petunjuk: {game['hint']}</p>", unsafe_allow_html=True)
        
        answer = st.text_input("Sambung dengan kata:", placeholder="Ketik kata selanjutnya")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ SUBMIT", use_container_width=True, key="submit_word"):
                if game_logic.check_answer("guess_word", answer, game['answer']):
                    st.success("🎉 Jawaban Benar!")
                    elapsed = time.time() - st.session_state.start_time
                    points = game_logic.calculate_points("guess_word", elapsed)
                    
                    user = get_user(st.session_state.username)
                    new_points = user.get('points', 0) + points
                    new_level = max(1, new_points // 1000 + 1)
                    update_user_profile(st.session_state.username, {
                        'points': new_points,
                        'level': new_level,
                        'total_plays': user.get('total_plays', 0) + 1
                    })
                    
                    st.info(f"Anda mendapatkan **{points}** poin! 🏆")
                    time.sleep(2)
                    del st.session_state.game_data
                    st.rerun()
                else:
                    st.error(f"❌ Jawaban Salah! Jawaban yang benar adalah: **{game['answer']}**")
        
        with col2:
            if st.button("⏭️ SKIP", use_container_width=True, key="skip_word"):
                del st.session_state.game_data
                st.rerun()
    
    elif game_type == "chat_bot":
        st.subheader("💬 Chat Bot Quiz")
        
        if "game_data" not in st.session_state or st.session_state.game_type != game_type:
            st.session_state.game_data = game_logic.get_random_game("chat_bot")
            st.session_state.game_type = game_type
        
        game = st.session_state.game_data
        
        st.markdown(f"<h3 style='color: #FF1493;'>{game['question']}</h3>", unsafe_allow_html=True)
        
        answer = st.text_input("Jawaban Anda:", placeholder="Ketik jawaban")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ SUBMIT", use_container_width=True, key="submit_chat"):
                if game_logic.check_answer("chat_bot", answer, game['answer']):
                    st.success("🎉 Jawaban Benar!")
                    
                    user = get_user(st.session_state.username)
                    new_points = user.get('points', 0) + game['points']
                    new_level = max(1, new_points // 1000 + 1)
                    update_user_profile(st.session_state.username, {
                        'points': new_points,
                        'level': new_level,
                        'total_plays': user.get('total_plays', 0) + 1
                    })
                    
                    st.info(f"Anda mendapatkan **{game['points']}** poin! 🏆")
                    time.sleep(2)
                    del st.session_state.game_data
                    st.rerun()
                else:
                    st.error(f"❌ Jawaban Salah! Jawaban yang benar adalah: **{game['answer']}**")
        
        with col2:
            if st.button("⏭️ SKIP", use_container_width=True, key="skip_chat"):
                del st.session_state.game_data
                st.rerun()
