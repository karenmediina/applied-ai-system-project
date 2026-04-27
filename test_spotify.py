import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

try:
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Search for "Un Ratito"
    query = "track:Un Ratito artist:Bad Bunny"
    results = sp.search(q=query, limit=1, type='track')

    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        artist_id = track['artists'][0]['id']
        
        # We fetch artist info safely
        artist_info = sp.artist(artist_id)
        
        print(f"--- Found: {track['name']} by {track['artists'][0]['name']} ---")
        
        # SAFE ACCESS: Use .get() so it doesn't crash if the key is missing
        pop = track.get('popularity', 'N/A (Restricted by Spotify)')
        genres = artist_info.get('genres', [])
        
        print(f"Popularity: {pop}")
        
        if genres:
            print(f"Genres: {', '.join(genres)}")
        else:
            print("Genres: No public genre data found.")
            
        # Album Art is usually still public!
        if track.get('album', {}).get('images'):
            print(f"Album Art: {track['album']['images'][0]['url']}")
            
    else:
        print("Song not found!")

except Exception as e:
    print(f"--- Connection Error ---\n{e}")