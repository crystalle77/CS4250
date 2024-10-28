#-------------------------------------------------------------------------
# AUTHOR: your name
# FILENAME: title of the source file
# SPECIFICATION: description of the program
# FOR: CS 4250- Assignment #1
# TIME SPENT: 1 hr because I had the algorithm down which made it easier
#-----------------------------------------------------------*/

#Importing some Python libraries
import csv
from math import log10

documents = []

#Reading the data in a csv file
with open('collection.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
         if i > 0:  # skipping the header
            documents.append (row[0])
print(documents)
#Conducting stopword removal for pronouns/conjunctions. Hint: use a set to define your stopwords.
#--> add your Python code here
stopWords = {"I", "She", "her", "They", "their", "and"}

cleaned_documents = []
for line in documents:
    # Split the sentence into words
    words = line.split()
    
    # Remove the words that are in stopWords
    cleaned_words = [word for word in words if word not in stopWords]
    cleaned_line = " ".join(cleaned_words)
    cleaned_documents.append(cleaned_line)

print("After stopwords")
for line in cleaned_documents:
    print(line)

#Conducting stemming. Hint: use a dictionary to map word variations to their stem.
#--> add your Python code here
#steeming = {?}
stemmed_documents = []

stemming_dict = {
    "love": "love",
    "loves": "love",
    "dog": "dog",
    "dogs": "dog",
    "cat": "cat",
    "cats": "cat"
}


stemmed_documents = []
for line in cleaned_documents:
    words = line.split()
    # Apply stemming using the stemming dictionary
    stemmed_words = [stemming_dict.get(word, word) for word in words]
    stemmed_line = " ".join(stemmed_words)
    stemmed_documents.append(stemmed_line)

print("\nAfter Stemming:")
for line in stemmed_documents:
    print(line)

#Identifying the index terms.
#--> add your Python code here
#terms = []
index_terms = set()
for doc in stemmed_documents:
    index_terms.update(doc.split())
index_terms = sorted(list(index_terms))  # Sort the terms alphabetically

print("\nIndex Terms:", index_terms)

#Building the document-term matrix by using the tf-idf weights.
#--> add your Python code here

def compute_tf(term, doc):
    words = doc.split()
    return words.count(term) / len(words)

# Step 6: IDF Calculation (Inverse Document Frequency)
def compute_idf(term, docs):
    idf = 0
    total_docs = len(docs)
    num_docs_containing_term = sum(1 for doc in docs if term in doc.split())
    
    # Avoid division by zero if term doesn't appear in any documents
    if num_docs_containing_term > 0:
        idf = log10(total_docs / num_docs_containing_term)
        return idf
    else:
        return idf  # if the term doesn't appear in any documents# Creating the document-term matrix
docTermMatrix = []

for doc in stemmed_documents:
    tf_idf_scores = []
    for term in index_terms:
        tf = compute_tf(term, doc)
        print(term , "tf: " , tf)
        idf = compute_idf(term, stemmed_documents)
        print(term , "idf " , idf)
        tf_idf_scores.append(round(tf * idf, 5))
    docTermMatrix.append(tf_idf_scores)


#Printing the document-term matrix.
# Step 8: Print the Document-Term Matrix
print("\nTF-IDF Document-Term Matrix:")
print("\t", "\t".join(index_terms))
for i, scores in enumerate(docTermMatrix, start=1):
    print(f"d{i}\t" + "\t".join(map(str, scores)))

