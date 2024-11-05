import streamlit as st
import pandas as pd
from utils import load_data, preprocess_data, compute_similarity, recommend_movie, create_user, authenticate_user
import warnings

# Load and preprocess data
meta = load_data()
meta, mlb, overview_df = preprocess_data(meta)
similarity_matrix = compute_similarity(meta, mlb, overview_df)

# Set page config for better visuals
st.set_page_config(page_title="Movie Recommendation System", layout="wide")  

# Define custom CSS for styling  
home_page_css = """  
<style>  
    body {  
        background-color: #2f2f2f;  
        color: #fff;  
        font-family: 'Roboto', sans-serif;  
    }  
    .main {  
        padding: 20px;  
    }  
    .movie-card {  
        position: relative;  
        background: #333;  
        border-radius: 10px;  
        padding: 15px;  
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);  
        text-align: center;  
        margin: 15px;  
        transition: transform 0.3s ease, box-shadow 0.3s ease;  
        cursor: pointer;  
        overflow: hidden;  
    }  
    .movie-card:hover {  
        transform: scale(1.05);  
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);  
    }  
    .movie-image {  
        width: 100%;  
        height: auto;  
        border-radius: 10px;  
        max-height: 300px;  
        object-fit: cover;  
    }  
    .movie-title {  
        font-weight: bold;  
        font-size: 16px;  
        color: #007bff;  
        margin-top: 10px;  
    }  
    .movie-overview, .movie-genres {  
        font-size: 14px;  
        color: #666;  
        margin-top: 10px;  
        display: none;  /* Initially hidden */  
    }  
    .movie-card:hover .movie-overview,  
    .movie-card:hover .movie-genres,  
    .movie-card:hover .know-more-button {  
        display: block;  /* Show on hover */  
    }  
    .know-more-button {  
        margin-top: 10px;  
        padding: 8px 16px;  
        font-size: 14px;  
        color: white;  
        background-color: #007bff;  
        border: none;  
        border-radius: 5px;  
        cursor: pointer;  
    }  
</style>  
"""  
st.markdown(home_page_css, unsafe_allow_html=True)   
# Handle query parameters
def handle_query_params():
    params = st.experimental_get_query_params()
    if 'page' in params and 'movie_title' in params:
        st.session_state.page = params['page'][0]
        st.session_state.selected_movie = meta[meta['title'] == params['movie_title'][0]].iloc[0]

# Call the function to handle the query parameters
handle_query_params()

# Streamlit app layout
st.title("MovieNights")

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
    # Logout button at the top of the page
    if st.button("Log Out"):
        st.session_state.user = None
        st.session_state.page = "sign_in"

    # Home page display logic  
if st.session_state.page == "home" and st.session_state.user is not None:  
    st.subheader("Top Movies Based on Your Genres")  
    selected_genres = st.session_state.genres.split(',')  
    filtered_movies = meta[meta['genres'].apply(lambda x: any(genre in x for genre in selected_genres))]  
    top_movies = filtered_movies.sort_values(by='vote_average', ascending=False).head(20)  

    cols = st.columns(4)  
    for index, row in top_movies.iterrows():  
        with cols[index % 4]:  
            # Create a clickable movie card with hover effects  
            st.markdown(f"""  
            <div class="movie-card">  
                <img src="http://image.tmdb.org/t/p/w185{row['poster_path']}" class="movie-image" alt="{row['title']}"/>  
                <div class="movie-title">{row['title']}</div>  
                <div class="movie-overview">{row['overview']}</div>  
                <div class="movie-genres">{', '.join(row['genres'])}</div>  
                <a href="?page=movie_details&movie_title={row['title']}">
                    <button class="know-more-button">Know More</button>
                </a>
            </div>  
            """, unsafe_allow_html=True)  

# Movie Details Page Logic  
elif st.session_state.page == "movie_details" and st.session_state.selected_movie is not None:  
    movie_details = st.session_state.selected_movie  
    st.subheader(movie_details['title'])  
    st.image("http://image.tmdb.org/t/p/w500" + movie_details['poster_path'], width=300)  
    st.write(movie_details['overview'])  

    # Show recommended movies based on selected movie  
    recommended_movies = recommend_movie(movie_details['title'], meta, similarity_matrix)  
    st.subheader("Recommended Movies")  

    rec_cols = st.columns(4)  
    for idx, rec_movie in recommended_movies.iterrows():  
        with rec_cols[idx % 4]:  
            st.markdown(f"""  
                <div class="movie-card">  
                    <img src="http://image.tmdb.org/t/p/w185{rec_movie['poster_path']}" class="movie-image" alt="{rec_movie['title']}"/>  
                    <div class="movie-title">{rec_movie['title']}</div>  
                    <div class="movie-overview">{rec_movie['overview']}</div>  
                    <a href="?page=movie_details&movie_title={rec_movie['title']}">
                        <button class="know-more-button">Know More</button>
                    </a>
                </div>  
            """, unsafe_allow_html=True)  

    # Back to home button  
    if st.button("Home"):  
        st.session_state.page = "home"