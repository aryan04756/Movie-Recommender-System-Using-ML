import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch a movie's poster
def fetch_poster(movie_id, api_key):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'poster_path' in data:
            return "https://image.tmdb.org/t/p/original" + data['poster_path']
        else:
            return None  # Return None if poster path not found
    else:
        return None  # Return None in case of an error

# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Recommendation function
def recommend(movie, api_key):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        poster_url = fetch_poster(movie_id, api_key)
        if poster_url:
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_posters.append(poster_url)
    
    return recommended_movies, recommended_movies_posters

# Streamlit app
def main():
    st.title('Movie Recommender System')
    selected_movie_name = st.selectbox(
        'Select a movie:',
        movies['title'].values)
    
    api_key = "ed7e744d0da49c800daba4d4622df471"
    
    if st.button('Recommend'):
        names, posters = recommend(selected_movie_name, api_key)
        
        if names and posters:
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.text(names[0])
                st.image(posters[0])

            with col2:
                st.text(names[1])
                st.image(posters[1])

            with col3:
                st.text(names[2])
                st.image(posters[2])

            with col4:
                st.text(names[3])
                st.image(posters[3])

            with col5:
                st.text(names[4])
                st.image(posters[4])

if __name__ == "__main__":
    main()
