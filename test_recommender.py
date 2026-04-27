from src.recommender import MusicRecommender
from dotenv import load_dotenv
import os

# Ensure environment variables are loaded
load_dotenv()

def test_system():
    print("--- Initializing Recommender System ---")
    try:
        # 1. Initialize the class
        recommender = MusicRecommender()
        print("✅ System Initialized (APIs Connected)")

        # 2. Test with a specific mood
        mood = "nostalgic and ready for a late night drive"
        print(f"--- Testing Mood: '{mood}' ---")
        
        result = recommender.get_recommendation(mood)

        # 3. Check the results
        if result:
            print(f"✅ Success! Recommended: {result['name']} by {result['artist']}")
            print(f"🔗 URL: {result['url']}")
            print(f"🖼️ Image: {result['image']}")
            print(f"📝 Reason: {result['reason']}")
        else:
            print("❌ Failure: No recommendation returned.")

    except Exception as e:
        print(f"❌ Error during test: {e}")

if __name__ == "__main__":
    test_system()