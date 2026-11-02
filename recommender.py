
import pandas as pd
import ast

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:

    def __init__(self):

        # Load datasets
        movies = pd.read_csv("data/tmdb_5000_movies.csv")
        credits = pd.read_csv("data/tmdb_5000_credits.csv")

        # Remove duplicate title column from credits
        credits = credits.drop(
            columns=["title"],
            errors="ignore"
        )

        # Merge movies and credits
        self.movies = movies.merge(
            credits,
            left_on="id",
            right_on="movie_id",
            how="inner"
        )

        # Clean missing titles
        self.movies = self.movies.dropna(
            subset=["title"]
        ).reset_index(drop=True)

        # Convert genres into names
        self.movies["genres"] = self.movies["genres"].apply(
            self.get_names
        )

        # Convert keywords into names
        self.movies["keywords"] = self.movies["keywords"].apply(
            self.get_names
        )

        # Extract top 3 cast members
        self.movies["cast"] = self.movies["cast"].apply(
            lambda x: self.get_names(x)[:3]
        )

        # Extract directors
        self.movies["crew"] = self.movies["crew"].apply(
            self.get_director
        )

        # Handle missing overview
        self.movies["overview"] = (
            self.movies["overview"].fillna("")
        )

        # Create combined tags
        self.movies["tags"] = self.movies.apply(
            self.create_tags,
            axis=1
        )

        # Convert text into numerical vectors
        self.vectorizer = CountVectorizer(
            max_features=5000,
            stop_words="english"
        )

        self.vectors = self.vectorizer.fit_transform(
            self.movies["tags"]
        )

    # Convert JSON text into list of names
    def get_names(self, text):

        try:
            data = ast.literal_eval(text)

            if isinstance(data, list):
                return [
                    item["name"]
                    for item in data
                    if isinstance(item, dict) and "name" in item
                ]

            return []

        except (ValueError, TypeError, SyntaxError):
            return []

    # Find movie director
    def get_director(self, text):

        try:
            data = ast.literal_eval(text)

            if isinstance(data, list):
                for person in data:

                    if (
                        isinstance(person, dict)
                        and person.get("job") == "Director"
                    ):
                        return [person["name"]]

            return []

        except (ValueError, TypeError, SyntaxError):
            return []

    # Combine movie features
    def create_tags(self, row):

        tags = (
            str(row["overview"]) + " "
            + " ".join(row["genres"]) + " "
            + " ".join(row["keywords"]) + " "
            + " ".join(row["cast"]) + " "
            + " ".join(row["crew"])
        )

        return tags.lower()

    # Return movie titles
    def get_movies(self):

        return sorted(
            self.movies["title"].dropna().unique().tolist()
        )

    # Recommend similar movies
    def recommend(self, movie_name, number=5):

        matches = self.movies[
            self.movies["title"].str.lower() == movie_name.lower()
        ]

        if matches.empty:
            return pd.DataFrame()

        movie_index = matches.index[0]

        # Calculate cosine similarity
        similarity = cosine_similarity(
            self.vectors[movie_index],
            self.vectors
        ).flatten()

        # Sort similarity scores
        similar_indices = similarity.argsort()[::-1]

        recommendations = []

        for index in similar_indices:

            if index != movie_index:
                recommendations.append(index)

            if len(recommendations) == number:
                break

        result = self.movies.iloc[recommendations].copy()

        result["similarity"] = similarity[recommendations]

        return result

    # Get all genres
    def get_genres(self):

        genres = set()

        for genre_list in self.movies["genres"]:
            genres.update(genre_list)

        return sorted(genres)

    # Get top-rated movies
    def get_top_rated(self, number=20):

        return (
            self.movies[
                self.movies["vote_count"] >= 100
            ]
            .sort_values(
                "vote_average",
                ascending=False
            )
            .head(number)
        )

    # Get movies by genre
    def get_by_genre(self, genre):

        return self.movies[
            self.movies["genres"].apply(
                lambda genres: genre in genres
            )
        ].sort_values(
            "vote_average",
            ascending=False
        )
