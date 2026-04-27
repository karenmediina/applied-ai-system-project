import os
from google import genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class MusicRecommender:
    def __init__(self):
        # Setup Gemini
        self.ai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
        # Setup Spotify
        auth_manager = SpotifyClientCredentials(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
        )
        self.sp = spotipy.Spotify(auth_manager=auth_manager)
        
    def get_recommendation_onesong(self, user_mood):
        # 1. Ask Gemini for a recommendation based on the mood
        prompt = f"""
        The user said: "{user_mood}"
        
        As a music expert, identify the core intent. 
        If they mentioned a specific artist or song, lean into that. 
        Otherwise, find a track that matches the atmospheric vibe.
        
        Return only: Song Name, Artist
        """
        # prompt = f"The user is feeling: {user_mood}. Recommend one perfect song. Provide the song name and artist only, separated by a comma."
        ai_resp = self.ai_client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        
        # 2. Parse the result (e.g., "Ojitos Lindos, Bad Bunny")
        recommendation_text = ai_resp.text.strip()
        
        # 3. Use Spotify to get the "Visuals" and "Metadata"
        results = self.sp.search(q=recommendation_text, limit=1, type='track')
        
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            return {
                "name": track['name'],
                "artist": track['artists'][0]['name'],
                "image": track['album']['images'][0]['url'],
                "url": track['external_urls']['spotify'],
                "reason": f"Because you're feeling {user_mood}, this track fits the vibe perfectly."
            }
        return None