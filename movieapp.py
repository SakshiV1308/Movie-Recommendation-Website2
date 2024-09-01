import streamlit as st
import pandas as pd
import pickle
import requests


# Function to fetch movie poster from TMDb API
def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US')
        response.raise_for_status()  # Check for request errors
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750.png?text=No+Image+Available"  # Placeholder image if no poster is found
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster: {e}")
        return None


# Function to recommend movies based on similarity
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        poster = fetch_poster(movie_id)
        if poster:
            recommended_movies_posters.append(poster)
        else:
            recommended_movies_posters.append("https://via.placeholder.com/500x750.png?text=No+Image+Available")

    return recommended_movies, recommended_movies_posters


# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title("Movie Recommender System")

# Selectbox for movie selection
option = st.selectbox(
    "Select a movie to get recommendations:",
    movies['title'].values)

# Button to trigger recommendations
if st.button("Recommend"):
    names, posters = recommend(option)

    # Display recommended movies and their posters in columns
    cols = st.columns(5)
    for i, col in enumerate(cols):
        if i < len(names):
            col.text(names[i])
            col.image(posters[i])
        else:
            col.empty()
