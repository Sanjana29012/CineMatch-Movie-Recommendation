
import streamlit as st
import pandas as pd
from recommender import MovieRecommender

st.set_page_config(
    page_title="CineMatch - Movie Recommendation",
    page_icon="🎬",
    layout="wide"
)

# Load recommendation system
@st.cache_resource
def load_model():
    return MovieRecommender()

try:
    model = load_model()
    movies = model.movies
except Exception as e:
    st.error(f"Unable to load movie dataset: {e}")
    st.stop()

# Header
st.title("🎬 CineMatch")
st.subheader("Discover your next favourite movie!")
st.write(
    "Select a movie and our recommendation system "
    "will suggest movies with similar genres, cast and story."
)

st.divider()

# Movie selection
movie_list = model.get_movies()

selected_movie = st.selectbox(
    "🎥 Choose a movie",
    movie_list
)

if st.button("✨ Recommend Movies", type="primary"):
    recommendations = model.recommend(selected_movie, 5)

    st.subheader("🎯 Movies Recommended for You")

    if recommendations.empty:
        st.warning("No recommendations found.")
    else:
        columns = st.columns(5)

        for column, (_, movie) in zip(
            columns, recommendations.iterrows()
        ):
            with column:
                poster = movie.get("poster_path")

                if pd.notna(poster) and poster:
                    st.image(
                        "https://image.tmdb.org/t/p/w500" + poster,
                        use_container_width=True
                    )
                else:
                    st.info("🎬 No poster available")

                st.markdown(f"**{movie['title']}**")

                st.write(
                    f"⭐ Rating: {movie['vote_average']}/10"
                )

                st.caption(
                    str(movie["overview"])[:150] + "..."
                )

st.divider()

# Project information
st.subheader("About CineMatch")

col1, col2, col3 = st.columns(3)

col1.metric("Movies Dataset", "5000+")
col2.metric("Recommendation Type", "Content-Based")
col3.metric("Algorithm", "Cosine Similarity")

st.info(
    "CineMatch uses movie descriptions, genres, keywords "
    "and cast information to recommend similar movies."
)
