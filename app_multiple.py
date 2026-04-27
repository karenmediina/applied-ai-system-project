import streamlit as st
from src.recommender import MusicRecommender
from dotenv import load_dotenv

# Page Config
st.set_page_config(page_title="VibeCheck AI", page_icon="🎵", layout="wide")
load_dotenv()

# Initialize Engine
@st.cache_resource
def load_engine():
    return MusicRecommender()

engine = load_engine()

# UI Layout
st.title("🎵 DJ Vi")
st.markdown("---")

user_mood = st.text_input("How are you feeling?", placeholder="e.g., Dreaming of an Italian Summer...")

if st.button("Get Vibe"):
    if user_mood:
        with st.spinner("The Oracle is searching the archives..."):
            results = engine.get_recommendation(user_mood)

            # Check if we got a valid list with items
            if isinstance(results, list) and len(results) > 0:
                st.markdown("### Your Top 3 Tracks:")
                cols = st.columns(3)
                
                for idx, song in enumerate(results):
                    # Final safety check to ensure 'song' is a dictionary
                    if isinstance(song, dict):
                        with cols[idx]:
                            st.image(song['image'], use_container_width=True)
                            st.subheader(song['name'])
                            st.write(f"by {song['artist']}")
                            st.link_button("Listen on Spotify", song['url'])
            else:
                # This catches empty lists OR non-list returns
                st.error("The Oracle is silent. Try a different mood or check your terminal for errors.")
    else:
        st.warning("Tell me a vibe first!")

# Symbolic Systems Debugger
st.markdown("---")
with st.expander("🔍 System Logic (Debug Mode)"):
    st.write("**Architecture:** RAG (Retrieval-Augmented Generation)")
    st.write("**Reasoner:** Gemini 2.5 Flash")
    st.write("**Retriever:** Spotify Web API")
    st.caption("Verification: AI identifies the song; Spotify provides the ground-truth metadata.")