"""Command-line runner for the Music Recommender Simulation."""

import argparse
from textwrap import shorten

from src.recommender import SCORING_MODES, load_songs, recommend_songs


PROFILES = {
    "Happy Energetic Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
        "target_valence": 0.85,
        "target_danceability": 0.80,
        "target_acousticness": 0.20,
        "target_popularity": 80,
        "target_release_decade": 2020,
        "target_instrumentalness": 0.05,
        "target_speechiness": 0.06,
        "target_liveness": 0.20,
    },
    "Chill Focused Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "focused",
        "target_energy": 0.40,
        "target_valence": 0.58,
        "target_danceability": 0.60,
        "target_acousticness": 0.80,
        "target_popularity": 60,
        "target_release_decade": 2020,
        "target_instrumentalness": 0.75,
        "target_speechiness": 0.06,
        "target_liveness": 0.10,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.92,
        "target_valence": 0.45,
        "target_danceability": 0.65,
        "target_acousticness": 0.10,
        "target_popularity": 75,
        "target_release_decade": 2010,
        "target_instrumentalness": 0.05,
        "target_speechiness": 0.08,
        "target_liveness": 0.30,
    },
    "Conflicting Happy Blues (Edge Case)": {
        "favorite_genre": "blues",
        "favorite_mood": "happy",
        "target_energy": 0.95,
        "target_valence": 0.20,
        "target_danceability": 0.20,
        "target_acousticness": 0.90,
        "target_popularity": 55,
        "target_release_decade": 1990,
        "target_instrumentalness": 0.25,
        "target_speechiness": 0.05,
        "target_liveness": 0.30,
    },
}


def format_recommendation_table(recommendations: list, maximum_score: float) -> str:
    """Return recommendations as a readable dependency-free ASCII table."""

    headers = ("#", "Title", "Artist", "Score", "Reasons")
    rows = []
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        rows.append(
            (
                str(rank),
                song["title"],
                song["artist"],
                f"{score:.2f}/{maximum_score:.2f}",
                shorten(explanation, width=72, placeholder="…"),
            )
        )
    widths = [
        max(len(str(row[index])) for row in [headers, *rows]) for index in range(5)
    ]
    border = "+" + "+".join("-" * (width + 2) for width in widths) + "+"

    def format_row(row: tuple) -> str:
        return "| " + " | ".join(
            str(value).ljust(width) for value, width in zip(row, widths)
        ) + " |"

    return "\n".join([border, format_row(headers), border, *map(format_row, rows), border])


def parse_args() -> argparse.Namespace:
    """Parse scoring-mode and diversity options from the command line."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=SCORING_MODES,
        default="balanced",
        help="Scoring strategy to use (default: balanced).",
    )
    parser.add_argument(
        "--no-diversity",
        action="store_true",
        help="Disable repeat-artist and repeat-genre penalties.",
    )
    return parser.parse_args()


def main() -> None:
    """Evaluate all profiles using the selected scoring strategy."""

    args = parse_args()
    songs = load_songs("data/songs.csv")
    weights = SCORING_MODES[args.mode]
    maximum_score = sum(weights.values())
    diversity_enabled = not args.no_diversity
    print(f"Scoring mode: {args.mode}")
    print(f"Diversity reranking: {'on' if diversity_enabled else 'off'}")

    for profile_name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(
            user_prefs,
            songs,
            k=5,
            mode=args.mode,
            apply_diversity=diversity_enabled,
        )
        print(f"\nUser profile: {profile_name}")
        print(format_recommendation_table(recommendations, maximum_score))


if __name__ == "__main__":
    main()
