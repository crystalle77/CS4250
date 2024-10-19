#-------------------------------------------------------------------------
# AUTHOR: Prerna Joshi
# FILENAME: title of the source file
# SPECIFICATION: description of the program
# FOR: CS 4250- Assignment #2
# TIME SPENT: 3hrs
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
# --> add your Python code here
from pymongo import MongoClient
from collections import defaultdict
import re

def connectDataBase():

    # Create a database connection object using pymongo
    # --> add your Python code here
    client = MongoClient('localhost', 27017)
    db = client["mydatabase"]
    return db
    
def createDocument(col, docId, docText, docTitle, docDate, docCat):

    # create a dictionary (document) to count how many times each term appears in the document.
    # Use space " " as the delimiter character for terms and remember to lowercase them.
    termCounts = {}
    terms = docText.lower().split() #split defaults the delimiter to " " in python
    
    [termCounts.update({term: termCounts[term] + 1}) if term in termCounts else termCounts.update({term: 1}) for term in terms]

    # create a list of dictionaries (documents) with each entry including a term, its occurrences, and its num_chars. Ex: [{term, count, num_char}]
    termList = []
    for term, count in termCounts.items():
        termList.append({"term": term, "count": count, "num_char": len(term)})
        
    #Producing a final document as a dictionary including all the required fields

    document = {
        "id": docId,
        "text": docText,
        "title": docTitle,
        "date": docDate,
        "category": docCat,
        "terms": termList
    }

    # Insert the document
    try:
        col.insert_one(document)
        print(f"Document with ID {docId} was created.")
    except Exception as e:
        print(f"An error occurred: {e}")

def deleteDocument(col, docId):

    # Delete the document from the database
    # --> add your Python code here
    result = col.delete_one({"id": docId})
    if result.deleted_count > 0:
        print(f"Document with ID {docId} was deleted.")
    else:
        print(f"No document found with ID {docId}.")

def updateDocument(col, docId, docText, docTitle, docDate, docCat):

    # Delete the document
    # --> add your Python code here
    deleteDocument(col, docId)
    # Create the document with the same id
    createDocument(col, docId, docText, docTitle, docDate, docCat)

    print(f"Document with ID {docId} was updated.")

def getIndex(col):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3', ...}
    # We are simulating an inverted index here in memory.
    # --> add your Python code here
    inverted_index = {}

    # Fetch all documents from the collection
    all_docs = col.find()

    # Iterate over each document
    for doc in all_docs:
        title = doc['title']  # Get the title of the document
        for term_dict in doc['terms']:
            term = term_dict['term']
            count = term_dict['count']
            if term not in inverted_index:
                inverted_index[term] = f"{title}:{count}"
            else:
                inverted_index[term] += f",{title}:{count}"

    # Return the inverted index
    return inverted_index

    # Example usage (Assuming you have a MongoDB instance running locally):

if __name__ == "__main__":
    db = connectDataBase()
    col = db["documents"]  # Name of the collection

    # Create a sample document
    createDocument(col, 1, "Python MongoDB integration is simple and powerful", "Integration with MongoDB", "2024-10-18", "Tech")

    # Get the inverted index
    index = getIndex(col)
    print("Inverted Index:", index)

    # Update the document
    updateDocument(col, 1, "Updated Python MongoDB integration details", "Updated MongoDB Integration", "2024-10-19", "Tech")

    # Delete the document
    deleteDocument(col, 1)