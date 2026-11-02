
import streamlit as st
from recommender import MovieRecommender

st.set_page_config(page_title="Top Rated Movies", page_icon="⭐")

@st.cache_resource
def load_model():
    return MovieRecommender()

model = load_model()

st.title("⭐ Top Rated Movies")
st.write("Explore the highest-rated movies.")

top_movies = model.get_top_rated(30)

for _, movie in top_movies.iterrows():
    st.subheader(movie["title"])
    st.write("⭐ Rating:", movie["vote_average"], "/10")
    st.write(movie["overview"])
    st.divider()
