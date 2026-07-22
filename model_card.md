# 🎧 Model Card: VibePath 1.0

## 1. Model Name

**VibePath 1.0**

---

## 2. Intended Use

VibePath suggests songs that match a listener's stated taste profile. It is a
classroom simulation for learning how recommendation scores and rankings work.
It assumes the listener can describe the sound they want with labels and target
numbers. It is not intended for a real streaming service, commercial decisions,
or predicting a person's identity, emotions, or behavior.

---

## 3. How the Model Works

The model compares every song with the user's preferred genre, mood, and sound
targets. Close numerical values earn similarity points, while exact genre and
mood matches earn fixed points. The user can choose balanced, genre-first, or
energy-focused scoring. The final ranking can subtract small penalties when an
artist or genre has already appeared, which creates a more varied Top 5.

---

## 4. Data

The catalog contains 18 fictional songs across 15 genres. Each row includes
genre, mood, tempo, energy, valence, danceability, acousticness, popularity,
release decade, instrumentalness, speechiness, and liveness. The dataset is
small and synthetic. It does not include lyrics, language, listening history,
cultural context, or feedback from real listeners.

---

## 5. Strengths

The model works well when a profile closely matches a song in the catalog.
`Sunrise City`, `Focus Flow`, and `Storm Runner` correctly lead the pop, lofi,
and rock profiles. Every result has a visible score explanation. Multiple modes
also make it easy to see how different product priorities change the ranking.

---

## 6. Limitations and Bias

Several genres have only one song, so an exact label can still have too much
influence. `Empty Station` remains first for the conflicting blues profile even
though its energy is far below the target. The five advanced attributes are
invented rather than measured from audio, so they should not be treated as real
music facts. Diversity penalties improve variety, but they can also push down a
second song that the listener might genuinely prefer.

---

## 7. Evaluation

I tested Happy Energetic Pop, Chill Focused Lofi, Deep Intense Rock, and a
conflicting Happy Blues edge case. The first three profiles produced intuitive
top songs. The edge case exposed the risk of sparse genre coverage.

I also compared scoring modes. Genre-first rewards exact labels most strongly,
while energy-focused can prefer a closer energy match from another genre. In a
separate weight experiment, reducing genre and increasing energy moved
`Rooftop Lights` above `Gym Hero`. This was different, not automatically better.

Finally, I tested diversity reranking. Without a repeat-artist penalty, two
LoRoom songs appeared together near the top of the lofi list. With diversity
enabled, `Library Rain` moved ahead of the second LoRoom song while all results
remained relevant. Nine automated tests verify data conversion, scoring,
ranking, modes, explanations, and diversity behavior.

---

## 8. Future Work

- Learn weights from real likes, skips, and listening time instead of choosing
  every weight by hand.
- Use a larger, measured music catalog with lyrics and audio embeddings.
- Let listeners control how much novelty and artist diversity they want.

---

## 9. Personal Reflection

My biggest learning moment was seeing that a small weight change could reorder
reasonable-looking recommendations. The math is simple, but each weight is a
human judgment about what should matter. I was also surprised that the outputs
could feel personal even though the system has no listening history.

AI tools helped me brainstorm features, profiles, tests, and explanations. I
still had to check the math, run the program, and challenge strange results. One
important correction was noticing that the original listed weights totaled 8.0
rather than 7.0. If I continued, I would test the system with real feedback and
compare its explanations with what listeners actually say they value.
