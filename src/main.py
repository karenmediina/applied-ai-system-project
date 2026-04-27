"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songse.csv") 

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    # productive student profile
    # A taste profile dictionary for your UserProfile object
    productive_student_profile = {
        "favorite_mood": "chill",
        "favorite_genre": "lofi",
        "target_bpm": 85,          # Mid-low tempo for focus
        "target_energy": 0.40,     # Not too distracting
        "target_acousticness": 0.75, # Preference for organic sounds
        "target_danceability": 0.40  # updated (lowered)
        }

    recommendations = recommend_songs(user_prefs, songs, k=5)
    # display_recommendations(recommendations)

    # print("\nTop recommendations:\n")
    # for rec in recommendations:
    #     # You decide the structure of each returned item.
    #     # A common pattern is: (song, score, explanation)
    #     song, score, explanation = rec
    #     print(f"{song['title']} - Score: {score:.2f}")
    #     print(f"Because: {explanation}")
    #     print()

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



if __name__ == "__main__":
    main()
