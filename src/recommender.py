import csv
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple


NUMERIC_SONG_FIELDS = (
    "energy",
    "tempo_bpm",
    "valence",
    "danceability",
    "acousticness",
)

DEFAULT_SCORING_WEIGHTS = {
    "genre": 2.0,
    "mood": 1.0,
    "energy": 2.0,
    "valence": 1.0,
    "danceability": 1.0,
    "acousticness": 1.0,
}


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
            row["id"] = int(row["id"])
            for field in NUMERIC_SONG_FIELDS:
                row[field] = float(row[field])
            songs.append(row)

    print(f"Loaded songs: {len(songs)}")
    return songs


def _similarity(value: float, target: float) -> float:
    """Return a 0-to-1 similarity based on absolute distance."""

    return max(0.0, 1.0 - abs(value - target))


def score_song(
    user_prefs: Dict, song: Dict, weights: Optional[Dict[str, float]] = None
) -> Tuple[float, List[str]]:
    """Score one song and return its numeric score and explanation reasons."""

    active_weights = DEFAULT_SCORING_WEIGHTS if weights is None else weights
    score = 0.0
    reasons = []

    genre_matches = song["genre"].strip().casefold() == user_prefs[
        "favorite_genre"
    ].strip().casefold()
    genre_points = active_weights["genre"] if genre_matches else 0.0
    score += genre_points
    reasons.append(
        f"genre {'match' if genre_matches else 'differs'} (+{genre_points:.2f})"
    )

    mood_matches = song["mood"].strip().casefold() == user_prefs[
        "favorite_mood"
    ].strip().casefold()
    mood_points = active_weights["mood"] if mood_matches else 0.0
    score += mood_points
    reasons.append(
        f"mood {'match' if mood_matches else 'differs'} (+{mood_points:.2f})"
    )

    numerical_rules = (
        ("energy", "target_energy", active_weights["energy"]),
        ("valence", "target_valence", active_weights["valence"]),
        ("danceability", "target_danceability", active_weights["danceability"]),
        ("acousticness", "target_acousticness", active_weights["acousticness"]),
    )
    for song_field, preference_field, weight in numerical_rules:
        points = weight * _similarity(
            float(song[song_field]), float(user_prefs[preference_field])
        )
        score += points
        reasons.append(f"{song_field} similarity (+{points:.2f})")

    return score, reasons


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    weights: Optional[Dict[str, float]] = None,
) -> List[Tuple[Dict, float, str]]:
    """Score all songs and return the highest-ranked k with explanations."""

    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weights)
        scored_songs.append((song, score, "; ".join(reasons)))

    return sorted(
        scored_songs,
        key=lambda result: (-result[1], int(result[0]["id"])),
    )[: max(k, 0)]
