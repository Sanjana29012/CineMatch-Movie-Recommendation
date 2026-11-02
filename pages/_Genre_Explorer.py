
import streamlit as st
from recommender import MovieRecommender

st.set_page_config(page_title="Genre Explorer", page_icon="🎭")

@st.cache_resource
def load_model():
    return MovieRecommender()

model = load_model()

st.title("🎭 Genre Explorer")
st.write("Find movies according to your favourite genre.")

genres = model.get_genres()

selected_genre = st.selectbox(
    "Select a genre",
    genres
)

if st.button("Show Movies"):
    genre_movies = model.get_by_genre(selected_genre)

    st.subheader(f"{selected_genre} Movies")

    for _, movie in genre_movies.head(30).iterrows():
        st.subheader(movie["title"])
        st.write("⭐ Rating:", movie["vote_average"], "/10")
        st.write(movie["overview"])
        st.divider()
