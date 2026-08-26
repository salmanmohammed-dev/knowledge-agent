import string

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
