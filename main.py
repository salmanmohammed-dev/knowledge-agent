import string
import math
from sentence_transformers import SentenceTransformer

documents = ["java.txt", "spring.txt", "database.txt"]

knowledge_base = []

for doc in documents:
    path = "documents/" + doc

    with open(path, "r") as file:
        content = file.read()

    document = {
        "name": doc,
        "content": content
    }

    knowledge_base.append(document)

print("Documents loaded:", len(knowledge_base))

for document in knowledge_base:
    print(document["name"])

chunks = []

for document in knowledge_base:
    sentences = document["content"].split(".")

    for index, sentence in enumerate(sentences):
        sentence = sentence.strip()

        if sentence:
            chunk = {
                "document": document["name"],
                "chunk_id": index,
                "text": sentence
            }

            chunks.append(chunk)

print("\nTotal chunks:", len(chunks))

for chunk in chunks:
    print(chunk)


def search(query, chunks, top_k):
    query_words = query.lower().translate(
        str.maketrans("", "", string.punctuation)
    ).split()

    search_results = []

    for chunk in chunks:
        chunk_words = chunk["text"].lower().translate(
            str.maketrans("", "", string.punctuation)
        ).split()

        score = 0

        for word in query_words:
            if word in chunk_words:
                score += 1

        if score > 0:
            result = {
                "chunk": chunk,
                "score": score
            }

            search_results.append(result)

    search_results.sort(
        key=lambda result: result["score"],
        reverse=True
    )

    return search_results[:top_k]


query = "What makes database queries faster?"

results = search(query, chunks, 2)

print("\nSearch results:")

for result in results:
    print(result)


def cosine_similarity(vector_a, vector_b):
    dot_product = 0

    for i in range(len(vector_a)):
        dot_product += vector_a[i] * vector_b[i]

    sum_squares_a = 0

    for i in range(len(vector_a)):
        sum_squares_a += vector_a[i] * vector_a[i]

    magnitude_a = math.sqrt(sum_squares_a)

    sum_squares_b = 0

    for i in range(len(vector_b)):
        sum_squares_b += vector_b[i] * vector_b[i]

    magnitude_b = math.sqrt(sum_squares_b)

    return dot_product / (magnitude_a * magnitude_b)


model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

for chunk in chunks:
    chunk["embedding"] = model.encode(chunk["text"])


def semantic_search(query, chunks, model, top_k):
    query_embedding = model.encode(query)

    search_results = []

    for chunk in chunks:
        similarity = cosine_similarity(
            query_embedding,
            chunk["embedding"]
        )

        result = {
            "chunk": chunk,
            "similarity": similarity
        }

        search_results.append(result)

    search_results.sort(
        key=lambda result: result["similarity"],
        reverse=True
    )

    return search_results[:top_k]


semantic_search_results = semantic_search(query, chunks, model, 2)

print("\nSemantic search results:")

for result in semantic_search_results:
    print(result["chunk"]["text"])
    print("similarity:", result["similarity"])
