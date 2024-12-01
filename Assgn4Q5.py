import re
import math
from pymongo import MongoClient
from collections import defaultdict, Counter
from sklearn.feature_extraction.text import TfidfVectorizer

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.search_engine
documents_collection = db.documents
terms_collection = db.terms

# Helper functions
def preprocess(text):
    """Lowercase and remove punctuation."""
    return re.sub(r'[^\w\s]', '', text.lower())

def tokenize(text):
    """Generate unigrams, bigrams, and trigrams."""
    tokens = text.split()
    unigrams = tokens
    bigrams = [' '.join(tokens[i:i+2]) for i in range(len(tokens)-1)]
    trigrams = [' '.join(tokens[i:i+3]) for i in range(len(tokens)-2)]
    return unigrams + bigrams + trigrams

# Step 1: Insert Documents
documents = [
    "After the medication, headache and nausea were reported by the patient.",
    "The medication caused a headache and nausea, but no dizziness was reported.",
    "Headache and dizziness are common effects of this medication.",
    "Dizziness and nausea are common side effects reported by the patient after taking this medication."
]

documents_collection.delete_many({})
for i, doc in enumerate(documents, 1):
    documents_collection.insert_one({"_id": i, "content": preprocess(doc)})

# Step 2: Build Inverted Index
terms_collection.delete_many({})
vocabulary = {}
inverted_index = defaultdict(list)

for doc in documents_collection.find():
    doc_id = doc['_id']
    tokens = tokenize(doc['content'])
    token_counts = Counter(tokens)
    
    for term, count in token_counts.items():
        if term not in vocabulary:
            vocabulary[term] = len(vocabulary) + 1
        term_id = vocabulary[term]
        inverted_index[term].append({"doc_id": doc_id, "tf": count})

for term, docs in inverted_index.items():
    idf = math.log(len(documents) / len(docs))
    for doc in docs:
        doc['tf-idf'] = doc['tf'] * idf
    terms_collection.insert_one({"_id": vocabulary[term], "term": term, "pos": vocabulary[term], "docs": docs})

# Step 3: Rank Documents
def rank_documents(query):
    """Rank documents using vector space model."""
    query_tokens = tokenize(preprocess(query))
    query_vector = defaultdict(float)
    
    for token in query_tokens:
        if token in vocabulary:
            term_data = terms_collection.find_one({"term": token})
            idf = math.log(len(documents) / len(term_data['docs']))
            query_vector[token] += idf
    
    scores = defaultdict(float)
    
    for token, q_weight in query_vector.items():
        term_data = terms_collection.find_one({"term": token})
        for doc in term_data['docs']:
            scores[doc['doc_id']] += q_weight * doc['tf-idf']
    
    ranked_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [(documents[doc_id - 1], score) for doc_id, score in ranked_docs]

# Queries
queries = {
    "q1": "nausea and dizziness",
    "q2": "effects",
    "q3": "nausea was reported",
    "q4": "dizziness",
    "q5": "the medication"
}

# Output results
for qid, query in queries.items():
    print(f"Results for Query {qid}: {query}")
    results = rank_documents(query)
    for content, score in results:
        print(f'"{content}", {score:.2f}')
    print()
