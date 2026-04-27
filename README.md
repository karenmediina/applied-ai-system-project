# DJ VI: Music Recommender

### Project Overview

Have you ever wished for a whole playlist that fits a specific vibe? But couldn't find that vibe on spotify. Same. That's why I made DJ VI!

As a starting point for this project, I built upon a previous music recommender system that I worked on for Module 3 of the Codepath AI110 Course. The goal was to represent songs and a user "taste profile" as data, design a scoring rule that turns that data into recommendations and evaluate the system. 

For this milestone, I transformed the tool into an **Applied AI System**. DJ VI uses a **RAG (Retrieval-Augmented Generation)** architecture to bridge the gap between 'mood' & 'vibes' and structured music data. Instead of searching by genre, users can input complex emotional states or aesthetic descriptions.

Traditional music search is limited by metadata tags (e.g. "Reggaeton"), but DJ VI allows for **semantic discovery**, translating a user's abstract mood into a specific, verified song recommendation.

Loom walkthrough: https://www.loom.com/share/8a44d33aec5a40f89fa095d9efe24436

### **Architecture Overview**
The system follows a **RAG Pipeline**:
1.  **User Input:** Captures an abstract mood or "vibe" via Streamlit.
2.  **AI Reasoner:** Gemini 2.5 Flash interprets the mood and suggests a target song/artist.
3.  **Data Retrieval:** The system calls the **Spotify API** to verify the suggestion exists and retrieves real-world metadata, such as album Art and the Spotify URL.
4.  **UI Generation:** The system combines the AI's "reasoning" with the API's "ground truth" into a clean user interface.

---
## Getting Started

### Setup Instructions
1.  Clone the Repository:
      `git clone [your-repo-link]`
2.  Install Dependencies:
      `python -m pip install google-genai spotipy streamlit python-dotenv`
3.  Configure Environment Variables:
      Create a `.env` file in the root directory with:
      * `GEMINI_API_KEY`
      * `SPOTIPY_CLIENT_ID`
      * `SPOTIPY_CLIENT_SECRET`
4.  Run the App:
      `python -m streamlit run app.py`

### **Sample Interactions**
| User Input | AI Recommendation | System Output |
| :--- | :--- | :--- |
| "Nostalgic late night drive" | *Fade Into You* by Mazzy Star | Verified Spotify Link + Album Art |
| "Dancing in the rain to Baby Miko" | *Wiggy* by Young Miko | Context-aware artist match |
| "Studying at Green Library at 2 AM" | *Lofi hip hop beats* (Various) | Thematic aesthetic match |

## Design Decisions & Trade-offs
* Gemini <> Spotify: I chose to use Gemini for recommendation logic but forced it to pass through a Spotify API "gatekeeper."  
    * *Trade-off:* Adds latency  because the system must call two different APIs before responding but this prevents hallucinations (AI suggesting fake songs). 
* Prompting Strategy: I intentionally kept the prompt flexible to allow for creative "Bottom-Up" discovery.
    * *Trade-off:* This sometimes leads to ambiguity (an example I ran into was Gemini confusing "Miko" with Japanese artists), but preserves exposure.

### **Testing Summary & Reflection**
The system works very well at identifying a vibe even if the description is ambiguous. Additionally, the integration between the GenAI SDK and Spotipy is stable and handles errors gracefully.

On the other hand, AI does not deal too well with polysemy most likely due to not having much background information or context. Furthermore, the cold start for Gemini and Spotify can take 1-2 seconds, which is noticeable in the UI.

Although all projects will have more to add, I'm very happy with the introduction to APIs this project gave me and the experience of manipulating how they communicate with each other and the pipeline. Each one has its own set of restrictions but it was my job to make them play nicely for the user and control the interaction between indeterministic output and a rigid, structured database like Spotify. This reinforced my interest in the intersection of human language and computational structures. <3

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

