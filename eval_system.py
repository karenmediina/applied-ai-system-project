import os
from src.recommender import MusicRecommender
from dotenv import load_dotenv

load_dotenv()

def run_evaluations():
    engine = MusicRecommender()
    
    # Test cases: Diverse vibes to stress-test the AI
    test_cases = [
        "Lofi beats for studying at Green Library",
        "Reggaeton for a beach party in Puerto Rico",
        "Sad indie songs for a rainy day in Palo Alto",
        "High energy workout music",
        "80s synthwave for a night drive"
    ]
    
    passed = 0
    total = len(test_cases)
    
    print("🚀 Starting DJ Vi Evaluation...\n")
    
    for vibe in test_cases:
        print(f"Testing Vibe: '{vibe}'")
        try:
            results = engine.get_recommendation(vibe)
            
            # Metric: Did we get exactly 3 verified songs back?
            if isinstance(results, list) and len(results) == 3:
                print(f"✅ PASS: Found 3 tracks.")
                passed += 1
            else:
                print(f"❌ FAIL: Returned {len(results)} tracks.")
        except Exception as e:
            print(f"❌ FAIL: System Error: {e}")
        print("-" * 30)
    
    accuracy = (passed / total) * 100
    print(f"\nFINAL METRICS:")
    print(f"Accuracy: {accuracy}% ({passed}/{total} tests passed)")
    print(f"Reliability: {'High' if accuracy > 80 else 'Needs Tuning'}")

if __name__ == "__main__":
    run_evaluations()