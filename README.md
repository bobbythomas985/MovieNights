# 🎬 MovieNights – Personalized Movie Recommendation System

**MovieNights** is an interactive **Streamlit-based movie recommendation system** that recommends top movies based on your favorite genres, provides personalized suggestions, and allows you to explore detailed movie information with a modern, card-based UI.  

---

## ✨ Features

✅ **User Authentication** – Sign up, log in, and save your favorite genres  
✅ **Personalized Recommendations** – Get a curated list of movies based on your genre preferences  
✅ **Movie Cards with Hover Effects** – Clean, responsive UI with poster images and overviews  
✅ **Detailed Movie Pages** – Click “Know More” to explore details, posters, and ratings  
✅ **Smart Recommendations** – Suggests similar movies using a precomputed similarity matrix  
✅ **Session State Management** – Seamless navigation between Sign In, Home, and Movie Details pages  

---

## 🛠 Tech Stack

- **Frontend & App Framework:** [Streamlit](https://streamlit.io/)  
- **Backend & Logic:** Python (pandas, similarity computation)  
- **Data Handling:** `pandas`, `MultiLabelBinarizer` for genres, cosine similarity  
- **Custom Styling:** Streamlit + CSS for hover effects and responsive movie cards  
- **Image Hosting:** TMDB Poster Paths  

---

## 🖥️ How It Works

1️⃣ **User Authentication**  
Sign up with your favorite genres → Log in securely → Navigate to your personalized dashboard.  

2️⃣ **Genre-Based Recommendations**  
The app filters movies matching your chosen genres, ranks them by `vote_average`, and displays the top 20.  

3️⃣ **Interactive Movie Cards**  
Hover over a movie card to reveal its overview, genres, and “Know More” button.  

4️⃣ **Movie Details + Similar Movies**  
View details of a selected movie along with AI-powered recommendations using a similarity matrix.  


## 📦 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/bobbythomas985/MovieNights
cd MovieNights
```
### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 3️⃣ Run the App
```python
streamlit run app.py
```
### 4️⃣ Open in Browser
Visit **http://localhost:8501** to use the app.

---

## 🖥️ How It Works

1️⃣ **Upload a PDF**  
📄 The system extracts all text from the research paper.

2️⃣ **Process & Embed**  
🔍 Splits the extracted text into overlapping chunks and creates a **FAISS vector index** using **HuggingFace embeddings** for efficient semantic search.

3️⃣ **Ask Questions**  
❓ User questions are converted into embeddings and matched with the most relevant chunks from the document.

4️⃣ **LLM Answer Generation**  
🤖 Groq’s `llama-3.3-70b-versatile` model is used to generate accurate, context-aware answers with a custom prompt.

5️⃣ **Summarize & Discover Papers**  
📝 Generates engaging, structured summaries of the document and retrieves similar papers from **arXiv** for further reading.


## 🔮 Future Improvements
- 🎭 Collaborative Filtering – Recommend movies based on similar users' preferences
- 🔍 Search Bar – Search for movies by title or actor
- 🎥 Trailer Integration – Embed YouTube trailers in movie details page
- 📊 Ratings & Watchlist – Allow users to rate and save movies
- 🌐 Deploy to Cloud – Host on Streamlit Cloud / Hugging Face Spaces for public access
---

> *Making movie nights easier, smarter, and more personalized!*
