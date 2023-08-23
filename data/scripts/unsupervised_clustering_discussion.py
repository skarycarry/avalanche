import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('omw-1.4')

stop_words = stopwords.words('english')
lemmatizer = WordNetLemmatizer()

# load the dataset into a Pandas DataFrame
data = pd.read_csv('../inputs/ratings_data.csv')

data['Discussion'] = data['Discussion'].astype(str)

# define the text preprocessing function
def preprocess_text(text):
    # remove non-alphanumeric characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    # convert to lowercase
    text = text.lower()
    
    # tokenize the text
    tokens = nltk.word_tokenize(text)
    
    # remove stop words and lemmatize the tokens
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    
    # join the tokens back into a string
    text = ' '.join(tokens)
    
    return text

# apply text preprocessing to the DataFrame
data['text'] = data['Discussion'].apply(preprocess_text)

# vectorize the text data using TfidfVectorizer
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(data['text'])

# find the optimal number of clusters using elbow method
scores = []
max_clusters = 10
for n in range(2, max_clusters):
    kmeans = KMeans(n_clusters=n, random_state=42)
    kmeans.fit(X)
    scores.append(silhouette_score(X, kmeans.labels_))

optimal_clusters = np.argmax(scores) + 2  # add 2 to start from 2 clusters

# perform unsupervised clustering using KMeans
kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
kmeans.fit(X)
labels = kmeans.labels_

# print the most unique features of each group
feature_names = vectorizer.get_feature_names_out()
for i in range(optimal_clusters):
    print(f'Cluster {i}:')
    cluster_features = X[labels == i].mean(axis=0).tolist()[0]
    sorted_features_indices = sorted(range(len(cluster_features)), key=lambda k: cluster_features[k], reverse=True)
    for j in range(10):
        print(f'\t{feature_names[sorted_features_indices[j]]}: {cluster_features[sorted_features_indices[j]]:.3f}')
