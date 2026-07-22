import csv
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple


FLOAT_SONG_FIELDS = (
    "energy",
    "tempo_bpm",
    "valence",
    "danceability",
    "acousticness",
    "instrumentalness",
    "speechiness",
    "liveness",
)
INTEGER_SONG_FIELDS = ("id", "popularity", "release_decade")

SCORING_MODES = {
    "balanced": {
        "genre": 2.0,
        "mood": 1.0,
        "energy": 2.0,
        "valence": 1.0,
        "danceability": 1.0,
        "acousticness": 1.0,
        "popularity": 0.5,
        "release_decade": 0.5,
        "instrumentalness": 0.5,
        "speechiness": 0.5,
        "liveness": 0.5,
    },
    "genre_first": {
        "genre": 4.0,
        "mood": 1.0,
        "energy": 1.0,
        "valence": 0.75,
        "danceability": 0.75,
        "acousticness": 0.75,
        "popularity": 0.25,
        "release_decade": 0.25,
        "instrumentalness": 0.25,
        "speechiness": 0.25,
        "liveness": 0.25,
    },
    "energy_focused": {
        "genre": 1.0,
        "mood": 0.5,
        "energy": 4.0,
        "valence": 1.0,
        "danceability": 1.0,
        "acousticness": 1.0,
        "popularity": 0.25,
        "release_decade": 0.25,
        "instrumentalness": 0.25,
        "speechiness": 0.25,
        "liveness": 0.25,
    },
}
DEFAULT_SCORING_WEIGHTS = SCORING_MODES["balanced"]


@dataclass
class Song:
    """Represent a song and the attributes used for recommendation."""

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
    popularity: int = 50
    release_decade: int = 2020
    instrumentalness: float = 0.0
    speechiness: float = 0.0
    liveness: float = 0.0


@dataclass
class UserProfile:
    """Represent a user's categorical and numerical taste preferences."""

    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_valence: float = 0.5
    target_danceability: float = 0.5
    target_acousticness: Optional[float] = None
    target_popularity: int = 50
    target_release_decade: int = 2020
    target_instrumentalness: float = 0.0
    target_speechiness: float = 0.0
    target_liveness: float = 0.0


def _profile_as_dict(user: UserProfile) -> Dict:
    """Convert an object-oriented user profile to the functional API shape."""

    acousticness = user.target_acousticness
    if acousticness is None:
        acousticness = 0.8 if user.likes_acoustic else 0.2
    return {
        "favorite_genre": user.favorite_genre,
        "favorite_mood": user.favorite_mood,
        "target_energy": user.target_energy,
        "target_valence": user.target_valence,
        "target_danceability": user.target_danceability,
        "target_acousticness": acousticness,
        "target_popularity": user.target_popularity,
        "target_release_decade": user.target_release_decade,
        "target_instrumentalness": user.target_instrumentalness,
        "target_speechiness": user.target_speechiness,
        "target_liveness": user.target_liveness,
    }


class Recommender:
    """Rank Song objects using the same rules as the functional API."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return up to k songs ordered from best to worst match."""

        user_prefs = _profile_as_dict(user)
        return sorted(
            self.songs,
            key=lambda song: (-score_song(user_prefs, asdict(song))[0], song.id),
        )[: max(k, 0)]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain how each feature contributed to a Song object's score."""

        _, reasons = score_song(_profile_as_dict(user), asdict(song))
        return "; ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from CSV and convert numeric columns to numbers."""

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            for field in INTEGER_SONG_FIELDS:
                row[field] = int(row[field])
            for field in FLOAT_SONG_FIELDS:
                row[field] = float(row[field])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs


def _similarity(value: float, target: float, scale: float = 1.0) -> float:
    """Return a 0-to-1 similarity based on scaled absolute distance."""

    return max(0.0, 1.0 - abs(value - target) / scale)


def get_scoring_weights(
    mode: str = "balanced", weights: Optional[Dict[str, float]] = None
) -> Dict[str, float]:
    """Return custom weights or the named scoring strategy."""

    if weights is not None:
        return weights
    if mode not in SCORING_MODES:
        choices = ", ".join(SCORING_MODES)
        raise ValueError(f"Unknown scoring mode '{mode}'. Choose from: {choices}")
    return SCORING_MODES[mode]


def score_song(
    user_prefs: Dict,
    song: Dict,
    weights: Optional[Dict[str, float]] = None,
    mode: str = "balanced",
) -> Tuple[float, List[str]]:
    """Score one song and return its numeric score and explanation reasons."""

    active_weights = get_scoring_weights(mode, weights)
    score = 0.0
    reasons = []

    for feature, preference in (
        ("genre", "favorite_genre"),
        ("mood", "favorite_mood"),
    ):
        matches = song[feature].strip().casefold() == user_prefs[
            preference
        ].strip().casefold()
        points = active_weights.get(feature, 0.0) if matches else 0.0
        score += points
        reasons.append(
            f"{feature} {'match' if matches else 'differs'} (+{points:.2f})"
        )

    numerical_rules = (
        ("energy", "target_energy", 1.0),
        ("valence", "target_valence", 1.0),
        ("danceability", "target_danceability", 1.0),
        ("acousticness", "target_acousticness", 1.0),
        ("popularity", "target_popularity", 100.0),
        ("release_decade", "target_release_decade", 50.0),
        ("instrumentalness", "target_instrumentalness", 1.0),
        ("speechiness", "target_speechiness", 1.0),
        ("liveness", "target_liveness", 1.0),
    )
    for song_field, preference_field, scale in numerical_rules:
        if song_field not in song or preference_field not in user_prefs:
            continue
        weight = active_weights.get(song_field, 0.0)
        points = weight * _similarity(
            float(song[song_field]), float(user_prefs[preference_field]), scale
        )
        score += points
        reasons.append(f"{song_field} similarity (+{points:.2f})")
    return score, reasons


def _apply_diversity(
    scored_songs: List[Tuple[Dict, float, List[str]]], k: int
) -> List[Tuple[Dict, float, str]]:
    """Greedily rerank songs with repeat-artist and repeat-genre penalties."""

    remaining = list(scored_songs)
    selected = []
    artist_counts: Dict[str, int] = {}
    genre_counts: Dict[str, int] = {}
    while remaining and len(selected) < max(k, 0):
        candidates = []
        for song, base_score, reasons in remaining:
            artist_penalty = 0.75 * artist_counts.get(song["artist"], 0)
            genre_penalty = 0.25 * genre_counts.get(song["genre"], 0)
            adjusted_score = base_score - artist_penalty - genre_penalty
            candidates.append(
                (
                    adjusted_score,
                    -int(song["id"]),
                    song,
                    reasons,
                    artist_penalty,
                    genre_penalty,
                )
            )
        adjusted, _, song, reasons, artist_penalty, genre_penalty = max(
            candidates, key=lambda candidate: (candidate[0], candidate[1])
        )
        explanation = list(reasons)
        if artist_penalty:
            explanation.append(f"repeat artist penalty (-{artist_penalty:.2f})")
        if genre_penalty:
            explanation.append(f"repeat genre penalty (-{genre_penalty:.2f})")
        selected.append((song, adjusted, "; ".join(explanation)))
        artist_counts[song["artist"]] = artist_counts.get(song["artist"], 0) + 1
        genre_counts[song["genre"]] = genre_counts.get(song["genre"], 0) + 1
        remaining = [candidate for candidate in remaining if candidate[0] is not song]
    return selected


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    weights: Optional[Dict[str, float]] = None,
    mode: str = "balanced",
    apply_diversity: bool = False,
) -> List[Tuple[Dict, float, str]]:
    """Score and rank the highest-matching songs with explanations."""

    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weights, mode)
        scored_songs.append((song, score, reasons))
    if apply_diversity:
        return _apply_diversity(scored_songs, k)
    ranked = sorted(
        scored_songs, key=lambda result: (-result[1], int(result[0]["id"]))
    )
    return [
        (song, score, "; ".join(reasons))
        for song, score, reasons in ranked[: max(k, 0)]
    ]
