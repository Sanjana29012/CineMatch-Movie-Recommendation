
import streamlit as st
from recommender import MovieRecommender

st.set_page_config(page_title="Explore Movies", page_icon="🔎")

@st.cache_resource
def load_model():
    return MovieRecommender()

model = load_model()
movies = model.movies

st.title("🔎 Explore Movies")
st.write("Search and explore movies from our dataset.")

search = st.text_input("Search movie by name")

if search:
    results = movies[
        movies["title"].str.contains(search, case=False, na=False)
    ]

    st.write(f"Found {len(results)} movies")

    for _, movie in results.head(20).iterrows():
        st.subheader(movie["title"])
        st.write(movie["overview"])
        st.write("⭐ Rating:", movie["vote_average"])
        st.divider()
else:
    st.info("Enter a movie name to search.")
