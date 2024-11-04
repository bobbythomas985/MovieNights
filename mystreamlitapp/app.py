import streamlit as st
import pandas as pd
from utils import load_data, preprocess_data, compute_similarity, recommend_movie, create_user, authenticate_user

# Load and preprocess data
meta = load_data()
meta, mlb, overview_df = preprocess_data(meta)
similarity_matrix = compute_similarity(meta, mlb, overview_df)

# Set page config for better visuals
st.set_page_config(page_title="Movie Recommendation System", layout="wide")

# Define custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
        color: #343a40;
    }
    h1 {
        text-align: center;
        color: #007bff;
    }
    .btn {
        background-color: #007bff;
        color: white;
    }
    .btn:hover {
        background-color: #0056b3;
    }
    .movie-card {
        background: white;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    .movie-card:hover {
        transform: translateY(-5px);
    }
    .movie-title {
        font-weight: bold;
        font-size: 1.2em;
        color: #007bff;
    }
    
</style>
""", unsafe_allow_html=True)

# Streamlit app layout
st.title("Movie Recommendation System")

# Page navigation and session state management
if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = "sign_in"
if 'selected_movie' not in st.session_state:
    st.session_state.selected_movie = None

# Sign In page
if st.session_state.page == "sign_in":
    st.subheader("Sign In")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Sign In", key='sign_in_button'):
        user, genres = authenticate_user(username, password)
        if user is not None:
            st.session_state.user = user
            st.session_state.genres = genres  # Get user-selected genres
            st.session_state.page = "home"
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password.")
    
    if st.button("Don't have an account? Sign Up", key='redirect_sign_up'):
        st.session_state.page = "sign_up"

# Sign Up page
elif st.session_state.page == "sign_up":
    st.subheader("Sign Up")
    username = st.text_input("Username", key="signup_username")
    password = st.text_input("Password", type='password', key="signup_password")
    genres = st.multiselect("Select your favorite genres", options=meta['genres'].explode().unique())
    
    if st.button("Sign Up", key='sign_up_button'):
        if create_user(username, password, ','.join(genres)):
            st.success("Account created successfully! Please log in.")
            st.session_state.page = "sign_in"
        else:
            st.error("Username already exists.")
    
    if st.button("Already have an account? Sign In", key='redirect_sign_in'):
        st.session_state.page = "sign_in"

# Home page after successful sign-in
elif st.session_state.page == "home" and st.session_state.user is not None:
    st.subheader("Top Movies Based on Your Genres")
    selected_genres = st.session_state.genres.split(',')
    filtered_movies = meta[meta['genres'].apply(lambda x: any(genre in x for genre in selected_genres))]
    top_movies = filtered_movies.sort_values(by='vote_average', ascending=False).head(20)

    # Display movies in a grid layout
    cols = st.columns(4)
    for index, row in top_movies.iterrows():
        with cols[index % 4]:
            if st.button(row['title'], key=f"movie_{index}"):
                st.session_state.selected_movie = row
                st.session_state.page = "movie_details"

            st.markdown(f"""
                <div class="movie-card">
                    <img src="{"http://image.tmdb.org/t/p/w185" + row['poster_path']}" width="100%" alt="{row['title']}"/>
                    <div class="movie-title">{row['title']}</div>
                </div>
            """, unsafe_allow_html=True)

    # Logout button
    if st.button("Log Out"):
        st.session_state.user = None
        st.session_state.page = "sign_in"

# Movie Details Page
elif st.session_state.page == "movie_details" and st.session_state.selected_movie is not None:
    movie_details = st.session_state.selected_movie
    st.subheader(movie_details['title'])
    st.image("http://image.tmdb.org/t/p/w500" + movie_details['poster_path'], width=300)
    st.write(movie_details['overview'])

    # Show similar movies based on selected movie
    recommended_movies = recommend_movie(movie_details['title'], meta, similarity_matrix)
    st.subheader("Recommended Movies")
    
    # Display recommended movies in a grid layout
    rec_cols = st.columns(4)
    for idx, rec_movie in recommended_movies.iterrows():
        with rec_cols[idx % 4]:
            st.markdown(f"""
                <div class="movie-card">
                    <img src="{"http://image.tmdb.org/t/p/w185" + rec_movie['poster_path']}" width="100%" alt="{rec_movie['title']}"/>
                    <div class="movie-title">{rec_movie['title']}</div>
                    <div>{rec_movie['overview']}</div>
                </div>
            """, unsafe_allow_html=True)

    # Back to home button
    if st.button("Home"):
        st.session_state.page = "home"