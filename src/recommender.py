from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"
    

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads song data from a CSV file, processes it, and returns a list of song dictionaries.

    This function reads a CSV file containing song information, converts string representations
    of numerical values to appropriate float/int types for computational use, and returns a list
    of dictionaries. Each dictionary represents a song with standardized keys.

    Parameters:
    - csv_path (str): The file path to the CSV file containing song data. The CSV should have
      a header row with column names matching the expected song attributes.

    Returns:
    - List[Dict]: A list of dictionaries, where each dictionary contains processed song data
      with the following keys:
        - 'id' (int): Unique identifier for the song.
        - 'title' (str): The song's title.
        - 'artist' (str): The song's artist.
        - 'genre' (str): The song's genre.
        - 'mood' (str): The song's mood.
        - 'energy' (float): Energy level (0.0 to 1.0).
        - 'tempo_bpm' (float): Tempo in beats per minute.
        - 'valence' (float): Valence level (0.0 to 1.0).
        - 'danceability' (float): Danceability level (0.0 to 1.0).
        - 'acousticness' (float): Acousticness level (0.0 to 1.0).

    Raises:
    - FileNotFoundError: If the specified CSV file does not exist.
    - KeyError: If the CSV is missing required columns.
    - ValueError: If numerical data cannot be converted (e.g., non-numeric strings in numerical columns).

    The function prints success messages or error details to the console for debugging purposes.

    Required by src/main.py
    """
    songs_list = []
    
    try:
        with open(csv_path, mode='r', encoding='utf-8') as file:
            # DictReader automatically uses the first row as keys for each dictionary
            reader = csv.DictReader(file)
            
            for row in reader:
                # Convert numerical fields to floats/ints for math operations
                processed_song = {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"])
                }
                songs_list.append(processed_song)
                
        print(f"Successfully loaded {len(songs_list)} songs from {csv_path}.")
        
    except FileNotFoundError:
        print(f"Error: The file at {csv_path} was not found.")
    except KeyError as e:
        print(f"Error: Missing expected column in CSV: {e}")
    except ValueError as e:
        print(f"Error: Could not convert numerical data: {e}")

    return songs_list

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences using a weighted priority system.

    The scoring prioritizes certain attributes over others: Mood (highest priority), followed by BPM,
    Genre, Acousticness, Energy, and Danceability. Each matching or proximate attribute contributes
    points to the total score, and reasons for the score are collected in a list.

    Parameters:
    - user_prefs (Dict): A dictionary containing user preferences with expected keys:
        - 'favorite_mood' (str): The preferred mood (e.g., 'happy', 'sad').
        - 'favorite_genre' (str): The preferred genre (e.g., 'pop', 'rock').
        - 'target_bpm' (float): The target tempo in beats per minute (default 100 if missing).
        - 'target_acousticness' (float): The target acousticness level (0.0 to 1.0, default 0.5).
        - 'target_energy' (float): The target energy level (0.0 to 1.0, default 0.5).
        - 'target_danceability' (float): The target danceability level (0.0 to 1.0, default 0.5).
    - song (Dict): A dictionary representing a song with attributes including:
        - 'mood' (str): The song's mood.
        - 'genre' (str): The song's genre.
        - 'tempo_bpm' (float): The song's tempo in beats per minute.
        - 'acousticness' (float): The song's acousticness level (0.0 to 1.0).
        - 'energy' (float): The song's energy level (0.0 to 1.0).
        - 'danceability' (float): The song's danceability level (0.0 to 1.0).

    Returns:
    - Tuple[float, List[str]]: A tuple containing:
        - score (float): The total computed score for the song (higher is better).
        - reasons (List[str]): A list of strings explaining why points were awarded (e.g., "mood match (+3.0)").

    Scoring Details:
    - Mood match: +3.0 points if exact match.
    - Genre match: +1.5 points if exact match.
    - BPM proximity: Up to +2.0 points based on closeness to target (within 40 BPM window).
    - Acousticness proximity: Up to +1.5 points (only added to reasons if >=1.0).
    - Energy and Danceability: Up to +1.0 point each based on proximity.

    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons = []

    # 1. Mood Match (+3.0 pts) - The Priority
    if song.get('mood') == user_prefs.get('favorite_mood'):
        score += 3.0
        reasons.append(f"mood match (+3.0)")

    # 2. Genre Match (+1.5 pts)
    if song.get('genre') == user_prefs.get('favorite_genre'):
        score += 1.5
        reasons.append(f"genre match (+1.5)")

    # 3. Numerical Proximity: BPM (Max +2.0 pts)
    # Logic: Reward closeness to the target BPM
    target_bpm = user_prefs.get('target_bpm', 100)
    actual_bpm = song.get('tempo_bpm', 100)
    # We use a 40-BPM window for scoring; anything further than 40 BPM away gets 0 points
    bpm_proximity = max(0, 1 - (abs(target_bpm - actual_bpm) / 40))
    bpm_points = bpm_proximity * 2.0
    score += bpm_points
    if bpm_points > 0:
        reasons.append(f"tempo proximity (+{bpm_points:.1f})")

    # 4. Numerical Proximity: Acousticness (Max +1.5 pts)
    target_ac = user_prefs.get('target_acousticness', 0.5)
    actual_ac = song.get('acousticness', 0.5)
    ac_proximity = 1 - abs(target_ac - actual_ac)
    ac_points = ac_proximity * 1.5
    score += ac_points
    if ac_points > 1.0: # Only list as a reason if it's a strong match
        reasons.append(f"acousticness match (+{ac_points:.1f})")

    # 5. Numerical Proximity: Energy & Danceability (Max +1.0 pt each)
    for feature in ['energy', 'danceability']:
        target_val = user_prefs.get(f'target_{feature}', 0.5)
        actual_val = song.get(feature, 0.5)
        feat_points = (1 - abs(target_val - actual_val)) * 1.0
        score += feat_points

    return score, reasons 

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Ranks songs based on user preferences and returns the top k recommendations with scores and explanations.

    This function evaluates each song against the user's preferences using a scoring algorithm that prioritizes
    mood matching, followed by genre, tempo proximity, acousticness, energy, and danceability. Songs are then
    sorted by their total score in descending order, and the top k recommendations are returned along with
    their scores and textual explanations of why they were recommended.

    Parameters:
    - user_prefs (Dict): A dictionary containing user preferences with keys such as:
        - 'favorite_mood' (str): The preferred mood (e.g., 'happy', 'sad').
        - 'favorite_genre' (str): The preferred genre (e.g., 'pop', 'rock').
        - 'target_bpm' (float): The target tempo in beats per minute.
        - 'target_acousticness' (float): The target acousticness level (0.0 to 1.0).
        - 'target_energy' (float): The target energy level (0.0 to 1.0).
        - 'target_danceability' (float): The target danceability level (0.0 to 1.0).
    - songs (List[Dict]): A list of dictionaries, each representing a song with attributes including
        'id', 'title', 'artist', 'genre', 'mood', 'energy', 'tempo_bpm', 'valence', 'danceability', 'acousticness'.
    - k (int, optional): The number of top recommendations to return. Defaults to 5.

    Returns:
    - List[Tuple[Dict, float, str]]: A list of tuples, where each tuple contains:
        - song (Dict): The song dictionary.
        - score (float): The computed score for the song.
        - explanation (str): A comma-separated string of reasons why the song was recommended.

    The list is sorted by score in descending order, with the highest-scoring songs first.

    Required by src/main.py
    """
    scored_results = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        # Turn the list of reasons into a single string for the display
        explanation = ", ".join(reasons)
        scored_results.append((song, score, explanation))

    # Sort by score (the second element in the tuple) in descending order
    scored_results.sort(key=lambda x: x[1], reverse=True)

    return scored_results[:k]

def display_recommendations(recommendations: List[Tuple[Dict, float, str]]) -> None:
    """
    Displays recommendations in a clean, readable terminal layout.
    Shows song title, final score, and reasons for each recommendation.
    """
    if not recommendations:
        print("No recommendations found.")
        return
    
    print("\n" + "=" * 80)
    print("TOP MUSIC RECOMMENDATIONS".center(80))
    print("=" * 80 + "\n")
    
    for idx, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"{idx}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f}")
        if explanation:
            print(f"   Reasons: {explanation}")
        else:
            print(f"   Reasons: No specific matches")
        print()