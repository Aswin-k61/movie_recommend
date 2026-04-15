import streamlit as st
st.set_page_config(layout="wide")
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import streamlit.components.v1 as components


# -------------------- CSS Styling --------------------
st.markdown("""
<style>
body {
    background-color: #0b0f1a;
}

.movie-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 20px;
    margin-top: 20px;
}

.movie-card {
    background: #141b29;
    border-radius: 16px;
    overflow: hidden;
    transition: transform 0.3s ease;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
    height: 100%;
}

.movie-card:hover {
    transform: scale(1.04);
}

.movie-poster {
    width: 100%;
    height: 320px;
    object-fit: cover;
}

.movie-info {
    padding: 15px;
}

.movie-title {
    font-size: 18px;
    font-weight: bold;
    color: white;
    min-height: 50px;
}

.movie-rating {
    color: gold;
    font-size: 15px;
    margin: 8px 0;
}

.movie-overview {
    font-size: 13px;
    color: #b0b3b8;
    line-height: 1.5;
    min-height: 80px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- API Key --------------------
API_KEY = "a4e3333f9cee2bc0630631e20c4bffa1"

# -------------------- Persistent Session with Retry --------------------
session = requests.Session()

retry = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504]
)

adapter = HTTPAdapter(max_retries=retry)
session.mount("https://", adapter)

session.headers.update({
    "User-Agent": "Mozilla/5.0"
})

# -------------------- Load Data --------------------
movies = pickle.load(open('movies.pkl', 'rb'))
semantic_vectors = pickle.load(open('semantic_vectors.pkl', 'rb'))
tfidf_vectors = pickle.load(open('tfidf_vectors.pkl', 'rb'))

# -------------------- Fetch Movie Details --------------------
@st.cache_data
def fetch_movie_details(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"

    try:
        response = session.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as e:
        print("API Error:", e)
        return {
            "poster": "https://via.placeholder.com/300x450?text=Connection+Error",
            "rating": "N/A",
            "overview": "Temporary network issue"
        }

    try:
        result = data['results'][0]

        poster_path = result.get('poster_path')
        poster_url = (
            "https://image.tmdb.org/t/p/w500/" + poster_path
            if poster_path
            else "https://via.placeholder.com/300x450?text=No+Image"
        )

        return {
            "poster": poster_url,
            "rating": result.get('vote_average', "N/A"),
            "overview": result.get('overview', "No description available")
        }

    except (IndexError, KeyError):
        return {
            "poster": "https://via.placeholder.com/300x450?text=No+Image",
            "rating": "N/A",
            "overview": "No description available"
        }

# -------------------- Recommendation Logic --------------------
def recommend(movie, num_recommendations):
    titles = movies['title'].fillna('').str.lower()

    # Exact match first
    matches = movies[titles == movie.lower()]

    # Fallback partial match
    if matches.empty:
        matches = movies[
             movies['tags'].str.contains(movie.lower(), na=False)
        ]

    if matches.empty:
        return []

    idx = matches.index[0]

    # Hybrid similarity scores
    tfidf_scores = cosine_similarity(
        tfidf_vectors[idx].reshape(1, -1),
        tfidf_vectors
    ).flatten()

    semantic_scores = cosine_similarity(
        semantic_vectors[idx].reshape(1, -1),
        semantic_vectors
    ).flatten()

    final_scores = (0.3 * tfidf_scores) + (0.7 * semantic_scores)

    similar_movies = sorted(
        list(enumerate(final_scores)),
        key=lambda x: x[1],
        reverse=True
    )

    seen_titles = set()
    filtered_movies = []

    for movie_idx, score in similar_movies:
        title = movies.iloc[movie_idx].title

        if title.lower() not in seen_titles and title.lower() != movie.lower():
            seen_titles.add(title.lower())
            filtered_movies.append((movie_idx, score))

        if len(filtered_movies) == num_recommendations:
            break

    movie_list = []

    for i in filtered_movies:
        title = movies.iloc[i[0]].title
        time.sleep(0.2)
        details = fetch_movie_details(title)

        movie_list.append({
            "title": title,
            "poster": details["poster"],
            "rating": details["rating"],
            "overview": details["overview"]
        })

    return movie_list

# -------------------- UI --------------------
st.markdown("""
<h1 style='text-align: center;'>🎬 Movie Recommender</h1>
<p style='text-align: center; color: gray;'>Find movies similar to your favorite ones</p>
""", unsafe_allow_html=True)

left, center, right = st.columns([1, 2, 1])

with center:
    movie_input = st.text_input("Enter a movie name")
    num_recommendations = st.slider("Number of recommendations", 5, 20, 10)
if st.button("Recommend"):
    with st.spinner("🍿 Finding best movies..."):
        results = recommend(movie_input, num_recommendations)

    if not results:
        st.error("Movie not found")
    else:
        st.subheader("Recommended Movies")

        movie_html = """
        <html>
        <head>
        <style>
        body {
            margin: 0;
            background: #0b0f1a;
        }
        .movie-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 20px;
            padding: 20px;
            width: 100%;
            box-sizing: border-box;
            overflow-x: hidden;
        }
        .movie-card {
            background: #141b29;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
            transition: transform 0.3s ease;
        }
        .movie-card:hover {
            transform: scale(1.03);
        }
        .movie-poster {
            width: 100%;
            height: 260px;
            object-fit: cover;
        }
        .movie-info {
            padding: 15px;
        }
        .movie-title {
            font-size: 18px;
            font-weight: bold;
            color: white;
        }
        .movie-rating {
            color: gold;
            margin: 8px 0;
        }
        .movie-overview {
            color: #b0b3b8;
            font-size: 13px;
        }
        </style>
        </head>
        <body>
        <div class="movie-grid">
        """

        for movie in results:
            movie_html += f"""
            <div class="movie-card">
                <img class="movie-poster" src="{movie['poster']}" />
                <div class="movie-info">
                    <div class="movie-title">{movie['title']}</div>
                    <div class="movie-rating">⭐ {movie['rating']}</div>
                    <div class="movie-overview">{movie['overview'][:100]}...</div>
                </div>
            </div>
            """

        movie_html += """
        </div>
        </body>
        </html>
        """

        components.html(movie_html, height=1200, scrolling=True)