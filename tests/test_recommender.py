import pytest

from src.recommender import (
    Recommender,
    Song,
    UserProfile,
    load_songs,
    recommend_songs,
    score_song,
)


PERFECT_PROFILE = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.8,
    "target_valence": 0.9,
    "target_danceability": 0.8,
    "target_acousticness": 0.2,
}


def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""
    assert "genre match" in explanation


def test_load_songs_converts_numeric_fields():
    songs = load_songs("data/songs.csv")

    assert len(songs) == 18
    assert isinstance(songs[0]["id"], int)
    assert isinstance(songs[0]["energy"], float)
    assert isinstance(songs[0]["tempo_bpm"], float)


def test_score_song_applies_the_complete_recipe():
    song = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "valence": 0.9,
        "danceability": 0.8,
        "acousticness": 0.2,
    }

    score, reasons = score_song(PERFECT_PROFILE, song)

    assert score == pytest.approx(8.0)
    assert len(reasons) == 6
    assert "energy similarity (+2.00)" in reasons


def test_recommend_songs_ranks_without_mutating_catalog():
    songs = [
        {
            "id": 2,
            "title": "Far Match",
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.2,
            "valence": 0.4,
            "danceability": 0.3,
            "acousticness": 0.9,
        },
        {
            "id": 1,
            "title": "Perfect Match",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "valence": 0.9,
            "danceability": 0.8,
            "acousticness": 0.2,
        },
    ]
    original_order = list(songs)

    results = recommend_songs(PERFECT_PROFILE, songs, k=1)

    assert results[0][0]["title"] == "Perfect Match"
    assert results[0][1] == pytest.approx(8.0)
    assert "genre match" in results[0][2]
    assert songs == original_order
