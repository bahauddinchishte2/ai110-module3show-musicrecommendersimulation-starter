"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


PROFILES = {
    "Happy Energetic Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
        "target_valence": 0.85,
        "target_danceability": 0.80,
        "target_acousticness": 0.20,
    },
    "Chill Focused Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "focused",
        "target_energy": 0.40,
        "target_valence": 0.58,
        "target_danceability": 0.60,
        "target_acousticness": 0.80,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.92,
        "target_valence": 0.45,
        "target_danceability": 0.65,
        "target_acousticness": 0.10,
    },
    "Conflicting Happy Blues (Edge Case)": {
        "favorite_genre": "blues",
        "favorite_mood": "happy",
        "target_energy": 0.95,
        "target_valence": 0.20,
        "target_danceability": 0.20,
        "target_acousticness": 0.90,
    },
}


def print_recommendations(profile_name: str, recommendations: list) -> None:
    """Print one profile and its explained Top 5 recommendations."""

    print(f"\nUser profile: {profile_name}")
    print("Top 5 recommendations:\n")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} — {song['artist']}")
        print(f"   Score: {score:.2f}/8.00")
        print(f"   Reasons: {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile_name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(profile_name, recommendations)


if __name__ == "__main__":
    main()
