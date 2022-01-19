import configparser
from pymongo import MongoClient
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


config = configparser.ConfigParser()
config.read('config.ini')
DBHOST = config['MONGO_DETAILS']['DBHOST']
DBPORT = config['MONGO_DETAILS']['DBPORT']
DATABASE = config['MONGO_DETAILS']['DATABASE']
COLLECTION = config['MONGO_DETAILS']['COLLECTION']
DISCOV_COLLECTION = config['MONGO_DETAILS']['DISCOV_COLLECTION']


connection = MongoClient(DBHOST, int(DBPORT))
collection = connection[DATABASE][COLLECTION]
tools_discov_collection = connection[DATABASE][DISCOV_COLLECTION]

def clean_text(text):
    # split into words
    tokens = word_tokenize(text)
    # convert to lower case
    tokens = [w.lower() for w in tokens]
    # remove punctuation from each word
    import string
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    # filter out stop words
    stop_words = set(stopwords.words('english'))
    n2grams = [f"{ngram[0]} {ngram[1]}" for ngram in nltk.ngrams(words,2)]
    n3grams = [f"{ngram[0]} {ngram[1]} {ngram[2]}" for ngram in nltk.ngrams(words,3)]
    words = [w for w in words if not w in stop_words]
    return(words, n2grams, n3grams)

def searchable_data_prep():
    for tool in collection.find():
        discoverer_tool = tool
        discoverer_tool['description_words'] = []
        discoverer_tool['description_n2gram'] = []
        discoverer_tool['description_n3gram'] = []
        if tool['description']:
            for description in tool['description']:
                words, n2grams, n3grams = clean_text(description)
                words = list(set(words))
                n2grams = list(set(n2grams))
                n3grams = list(set(n3grams))
                for w in words:                                                             
                    discoverer_tool['description_words'].append(w)
                for ng in n2grams:
                    discoverer_tool['description_n2gram'].append(ng)
                for n3g in n3grams:
                    discoverer_tool['description_n3gram'].append(n3g)
        
        
        if tool['semantics']: #only entries from bio.tools have this field
            discoverer_tool['edam'] = []
            if tool['semantics']['topics']:
                discoverer_tool['edam'] = tool['semantics']['topics']

            if tool['semantics']['operations']:
                discoverer_tool['edam'] = tool['semantics']['operations'] 


        tools_discov_collection.insert(discoverer_tool)

def index():
    tools_discov_collection.create_index('description_words')
    tools_discov_collection.create_index('description_n2gram')
    tools_discov_collection.create_index('description_n3gram')
    tools_discov_collection.create_index('edam')


if __name__ == "__main__":
    # Preapare
    searchable_data_prep()
    # Then build inverted indexes in Mongo
    index()