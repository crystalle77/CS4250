from pymongo import MongoClient
import string
import math
from collections import Counter

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Update connection string if needed
db = client.search_engine
terms_collection = db.terms
documents_collection = db.documents

# Documents (from Question 3)
documents = [
    "After the medication, headache and nausea were reported by the patient.",
    "The patient reported nausea and dizziness caused by the medication.",
    "Headache and dizziness are common effects of this medication.",
    "The medication caused a headache and nausea, but no dizziness was reported."
]

# Tokenization function
def tokenize(text):
    text = text.lower().translate(str.maketrans("", "", string.punctuation))
    words = text.split()
    unigrams = words
    bigrams = [" ".join(words[i:i+2]) for i in range(len(words)-1)]
    trigrams = [" ".join(words[i:i+3]) for i in range(len(words)-2)]
    return unigrams + bigrams + trigrams

# Create collections
terms_collection.drop()
documents_collection.drop()

# Populate documents collection
for i, content in enumerate(documents, start=1):
    documents_collection.insert_one({"_id": i, "content": content})

# Build inverted index
vocab = {}
for doc_id, content in enumerate(documents, start=1):
    tokens = tokenize(content)
    term_freq = Counter(tokens)
    for term, freq in term_freq.items():
        if term not in vocab:
            vocab[term] = len(vocab) + 1
        pos = vocab[term]
        tf = 1 + math.log(freq)  # TF calculation
        idf = math.log(len(documents) / sum(term in tokenize(d) for d in documents))  # IDF calculation
        tf_idf = tf * idf
        terms_collection.update_one(
            {"_id": pos},
            {"$set": {"pos": pos}, "$push": {"docs": {"doc_id": doc_id, "tf_idf": tf_idf}}},
            upsert=True
        )

# Define queries
queries = [
    "nausea and dizziness",
    "effects",
    "nausea was reported",
    "dizziness",
    "the medication"
]

# Process queries and compute scores
def compute_scores(query):
    query_tokens = tokenize(query)
    scores = Counter()
    for token in query_tokens:
        term = terms_collection.find_one({"_id": vocab.get(token)})
        if term:
            for doc in term["docs"]:
                scores[doc["doc_id"]] += doc["tf_idf"]
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

# Output results
results = {}
for i, query in enumerate(queries, start=1):
    scores = compute_scores(query)
    results[f"q{i}"] = [
        {"content": documents[doc_id - 1], "score": score}
        for doc_id, score in scores
    ]

# Print the results for each query
for query_id, ranked_docs in results.items():
    print(f"Results for {query_id}:")
    for doc in ranked_docs:
        print(f"Document: {doc['content']}, Score: {doc['score']}")
