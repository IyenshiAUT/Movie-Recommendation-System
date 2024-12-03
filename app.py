import streamlit as st
import pickle
import requests


# Load preprocessed data: movies and similarity matrix
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Extract movie titles for the dropdown list
movies_list = movies['title'].values

# Streamlit header for the web app
st.header("Movie Recommendation System")

# Dropdown for selecting a movie
selected_value = st.selectbox('Select the movie you prefer from below', movies_list)


# Function to fetch movie posters from The Movie Database (TMDb) API
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=c243a1b2c7b12ec533d9e262259e2c0e&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
    return full_path
    

# Function to recommend movies based on the selected movie
def recommend(movies_collection):
    index = movies[movies['title']==movies_collection].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    recommend_list = []
    recommend_poster_list = []
    for i in distance[0:5]:
        recommend_poster_list.append(fetch_poster(movies.iloc[i[0]].id))
        recommend_list.append(movies.iloc[i[0]].title)
    return recommend_list, recommend_poster_list


# Button to trigger recommendations
if st.button('Show Recommended Movies'):
    recommended_movies, recommend_poster_list = recommend(selected_value)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
       st.text(recommended_movies[0])
       st.image(recommend_poster_list[0])
    with col2:
       st.text(recommended_movies[1])
       st.image(recommend_poster_list[1])
    with col3:
       st.text(recommended_movies[2])
       st.image(recommend_poster_list[2])
    with col4:
       st.text(recommended_movies[3])
       st.image(recommend_poster_list[3])
    with col5:
       st.text(recommended_movies[4])
       st.image(recommend_poster_list[4])