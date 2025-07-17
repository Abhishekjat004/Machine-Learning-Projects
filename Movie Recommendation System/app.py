import pickle 
import streamlit as st
import requests


def fetch_poster(movie_id):
    url = f"http://www.omdbapi.com/?i={movie_id}&apikey=YOUR_API_KEY"
    response = requests.get(url)
    data = response.json()
    
    # Debug output
    print(data)

    # Check for valid response and Poster key
    if data.get('Response') == 'True' and 'Poster' in data and data['Poster'] != 'N/A':
        return data['Poster']
    else:
        # If Poster not available, return placeholder
        return "https://via.placeholder.com/500x750?text=No+Image+Available"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[0:10]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].imdb_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System Using Machine Learning')
movies = pickle.load(open('unsafe_data/movie_lists.pkl', 'rb'))
similarity = pickle.load(open('unsafe_data/similarity.pkl', 'rb'))


movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# if st.button('Show Recommendation'):


if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)

    # First row: 5 columns
    cols1 = st.columns(5)
    for i in range(5):
        with cols1[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])

    # Second row: 5 columns
    cols2 = st.columns(5)
    for i in range(5, 10):
        with cols2[i - 5]:  # index reset for second row
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
