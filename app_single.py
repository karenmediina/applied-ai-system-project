import streamlit as st
from src.recommender import MusicRecommender
from dotenv import load_dotenv

# 1. Page Config
st.set_page_config(page_title="VibeCheck AI", page_icon="🎵", layout="centered")
load_dotenv()

# 2. Initialize the "Brain" (Cached so it doesn't reload every time)
@st.cache_resource
def load_engine():
    return MusicRecommender()

engine = load_engine()

# 3. UI Elements
st.title("🎵 VibeCheck AI")
st.subheader("Your personal AI Music Curator")
st.markdown("---")

# User Input
user_mood = st.text_input("How are you feeling right now?", placeholder="e.g. Wistful, energetic, or 'Italian Summer' vibes...")

if st.button("Get Recommendations"):
    if user_mood:
        with st.spinner("Curating your vibe..."):
            results = engine.get_recommendation(user_mood)
            
            # CHECK: Ensure results is a list and not empty
            if results and isinstance(results, list):
                st.markdown("### Your Personalized Vibe:")
                cols = st.columns(len(results)) # Dynamically create columns based on count
                
                for idx, song in enumerate(results):
                    # SAFETY: Double check that 'song' is actually a dictionary
                    if isinstance(song, dict) and 'image' in song:
                        with cols[idx]:
                            st.image(song['image'], use_container_width=True)
                            st.markdown(f"**{song['name']}**")
                            st.caption(song['artist'])
                            st.link_button("Listen", song['url'], use_container_width=True)
            else:
                st.error("The oracle is silent. Try rephrasing your mood!")
                
# if st.button("Get Recommendation"):
#     if user_mood:
#         with st.spinner("Consulting the musical oracle..."):
#             result = engine.get_recommendation(user_mood)
            
#             if result:
#                 st.markdown("### We found your vibe:")
                
#                 # Layout: Image on left, Details on right
#                 col1, col2 = st.columns([1, 2])
                
#                 with col1:
#                     st.image(result['image'], use_container_width=True)
                
#                 with col2:
#                     st.header(result['name'])
#                     st.subheader(f"by {result['artist']}")
#                     st.write(result['reason'])
#                     st.link_button("Listen on Spotify", result['url'])
#             else:
#                 st.error("I couldn't find a song for that mood. Try being more descriptive!")
#     else:
#         st.warning("Please enter a mood first!")

st.markdown("---")
st.caption("Powered by Gemini 3 & Spotify | Created for Applied AI Final Project")