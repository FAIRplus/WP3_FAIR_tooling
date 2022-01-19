import json
import requests
import os
import pandas as pd

import db_retrieval
import zooma_api as za

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class tools_discoverer(object):

    def __init__(self, label, kw_w, out_path, default_unspecified_keyword_score, custom_weights, verbosity):
        self.verbosity = verbosity
        self.label = label
        self.custom_weights = custom_weights

        if self.verbosity:
            prompt_text = f"Loading input files..."
            print(f"{bcolors.OKBLUE}{prompt_text}{bcolors.ENDC}")    

        self.terms_input = kw_w # list(dict('keyword', 'weight'))
        # keywords in:
        self.keywords_weights = pd.DataFrame(kw_w)
        # zooma terms in:
        self.edam_terms = []
        # terms stored here
        self.free_terms = []
        self.terms_label = {}

        self.query_zooma()

        self.default_score = default_unspecified_keyword_score
        if self.default_score == None:
            self.default_score = 0.7
        else:
            self.default_score = 1.0

        self.out_path = out_path

        

        # results will be here
        self.results = []

    def run_pipeline(self):
        self.query_terms()
        print('query done')
        self.rank_tools()
        print('tools ranked')

    def query_zooma(self):
        '''
        keywords is a set of strings to look up in zooma
        '''
        if self.verbosity:
            print("Looking up terms in ZOOMA")
        print(self.keywords_weights)
        for keyword in list(self.keywords_weights['keyword']):
            if self.verbosity:
                print(f"{bcolors.BOLD}{keyword}{bcolors.ENDC}")
            confident_matches = za.zooma_single_lookup(keyword)
            if confident_matches:
                if self.verbosity:
                    print(f"\tMatches found in EDAM:")
                    [print(f"\\tt{match['label']} - {match['confidence']} - {match['edam_term']}") for match in confident_matches]
                
                for match in confident_matches:
                        term = match['edam_term'].split('http://edamontology.org/')[1].strip('\n')
                        self.edam_terms.append(term)
                        self.terms_label[term] = str(match['label']).strip('\n')

            else:
                self.free_terms.append(keyword)
        print('zooma done')


    def query_terms(self):
        search_performed = False
        query = db_retrieval.query(self.edam_terms, self.free_terms)
        query.getData() # perform db search
        self.results = query.results
        print(self.results)

    def rank_tools(self):
        if self.verbosity:
            promp_text = 'Ranking results...'
            print(f'{bcolors.OKBLUE}{promp_text}{bcolors.ENDC}')

        # sorting
        print('sorting')
        self.results['raw_score'] = self.results.apply (lambda row: self.compute_score(row), axis=1)
        max_score = max(self.results['raw_score'])
        self.results['score'] = self.results.apply (lambda row: row['raw_score']/max_score, axis=1)
        self.results = self.results.sort_values('score', ascending=False)    
        print(self.results)
        print('Done')   

    def compute_score(self, row):
        if self.custom_weights == False:
            print(float(len([x for x in list(row['matches'])])))
            return(float(len([x for x in row['matches']])))
        else:
            scores = []
            for match in list(row['matches']):
                w = self.keywords_weights.loc[self.keywords_weights['keyword']=='Ontology annotation']['weight'].values[0]
                scores.append(w)
            summ = sum(scores)
            print(summ)
            return(float(summ))


    def generate_outputs(self):
        try:
            self.results.pop('_id')
            result = self.results.to_json(orient="records")
            print('hey')
            self.json_result_parsed = json.loads(result)
            return(self.json_result_parsed)

        except Exception as err:
            '''
            error_text = f"Something went wrong while saving results to {path}"
            print(f'{bcolors.FAIL}{error_text}{bcolors.ENDC}')
            '''
            raise(err)

        

