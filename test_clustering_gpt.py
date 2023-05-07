import openai
import pandas as pd
import numpy as np
import re
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import json


# API key for OpenAI GPT-3
openai.api_key = "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"


# GPT-3 function to preprocess text data
def preprocess_text(text):
    # Define the data payload as a dictionary
    data = {
        "prompt": text,
        "max_tokens": 1024,
        "n": 1,
        "stop": None,
        "temperature": 0.5
    }

    # Convert the data payload to a JSON string
    payload = json.dumps(data)

    # Send the API request with the JSON payload
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=payload
    )

    # Extract the cleaned text from the API response
    cleaned_text = response.choices[0].text.strip()

    return cleaned_text


# Load data into pandas dataframe
data = pd.read_csv("data/ratings_data.csv")

# Preprocess text column using GPT-3
preprocessed_data = data["Discussion"].apply(preprocess_text)

# Apply TF-IDF vectorization
tfidf_vectorizer = TfidfVectorizer(stop_words="english")
tfidf_data = tfidf_vectorizer.fit_transform(preprocessed_data)

# Reduce dimensionality using PCA
pca = PCA(n_components=2, random_state=42)
pca_data = pca.fit_transform(tfidf_data.toarray())

# Determine optimal number of clusters using elbow method
wcss = []
for i in range(1, 11):
   kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=42)
   kmeans.fit(pca_data)
   wcss.append(kmeans.inertia_)
plt.plot(range(1, 11), wcss)
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

# Fit KMeans clustering algorithm to data
num_clusters = 4 # Replace with elbow method's number of clusters
kmeans = KMeans(n_clusters=num_clusters, init='k-means++', max_iter=300, n_init=10, random_state=42)
kmeans.fit(pca_data)
labels = kmeans.labels_

# Evaluate clustering performance using silhouette score
score = silhouette_score(pca_data, labels)
print("Silhouette Score: {}".format(score))

# Identify and print common features of each cluster
cluster_features = {}
for i in range(num_clusters):
    indices = np.where(labels == i)[0]
    cluster_data = data.iloc[indices]
    feature_counts = np.asarray(tfidf_data[indices,:].sum(axis=0)).ravel().tolist()
    feature_names = tfidf_vectorizer.get_feature_names()
    feature_dict = dict(zip(feature_names, feature_counts))
    sorted_features = sorted(feature_dict.items(), key=lambda x: x[1], reverse=True)[:10]
    cluster_features["Cluster " + str(i)] = sorted_features
    
for key, value in cluster_features.items():
    print(key + ":", value)