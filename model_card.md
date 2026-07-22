# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

The 18-song catalog is too small to represent the variety inside each genre,
and several genres have only one song. Exact genre and mood labels can therefore
create a filter bubble by repeatedly rewarding the only labeled match. The edge
case showed that `Empty Station` could rank first for a high-energy listener even
though its energy is only 0.45, because it was the catalog's only blues song.
The model also ignores lyrics, listening history, context, and diversity, so its
scores should not be treated as proof that a listener will enjoy a song.

---

## 7. Evaluation  

I ran four profiles: Happy Energetic Pop, Chill Focused Lofi, Deep Intense Rock,
and a conflicting Happy Blues edge case. The first three felt reasonable:
`Sunrise City`, `Focus Flow`, and `Storm Runner` ranked first because each nearly
matched its profile across both labels and numerical features. `Gym Hero` also
appeared for both pop and rock listeners: it earns the pop genre bonus in one
case and the intense mood bonus plus high-energy similarity in the other.

The edge case requested happy blues with very high energy but low valence,
low danceability, and high acousticness. `Empty Station` ranked first even with
a large energy gap because it received the catalog's only blues genre bonus.
That result is explainable, but it does not fully match my musical intuition and
shows how a sparse catalog can make one label too influential.

### Profile Comparisons

- Happy Pop vs. Chill Lofi: the pop list favors bright, electronic tracks,
  while the lofi list shifts to low-energy, highly acoustic tracks.
- Happy Pop vs. Intense Rock: both include `Gym Hero`, but pop rewards its genre
  and rock rewards its intense mood and high energy.
- Happy Pop vs. Happy Blues: the shared happy label helps pop songs in both,
  but the blues bonus makes `Empty Station` win the edge-case list.
- Chill Lofi vs. Intense Rock: their top results are almost opposites in energy
  and acousticness, which is exactly what those profiles were designed to test.
- Chill Lofi vs. Happy Blues: both prefer acoustic sound, but the conflicting
  profile's high-energy target pulls rock and pop songs into its lower ranks.
- Intense Rock vs. Happy Blues: both request high energy, but rock favors
  amplified low-acoustic tracks while the blues profile asks for high acousticness.

### Weight-Shift Experiment

For Happy Energetic Pop, I halved genre weight from 2.0 to 1.0 and doubled
energy from 2.0 to 4.0. `Sunrise City` remained first, while `Rooftop Lights`
moved from third to second and `Gym Hero` moved from second to third. This made
the list more sensitive to energy closeness but less faithful to the explicit
genre preference, so the result was different rather than universally better.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
