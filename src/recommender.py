import os
from google import genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class MusicRecommender:
    def __init__(self):
        # Initialize Gemini and Spotify
        self.ai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        auth_manager = SpotifyClientCredentials(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
        )
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

    def get_recommendation(self, user_mood):
        # Structured prompt for consistent parsing
        prompt = f"""
        User Mood: "{user_mood}"
        Recommend 3 specific songs. For each, provide a 1-sentence explanation of why it fits.
        Format: Song Name | Artist | Reasoning
        Return ONLY the list. Do not include introductory text.
        """
        
        recommendations = []
        try:
            ai_resp = self.ai_client.models.generate_content(
                model="gemini-2.5-flash-lite", 
                contents=prompt
            )


            # Extract text safely
            response_text = ai_resp.text if hasattr(ai_resp, 'text') else str(ai_resp)
            raw_lines = response_text.strip().split('\n')

            for line in raw_lines:
                # Handle different bullet point styles and extract components
                clean_line = line.strip().lstrip('0123456789.-* ').strip()
                
                # Split by pipe, but handle fallback delimiters
                if "|" in clean_line:
                    parts = clean_line.split("|")
                elif " - " in clean_line:
                    parts = clean_line.split(" - ")
                else:
                    continue

                if len(parts) >= 2:
                    song_name = parts[0].strip().replace('"', '').replace("'", "")
                    artist_name = parts[1].strip().replace('"', '').replace("'", "")
                    # Assign reasoning or provide a fallback
                    reasoning = parts[2].strip() if len(parts) > 2 else "This track perfectly matches the requested aesthetic."
                    
                    # Search Spotify for the specific track
                    search_query = f"{song_name} {artist_name}"
                    
                    if len(recommendations) < 3:
                        results = self.sp.search(q=search_query, limit=1, type='track')
                        if results['tracks']['items']:
                            track = results['tracks']['items'][0]
                            recommendations.append({
                                "name": track['name'],
                                "artist": track['artists'][0]['name'],
                                "image": track['album']['images'][0]['url'],
                                "url": track['external_urls']['spotify'],
                                "reason": reasoning
                            })
            
            return recommendations
            
        except Exception as e:
            print(f"DEBUG System Error: {e}")
            return []