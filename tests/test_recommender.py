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
    assert isinstance(songs[0]["popularity"], int)
    assert isinstance(songs[0]["release_decade"], int)
    assert isinstance(songs[0]["instrumentalness"], float)


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


def test_score_song_accepts_experimental_weights():
    song = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "valence": 0.9,
        "danceability": 0.8,
        "acousticness": 0.2,
    }
    weight_shift = {
        "genre": 1.0,
        "mood": 1.0,
        "energy": 4.0,
        "valence": 1.0,
        "danceability": 1.0,
        "acousticness": 1.0,
    }

    score, reasons = score_song(PERFECT_PROFILE, song, weight_shift)

    assert score == pytest.approx(9.0)
    assert "genre match (+1.00)" in reasons
    assert "energy similarity (+4.00)" in reasons


def test_advanced_features_contribute_to_balanced_score():
    profile = {
        **PERFECT_PROFILE,
        "target_popularity": 80,
        "target_release_decade": 2020,
        "target_instrumentalness": 0.1,
        "target_speechiness": 0.05,
        "target_liveness": 0.2,
    }
    song = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "valence": 0.9,
        "danceability": 0.8,
        "acousticness": 0.2,
        "popularity": 80,
        "release_decade": 2020,
        "instrumentalness": 0.1,
        "speechiness": 0.05,
        "liveness": 0.2,
    }

    score, reasons = score_song(profile, song)

    assert score == pytest.approx(10.5)
    assert len(reasons) == 11
    assert "popularity similarity (+0.50)" in reasons


def test_scoring_modes_change_ranking_priorities():
    profile = {**PERFECT_PROFILE, "target_energy": 1.0}
    genre_match = {
        "id": 1,
        "title": "Genre Match",
        "artist": "Artist A",
        "genre": "pop",
        "mood": "other",
        "energy": 0.0,
        "valence": 0.9,
        "danceability": 0.8,
        "acousticness": 0.2,
    }
    energy_match = {
        **genre_match,
        "id": 2,
        "title": "Energy Match",
        "artist": "Artist B",
        "genre": "rock",
        "energy": 1.0,
    }

    genre_results = recommend_songs(
        profile, [genre_match, energy_match], mode="genre_first"
    )
    energy_results = recommend_songs(
        profile, [genre_match, energy_match], mode="energy_focused"
    )

    assert genre_results[0][0]["title"] == "Genre Match"
    assert energy_results[0][0]["title"] == "Energy Match"


def test_diversity_penalty_avoids_repeating_artist_when_scores_tie():
    songs = []
    for song_id, artist in ((1, "Repeated Artist"), (2, "Repeated Artist"), (3, "New Artist")):
        songs.append(
            {
                "id": song_id,
                "title": f"Song {song_id}",
                "artist": artist,
                "genre": "pop",
                "mood": "happy",
                "energy": 0.8,
                "valence": 0.9,
                "danceability": 0.8,
                "acousticness": 0.2,
            }
        )

    results = recommend_songs(PERFECT_PROFILE, songs, k=2, apply_diversity=True)

    assert results[0][0]["artist"] == "Repeated Artist"
    assert results[1][0]["artist"] == "New Artist"
    assert "repeat genre penalty" in results[1][2]
