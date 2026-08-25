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