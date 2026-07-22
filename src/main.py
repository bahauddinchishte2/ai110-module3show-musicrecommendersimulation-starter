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
    songs = load_songs("data/songs.csv")

    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
        "target_valence": 0.85,
        "target_danceability": 0.80,
        "target_acousticness": 0.20,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nUser profile: happy, energetic pop")
    print("Top 5 recommendations:\n")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} — {song['artist']}")
        print(f"   Score: {score:.2f}/8.00")
        print(f"   Reasons: {explanation}")
        print()


if __name__ == "__main__":
    main()
