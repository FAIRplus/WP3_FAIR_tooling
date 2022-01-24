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
        print('Query done')
        if self.results.empty:
            print('No tools found')
            self.result_found = False
        else:
            self.rank_tools()
            print('Tools ranked')
            self.result_found = True
            

    def query_zooma(self):
        '''
        keywords is a set of strings to look up in zooma
        '''
        if self.verbosity:
            print("Looking up terms in ZOOMA")
        for keyword in list(self.keywords_weights['keyword']):
            if self.verbosity:
                print(f"{bcolors.BOLD}{keyword}{bcolors.ENDC}")
            confident_matches = za.zooma_single_lookup(keyword)
            if confident_matches:
                if self.verbosity:
                    print(f"Matches found in EDAM:")
                    [print(f"{match['label']} - {match['confidence']} - {match['edam_term']}") for match in confident_matches]
                
                w = self.keywords_weights.loc[self.keywords_weights['keyword']==keyword]['weight'].values[0]
                for match in confident_matches:
                    term = match['edam_term'].strip('\n')
                    self.edam_terms.append(term)
                    #self.terms_label[match] = str(match['label']).strip('\n')
                    self.keywords_weights = self.keywords_weights.append({'keyword':term, 'weight':w}, ignore_index=True)
                self.free_terms.append(keyword)
            else:
                self.free_terms.append(keyword)
        print(self.keywords_weights)
        print('Zooma lookup done')


    def query_terms(self):
        print('edam terms: ' + str(self.edam_terms))
        print('free terms' + str(self.free_terms))
        query = db_retrieval.query(self.edam_terms, self.free_terms)
        query.getData() # perform db search
        self.results = query.results

    def rank_tools(self):
        if self.verbosity:
            promp_text = 'Ranking results...'
            print(f'{bcolors.OKBLUE}{promp_text}{bcolors.ENDC}')

        # sorting
        self.results['raw_score'] = self.results.apply (lambda row: self.compute_score(row), axis=1)
        max_score = max(self.results['raw_score'])
        self.results['score'] = self.results.apply (lambda row: row['raw_score']/max_score, axis=1)
        self.results = self.results.sort_values('score', ascending=False)    
        print(self.results)
        print('Done')   

    def compute_score(self, row):
        if self.custom_weights == False:
            return(float(len([x for x in row['matches']])))
        else:
            scores = []
            for match in list(row['matches']):
                print(match)
                w = self.keywords_weights.loc[self.keywords_weights['keyword']==match]['weight'].values[0]
                scores.append(w)
            summ = sum(scores)
            return(float(summ))


    def generate_outputs(self):
        try:
            result = self.results.head(100).to_json(orient="records")
            self.json_result_parsed = json.loads(result)
            return(self.json_result_parsed)

        except Exception as err:
            raise(err)

        

