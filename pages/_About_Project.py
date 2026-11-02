
import streamlit as st

st.set_page_config(page_title="About CineMatch", page_icon="ℹ️")

st.title("ℹ️ About CineMatch")

st.write("""
CineMatch is a Movie Recommendation System built using Python
and Machine Learning.

The project recommends movies based on the similarity of
their content, including genres, keywords, cast and overview.
""")

st.subheader("Technologies Used")

st.markdown("""
- Python
- Pandas
- Scikit-learn
- Streamlit
- TMDB 5000 Movie Dataset
""")

st.subheader("Machine Learning Algorithm")

st.write("""
1. Data preprocessing
2. Feature extraction using CountVectorizer
3. Cosine Similarity
4. Movie recommendation
""")

st.subheader("Project Objective")

st.write("""
The objective is to help users discover movies they may enjoy
based on the content of a movie they select.
""")

st.success("Thank you for using CineMatch! 🎬")
