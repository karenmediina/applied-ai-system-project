# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
DJ VI  

---

## 2. Intended Use

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

DJ VI is an AI music curator designed to bridge the gap between subjective human experience and structured music metadata! It generates 3-track "vibe-checks" based on natural language descriptions. Instead of relying on rigid genre labels, it uses the LLM’s reasoning to interpret the emotional subtext of a prompt and matches it to specific tracks verified via the Spotify API.


There are barely any assumptions about the user other than that they would prefer to describe a feeling or scenario rather than technical musical terms. The system is more for classroom exploration as I consider there are still many features that could be added in order to make it ready for deployment such as curating an entire playlist and keeping track of previous engagement with other songs. This project does show that LLM creativity can be safely grounded by external APIs, namely Spotipy.

A potential misuse of this tool could be to find nonmainstream recommendations and then go to another platform, that doesn't compensate the creators, to stream the song. As a push in the other direction, the app provides links that connect directly to streaming platform Spotify, where creators are supposed to get their compensation. 
---

## 3. How the Model Works  - MISSING

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.


---

## 4. Data  - MISSING

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Limitations and Bias

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

A limitation of this system is that since it relies on the Spotify API, it inherits Spotify's library biases potentially neglecting smaller, more niche artists. Even if Gemini happens to recommend them, they might not be found and therefore DJ VI won't be able to recommend them. 

In a similar vein, the system is subject to semantic drift when the AI overgeneralizes, or doesn't place appropriate weights to certain preferences. This and further personalization could be addressed by modifying the prompt, but it was purposefully left general for classroom purposes. In the future, one could explore how it grows personalized as interactions with the songs are tracked. 

---

## 6. Evaluation  - MISSING

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.



---

## 8. Future Work  - MISSING

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  - MISSING

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
