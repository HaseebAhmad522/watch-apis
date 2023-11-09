from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from .models import Watch

# Create your views here.


def get_top_recommendations(self, user_query):
        # Your recommendation function implementation here
        # Initialize the TF-IDF vectorizer with the entire dataset
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(Watch.objects.values_list('title', flat=True))

        # Calculate cosine similarity between the user query and all items in the dataset
        user_query_vector = tfidf_vectorizer.transform([user_query])
        cosine_sim = linear_kernel(user_query_vector, tfidf_matrix)

        # Get the indices of items sorted by similarity in descending order
        indices = cosine_sim[0].argsort()[::-1]

        # Find the index with the highest similarity (excluding the first, which is the query itself)
        max_similarity_index = cosine_sim[0][1:].argmax() + 1

        # Check if the highest similarity is below a threshold and shuffle the indices
        if cosine_sim[0][max_similarity_index] < 0.00001:
            np.random.shuffle(indices)

        # Get the top 10 recommendations (excluding the query itself)
        top_indices = indices[1:50]

        return Watch.objects.filter(pk__in=top_indices)