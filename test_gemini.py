import os
from dotenv import load_dotenv
from google import genai

# 1. Setup
load_dotenv()
# Using the key from your .env
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 2. Define the "Music Expert" Prompt
song_name = "Un Ratito"
artist = "Bad Bunny"

prompt = f"""
I'm building a music recommender. Spotify's API is restricted, so I need your expertise.
For the song '{song_name}' by '{artist}', please provide:
1. A brief 1-sentence 'vibe' description.
2. Three specific 'Audio Features' estimates (Energy, Danceability, Mood) on a scale of 0.0 to 1.0.
3. 2 similar songs that a fan of this track would like.
"""

# 3. Generate content
try:
    # 'gemini-2.5-flash' is the stable current workhorse for the free API
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=prompt
    )
    print("--- Gemini 2.5 Analysis ---")
    print(response.text)
except Exception as e:
    print(f"--- Connection Failed ---\nError: {e}")