import streamlit as st
import pickle
import requests

# Load data
movies = pickle.load(open('movies.pkl', 'rb'))          # This should be a DataFrame
similarity = pickle.load(open('similarity.pkl', 'rb'))  # This should be a 2D list or array

import requests

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=YOUR_API_KEY"
        response = requests.get(url)
        response.raise_for_status()  # raise exception for HTTP errors
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for movie ID {movie_id}: {e}")
        return "https://via.placeholder.com/500x750.png?text=Image+Unavailable"


def recommend(movie):
    # Find the index of the selected movie
    index = movies[movies['title'] == movie].index[0]

    # Get similarity scores
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    # Get top 5 recommended movies
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names,recommended_movie_posters

# Streamlit UI
st.title('Movie Recommender System')

movie_list = movies['title'].values
select_movie_name = st.selectbox('Select a movie to get recommendations:', movie_list)

if st.button('Recommend'):
    names, posters = recommend(select_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.header(names[0])
        st.image(posters[0])

    with col2:
        st.header(names[1])
        st.image(posters[1])

    with col3:
        st.header(names[2])
        st.image(posters[2])

    with col4:
        st.header(names[3])
        st.image(posters[3])
    with col5:
        st.header(names[4])
        st.image(posters[4])
