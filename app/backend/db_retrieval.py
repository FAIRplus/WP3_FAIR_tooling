import configparser
from pymongo import MongoClient
import pandas as pd

config = configparser.ConfigParser()
config.read('config.ini')
DBHOST = config['MONGO_DETAILS']['DBHOST']
DBPORT = config['MONGO_DETAILS']['DBPORT']
DATABASE = config['MONGO_DETAILS']['DATABASE']
COLLECTION = config['MONGO_DETAILS']['DISCOV_COLLECTION']

class query(object):
    def __init__(self, edam_terms, free_terms):
        self.edam_terms = edam_terms
        self.free_terms = free_terms
        self.results = pd.DataFrame(columns =['_id', 
                                              '@id', 
                                              'authors',
                                              'bioschemas',
                                              'contribPolicy',
                                              'dependencies',
                                              'description',
                                              'documentation', 
                                              'download', 
                                              'https', 
                                              'input', 
                                              'inst_instr', 
                                              'license', 
                                              'links', 
                                              'name', 
                                              'operational', 
                                              'os', 
                                              'output',
                                              'publication', 
                                              'repository', 
                                              'semantics', 
                                              'source', 
                                              'src', 
                                              'ssl', 
                                              'termsUse', 
                                              'test', 
                                              'type', 
                                              'version',
                                              'matches'])
        self.results.set_index('@id')

    def add_to_results(self, matches, topic):
        for doc in matches:
            if '@id' in doc.keys():
                if doc['@id'] in self.results_ids:
                    self.results.loc[doc['@id'],'matches'].append(topic)
                    
                else:
                    doc['matches'] = [topic]
                    doc_id = doc['@id']
                    doc.pop('@id')
                    self.results.loc[doc_id] = doc
                    self.results_ids.add(doc_id)


    def query_edam(self):
        for term in self.edam_terms:
            matches = self.collection.find({
                'edam' : term
            })

            self.add_to_results(matches, term)

    def full_text_query(self, term):
        matches = []
        description_docs = self.collection.find({
            'description' : {'$gt' : [] }
        })
        for doc in description_docs:
            for description in doc['description']:
                if term in description.lower():
                    matches.append(doc)
                    break

        return(matches)

    def query_description(self):
        for term in self.free_terms:
            term = term.lower()
            l = len(term.split(' '))
            if l==1:
                matches = self.collection.find({'description_words':term})
            elif l==2:
                matches = self.collection.find({'description_n2gram':term})
            elif l==3:
                matches = self.collection.find({'description_n3gram':term})
            else:
                matches =  self.full_text_query(term)
            
            if matches:
                self.add_to_results(matches, term)
        
    
    def connect_mongo(self):
        connection = MongoClient(DBHOST, int(DBPORT))
        self.collection = connection[DATABASE][COLLECTION]

    def getData(self):
        self.connect_mongo()
        self.results_ids = set()
        self.query_edam()
        self.query_description()
