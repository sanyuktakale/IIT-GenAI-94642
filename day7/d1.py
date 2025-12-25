# cmd> pip install sentence-transformers torch
#This code converts sentences into numerical vectors (embeddings) using a pre-trained language model
#  and then measures how similar two sentences are using cosine similarity.

from sentence_transformers import SentenceTransformers
import pandas as pd

# Define cosine similarity function
#cosine similarity=A.B/||A||*||B||
def cosine_similarity(x,y):
    return np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y))

#Load pre-trained embedding model
embed_model=SentenceTransformer("text-embedding-nomic-embed-text-v1.5")

#input sentences 
sentences=["I love programming.","Coding is my passion."]

#convert sentence into embeddings
embeddings=embed_model.encode(sentences)

#print embedding length
for embd_vect in embeddings:
    print (len(embd_vect))

# print similarity
print("cosine similarity between sentences: ",cosine_similarity(embeddings[0],embeddings[1]))




