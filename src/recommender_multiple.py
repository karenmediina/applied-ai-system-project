import os
from google import genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class MusicRecommender:
    def __init__(self):
        self.ai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        auth_manager = SpotifyClientCredentials(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
        )
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

    def get_recommendation(self, user_mood):
        prompt = f"User Mood: {user_mood}. Recommend 3 songs. Format: Song, Artist. Return only the list."
        
        # Initialize as an empty list ALWAYS
        recommendations = []
        
        try:
            ai_resp = self.ai_client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=prompt
            )
            
            if not ai_resp.text:
                print("DEBUG: Gemini returned empty response.")
                return []
            

            raw_lines = ai_resp.text.strip().split('\n')
            print(f"DEBUG: Gemini Raw Response:\n{ai_resp.text}\n--- End of Gemini Response ---")

            for line in raw_lines:
                clean_line = line.strip().lstrip('0123456789.-* ').strip()
                print(f"DEBUG: Processing line: '{line}' -> Cleaned: '{clean_line}'")
                if not clean_line or len(clean_line) < 3:
                    continue
                
                if len(recommendations) < 3:
                    results = self.sp.search(q=clean_line, limit=1, type='track')
                    if results['tracks']['items']:
                        track = results['tracks']['items'][0]
                        recommendations.append({
                            "name": track['name'],
                            "artist": track['artists'][0]['name'],
                            "image": track['album']['images'][0]['url'],
                            "url": track['external_urls']['spotify']
                        })
            
            return recommendations # Returns list of dicts
            
        except Exception as e:
            print(f"DEBUG: System Error: {e}")
            return [] # Returns empty list on failure