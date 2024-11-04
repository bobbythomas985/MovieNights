import pandas as pd
import os
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
# Define the path for the user data CSV
USER_DATA_CSV = 'user_data.csv'

def load_user_data():
    """Load user data from CSV, creating the file if it doesn't exist."""
    try:
        if not os.path.isfile(USER_DATA_CSV):
            user_data = pd.DataFrame(columns=['username', 'password', 'genres'])
            user_data.to_csv(USER_DATA_CSV, index=False)
            return user_data
        else:
            return pd.read_csv(USER_DATA_CSV)
    except PermissionError:
        st.error("Permission denied when accessing user_data.csv. Please close any open instances or check permissions.")
        return pd.DataFrame(columns=['username', 'password', 'genres'])

def load_data():
    """Load movie metadata from a CSV file."""
    return pd.read_csv('final.csv')  # Update with the actual path if needed

def load_user_data():
    """Load user data from CSV, creating the file if it doesn't exist."""
    if not os.path.isfile(USER_DATA_CSV):
        # Create a new DataFrame if the file does not exist
        user_data = pd.DataFrame(columns=['username', 'password', 'genres'])
        user_data.to_csv(USER_DATA_CSV, index=False)
        return user_data
    else:
        return pd.read_csv(USER_DATA_CSV)

def preprocess_data(meta):
    """Preprocess the movie metadata."""
    # Assuming 'genres' is a string representation of a list
    meta['genres'] = meta['genres'].apply(lambda x: eval(x) if isinstance(x, str) else [])
    
    # Use MultiLabelBinarizer to create dummy variables for genres
    mlb = MultiLabelBinarizer()
    genre_data = mlb.fit_transform(meta['genres'])
    
    # Creating a DataFrame for genre features
    genre_df = pd.DataFrame(genre_data, columns=mlb.classes_)
    
    # Combine with original metadata
    meta = pd.concat([meta, genre_df], axis=1)
    
    # Process overview or any other text fields as needed
    overview_df = meta['overview']
    
    return meta, mlb, overview_df

def compute_similarity(meta, mlb, overview_df):
    """Compute cosine similarity based on genres and other factors."""
    # Compute genre similarity
    genre_similarity = cosine_similarity(meta[mlb.classes_].values)
    
    # You can include more similarity calculations here (e.g., for overviews)
    # Return a combined similarity matrix or handle it as needed
    return genre_similarity

def recommend_movie(title, meta, similarity_matrix):
    """Recommend movies based on the title provided."""
    idx = meta[meta['title'] == title].index[0]
    similar_indices = similarity_matrix[idx].argsort()[::-1][1:6]  # Get top 5 similar movies
    return meta.iloc[similar_indices]

def create_user(username, password, genres):
    """Create a new user and save to CSV."""
    users = load_user_data()
    
    # Check if the username already exists
    if username in users['username'].values:
        return False  # User already exists

    # Add new user to DataFrame
    new_user = pd.DataFrame({'username': [username], 'password': [password], 'genres': [genres]})
    users = pd.concat([users, new_user], ignore_index=True)
    users.to_csv(USER_DATA_CSV, index=False)  # Save back to CSV
    return True

def authenticate_user(username, password):
    """Authenticate a user."""
    users = load_user_data()
    user = users[(users['username'] == username) & (users['password'] == password)]
    if not user.empty:
        return user.iloc[0],user['genres'].values[0]   # Return the first matching user
    return None,None