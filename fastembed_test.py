from fastembed import TextEmbedding
import numpy as np

# Example sentences
sentences = [
    "Artificial Intelligence is transforming education.",
    "Machine learning is a subset of AI.",
]

# Generate embeddings using FastEmbed
embedding_model = TextEmbedding()
embeddings = embedding_model.embed(sentences)

# Normalize embeddings (if needed, though they should be normalized by default)
print(embeddings)
