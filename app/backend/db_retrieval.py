import configparser
from pymongo import MongoClient
import pandas as pd

config = configparser.ConfigParser()
config.read('config.ini')
DBHOST = config['MONGO_DETAILS']['DBHOST']
DBPORT = config['MONGO_DETAILS']['DBPORT']
DATABASE = config['MONGO_DETAILS']['DATABASE']
COLLECTION = config['MONGO_DETAILS']['DISCOV_COLLECTION']

edam_df = pd.read_csv('EDAM_1.25.csv')
edam_dict = dict(zip(edam_df['Class ID'], edam_df['Preferred Label']))

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
                                              'edam_topics',
                                              'edam_operations',
                                              'matches',
                                              'citations',
                                              'sources_labels'])
        self.results.set_index('@id')

    def extract_citations(self, tool):
        #print('Extracting citations ...')
        citations = []
        if tool['publication']:
            for pub in tool['publication']:
                new_trace = {'x':[], 'y':[]}
                if type(pub) == dict:
                    if 'entries' in pub.keys():
                        for entry in pub['entries']:
                            if 'citations' in entry.keys():
                                [(new_trace['x'].append(item['year']), new_trace['y'].append(item['count'])) for item in entry['citations']]
                                entry['trace'] = new_trace
                                citations.append(entry)
        return(citations)
    
    def aggregate_sources_labels(self,tool):
        #print('Aggregating sources labels ...')
        labels = set()
        print(tool['source'])
        if 'biotools' in tool['source']:
            labels.add('biotools')
        if 'bioconductor' in tool['source']:
            labels.add('bioconductor')
        if 'github' in tool['source']:
            labels.add('github')
        if 'galaxy' in tool['source'] or 'toolshed' in tool['source']:
            labels.add('galaxy')
        if 'bioconda' in tool['source']:
            labels.add('bioconda')
        if 'bioconda_conda' in tool['source'] or 'bioconda_recipes' in tool['source']:
            labels.add('bioconda')
        if 'sourceforge' in tool['source']:
            labels.add('sourceforge')
        if 'bitbucket' in tool['source']:
            labels.add('bitbucket')
       
        labels_links = {}
        valid = {'github':['github'],
                'biotools':['bio.tools'],
                'bitbucket':['bitbucket'],
                'sourceforge':['sourceforge'],
                'galaxy':['galaxy','toolshed'],
                'bioconda':['bioconda'],
                'bioconductor':['bioconductor']}
        print(valid)
        if tool['links']:
            hit = False
            for label in labels:
                labels_links[label] = ''
                for link in tool['links']:
                    for valid_label in valid[label]:
                        if valid_label in link:
                            labels_links[label] = link
                            hit =True
                            break
            if hit == False:
                labels_links['other'] = tool['links'][0]

        if 'biotools' in labels:
            link = f"https://bio.tools/{tool['name']}"
            labels_links['biotools'] = link
            
            return(labels_links)

    def match_edam_label(self, uri):
        #print('Matching EDAM label')
        if uri == 'http://edamontology.org/topic_3557':
            uri = 'http://edamontology.org/operation_3557'
        try:
            label = edam_dict[uri]
        except:
            label = uri
        return(label)

    def match_data(self, doc, td):
        #print('Data types matching ...')
        newd = []
        if td in doc.keys():
            for data in doc[td]:
                if type(data)==dict:
                    newdict = {'datatype':'', 'formats':[]}
                    if 'datatype' in data.keys():
                        newdict['datatype'] = self.match_edam_label(data['datatype'])
                    if 'formats' in data.keys():
                        for i in data['formats']:
                            newdict['formats'].append(self.match_edam_label(str(i)))
                    newd.append(newdict)
        return(newd)


    def add_to_results(self, matches, topic):
        #print(f'Adding to results ...')
        for doc in matches:
            #print(f"- {doc['name']}")
            doc['_id'] = str(doc['_id'])
            doc['citations'] = self.extract_citations(doc)
            doc['sources_labels'] = self.aggregate_sources_labels(doc)
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
        #print('EDAM query ...')
        for term in self.edam_terms:
            matches = self.collection.find({
                'edam' : term
            })
            self.add_to_results(matches, term)

    def full_text_query(self, term):
        #print('Full text query ...')
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

'''
edam_terms = ['http://edamontology.org/topic_0797']
free_terms = ['ontology annotation', 'semantic annotation']
mquery = query(edam_terms, free_terms)
mquery.getData()
print(mquery.results)
'''