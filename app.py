import streamlit as st 
import pickle
import pandas as pd
from fuzzywuzzy import process
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=d61ed2c05d73c1039808b10af3449cd6".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data["poster_path"]
    full_path = "https://image.tmdb.org/t/p/w500" + poster_path
    return full_path

def recommend(movie_title):
    # Find the closest match in the movies dataset
    best_match, score, _ = process.extractOne(movie_title, movies['title'])
    
    if score < 70:  # You can adjust the threshold as needed
        print("No close match found.")
        return
    
    # Get the index of the closest match
    movie_index = movies[movies["title"] == best_match].index[0]
    
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

# Streamlit UI
st.title("CineExplorer")
st.write("### Find movies similar to your favorite movie!")
st.write("")
movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list,
    on_change=lambda: st.session_state.update({"trigger": True})  # Trigger recommendation on change
)

# Check if "Show Recommendation" button is pressed or Enter key is triggered
if st.session_state.get("trigger", False) or st.button('Show Recommendation'):
    st.session_state["trigger"] = False  # Reset trigger
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])