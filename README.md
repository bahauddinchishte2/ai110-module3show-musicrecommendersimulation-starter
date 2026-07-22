# 🎵 Music Recommender Simulation

## Project Summary

This project is a CLI-first, content-based music recommender simulation. It
loads an 18-song catalog from CSV, compares every song with a listener's taste
profile, and prints a ranked Top 5 with a score and plain-language reasons for
each result. Its weighted rules make the transformation from song data to a
recommendation visible instead of hiding it inside a black box.

---

## How The System Works

This simulation uses **content-based filtering**. It compares the attributes of
each song with a user's stated preferences instead of relying on other users'
listening histories. Each song has identity fields (`id`, `title`, and `artist`),
categorical features (`genre` and `mood`), and numerical features
(`energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`). The
initial 10-song catalog was expanded to 18 songs so the simulator represents a
wider range of genres and moods.

### Target User Profile

The first user profile represents someone who prefers happy, energetic,
danceable pop with a mostly electronic sound:

```python
user_profile = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.80,
    "target_valence": 0.85,
    "target_danceability": 0.80,
    "target_acousticness": 0.20,
}
```

This profile should clearly distinguish intense rock from chill lofi. An
intense rock song may be close to the energy target, but it will not match the
preferred genre or mood. Chill lofi will usually be farther from the energy,
danceability, and acousticness targets. However, the profile is intentionally
narrow: it may overlook dark but energetic pop or happy acoustic songs that the
listener could still enjoy.

### Algorithm Recipe

Each song can earn a maximum score of **8.0 points**:

- Exact genre match: `+2.0`
- Exact mood match: `+1.0`
- Energy similarity: `2 × (1 - |song energy - target energy|)`
- Valence similarity: `1 × (1 - |song valence - target valence|)`
- Danceability similarity: `1 × (1 - |song danceability - target danceability|)`
- Acousticness similarity: `1 × (1 - |song acousticness - target acousticness|)`

The similarity formulas reward closeness to the user's target rather than
rewarding every high value. Energy receives twice the weight of the other
numerical features because it strongly affects whether a track feels intense
or relaxed. After every song is scored, the recommender sorts songs from the
highest score to the lowest. If two songs have the same score, the song with
the lower ID comes first. It then returns the top `k` songs.

The implementation uses `sorted()` because it produces a new ranked list and
leaves the original song catalog unchanged. In contrast, a list's `.sort()`
method changes that list in place and returns `None`.

### Data Flow

```text
Input: user preferences
        |
        v
Process: load the CSV and score every song with the algorithm recipe
        |
        v
Ranking: sort by score (then by song ID for ties)
        |
        v
Output: return the Top K recommendations
```

### Expected Biases

Exact genre and mood matches depend on broad human-assigned labels, so two
similar songs with different labels may be treated as unrelated. The similarity
rules can also create a filter bubble by repeatedly favoring songs close to the
same target vibe. Finally, this small synthetic catalog cannot represent the
full variety within each genre, mood, culture, or listener's taste.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Running `python -m src.main` evaluates four profiles. The following blocks are
the observed Top 5 results for each profile.

### Happy Energetic Pop

```text
1. Sunrise City — Neon Echo
   Score: 7.92/8.00
   Reasons: genre match (+2.00); mood match (+1.00); energy similarity (+1.96); valence similarity (+0.99); danceability similarity (+0.99); acousticness similarity (+0.98)

2. Gym Hero — Max Pulse
   Score: 6.43/8.00
   Reasons: genre match (+2.00); mood differs (+0.00); energy similarity (+1.74); valence similarity (+0.92); danceability similarity (+0.92); acousticness similarity (+0.85)

3. Rooftop Lights — Indigo Parade
   Score: 5.71/8.00
   Reasons: genre differs (+0.00); mood match (+1.00); energy similarity (+1.92); valence similarity (+0.96); danceability similarity (+0.98); acousticness similarity (+0.85)

4. Carnival Sky — Sol Mercado
   Score: 4.61/8.00
   Reasons: genre differs (+0.00); mood differs (+0.00); energy similarity (+1.82); valence similarity (+0.94); danceability similarity (+0.87); acousticness similarity (+0.98)

5. Concrete Crown — North Cipher
   Score: 4.55/8.00
   Reasons: genre differs (+0.00); mood differs (+0.00); energy similarity (+1.88); valence similarity (+0.83); danceability similarity (+0.96); acousticness similarity (+0.88)
```

### Chill Focused Lofi

```text
1. Focus Flow — LoRoom
   Score: 7.97/8.00
   Reasons: genre match (+2.00); mood match (+1.00); energy similarity (+2.00); valence similarity (+0.99); danceability similarity (+1.00); acousticness similarity (+0.98)

2. Midnight Coding — LoRoom
   Score: 6.83/8.00
   Reasons: genre match (+2.00); mood differs (+0.00); energy similarity (+1.96); valence similarity (+0.98); danceability similarity (+0.98); acousticness similarity (+0.91)

3. Library Rain — Paper Lanterns
   Score: 6.80/8.00
   Reasons: genre match (+2.00); mood differs (+0.00); energy similarity (+1.90); valence similarity (+0.98); danceability similarity (+0.98); acousticness similarity (+0.94)

4. River Memory — Cedar Thread
   Score: 4.80/8.00
   Reasons: genre differs (+0.00); mood differs (+0.00); energy similarity (+1.98); valence similarity (+0.99); danceability similarity (+0.90); acousticness similarity (+0.93)

5. Coffee Shop Stories — Slow Stereo
   Score: 4.66/8.00
   Reasons: genre differs (+0.00); mood differs (+0.00); energy similarity (+1.94); valence similarity (+0.87); danceability similarity (+0.94); acousticness similarity (+0.91)
```

### Deep Intense Rock

```text
1. Storm Runner — Voltline
   Score: 7.94/8.00
   Reasons: genre match (+2.00); mood match (+1.00); energy similarity (+1.98); valence similarity (+0.97); danceability similarity (+0.99); acousticness similarity (+1.00)

2. Gym Hero — Max Pulse
   Score: 5.38/8.00
   Reasons: genre differs (+0.00); mood match (+1.00); energy similarity (+1.98); valence similarity (+0.68); danceability similarity (+0.77); acousticness similarity (+0.95)

3. Concrete Crown — North Cipher
   Score: 4.44/8.00
   Reasons: genre differs (+0.00); mood differs (+0.00); energy similarity (+1.88); valence similarity (+0.77); danceability similarity (+0.81); acousticness similarity (+0.98)

4. Night Drive Loop — Neon Echo
   Score: 4.42/8.00
   Reasons: genre differs (+0.00); mood differs (+0.00); energy similarity (+1.66); valence similarity (+0.96); danceability similarity (+0.92); acousticness similarity (+0.88)

5. Electric Bloom — Pulse Arcade
   Score: 4.23/8.00
   Reasons: genre differs (+0.00); mood differs (+0.00); energy similarity (+1.96); valence similarity (+0.57); danceability similarity (+0.74); acousticness similarity (+0.96)
```

### Conflicting Happy Blues (Edge Case)

```text
1. Empty Station — Blue Hour
   Score: 5.55/8.00
   Reasons: genre match (+2.00); mood differs (+0.00); energy similarity (+1.00); valence similarity (+0.92); danceability similarity (+0.72); acousticness similarity (+0.91)

2. Rooftop Lights — Indigo Parade
   Score: 3.84/8.00
   Reasons: genre differs (+0.00); mood match (+1.00); energy similarity (+1.62); valence similarity (+0.39); danceability similarity (+0.38); acousticness similarity (+0.45)

3. Sunrise City — Neon Echo
   Score: 3.79/8.00
   Reasons: genre differs (+0.00); mood match (+1.00); energy similarity (+1.74); valence similarity (+0.36); danceability similarity (+0.41); acousticness similarity (+0.28)

4. Storm Runner — Voltline
   Score: 3.38/8.00
   Reasons: genre differs (+0.00); mood differs (+0.00); energy similarity (+1.92); valence similarity (+0.72); danceability similarity (+0.54); acousticness similarity (+0.20)

5. Dust and Gold — Canyon Lines
   Score: 3.30/8.00
   Reasons: genre differs (+0.00); mood differs (+0.00); energy similarity (+1.26); valence similarity (+0.57); danceability similarity (+0.61); acousticness similarity (+0.86)
```

---

## Experiments You Tried

I tested a weight shift on the Happy Energetic Pop profile. The default formula
uses genre weight `2.0` and energy weight `2.0`. The experiment halved genre to
`1.0` and doubled energy to `4.0`, raising the experimental maximum to `9.0`.

```text
Baseline:     Sunrise City, Gym Hero, Rooftop Lights, Carnival Sky, Concrete Crown
Weight shift: Sunrise City, Rooftop Lights, Gym Hero, Concrete Crown, Carnival Sky
```

`Sunrise City` stayed first, but `Rooftop Lights` moved above `Gym Hero` because
its energy is closer to the target and genre now matters less. The result was
not objectively more accurate; it was more focused on numerical vibe and less
focused on the user's explicit pop preference.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this
