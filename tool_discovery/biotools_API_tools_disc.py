import sys
import json
import requests
import argparse
import yaml
import biotools_parse as bp
import pandas as pd
from pathlib import Path
from matplotlib import pyplot as plt


# The call to get all bio.tools entries through the api is: https://bio.tools/api/tool/?format=json.
# Unfortunately, the response is limited to n tools. To get the whole set, the next pages must be retrieve.
# use "next" in the response to get succesive entries.
 
base_call = "https://bio.tools/api/tool/?format=json"

def make_request(URL):
    try:
        response = requests.get(URL)
    except:
        print('Could not make the request')
        return
    else:
        response = json.loads(response.text)
        return(response)

def build_url(next_page, filters):
    call_template = "https://bio.tools/api/tool/?{attributes}{next_page}&format=json"
    if next_page:
        next_page = "&%s"%next_page
    else:
        next_page = ""
    attributes = '&'.join(filters)    
    url = call_template.format(next_page=next_page, attributes=attributes)
    return(url)


def get_all_pages(filters):
    res = []
    next_page = "page=1"
    print('Starting making the requests...')
    while next_page:
        response = make_request(build_url(next_page, filters))
        print("Requesting: " + build_url(next_page, filters), end='\r')
        res = res + response["list"]
        next_page = response["next"]
        if next_page:
            next_page = next_page[1:]
    print('\nRequests finished.')
    return(res)

def save_result(out_path, result):
    with open(out_path, 'w') as out:
        json.dump(result, out)
    print('Result saved as ' + out_path )
    

colnames_general = ['name', 'description', 'type', 'topic', 'input', 'output']
colnames_detailed = [ 'name', 'description', 'version', 'type', 'topic', 'links', 'publication', 'download', 'inst_instr', 'test', 'src', 'os', 'input', 'output', 'dependencies', 'documentation', 'license', 'termsUse', 'contribPolicy', 'authors', 'repository']
def results_to_table(result, colnames):
    tools = bp.biotoolsToolsGenerator(result).instances
    # Load features into table
    colnames_features = colnames
    df_dict = {name : [] for name in colnames_features}

    for tool in tools:
        for field in colnames_features:
            df_dict[field].append(tool.__dict__.get(field))

    df_features = pd.DataFrame.from_dict(df_dict)
    df_features.drop_duplicates(subset ="name", keep = False, inplace = True) 
    return(df_features)


def parse_zooma_results(input_file):
    with open(input_file, 'r') as inp:
        zooma_terms_df = pd.read_csv(input_file)
        # getting list of terms
        terms = zooma_terms_df['iri']
        terms = []
        free_terms = []
        terms_label = {}
        for index, row in zooma_terms_df.iterrows():
            if type(row['iri']) == str:
                term = row['iri'].split('http://edamontology.org/')[1].strip('\n')
                terms.append(term)
                terms_label[term] = row['label'].strip('\n')
            else:
                free_terms.append(row['keyword'].strip('\n'))
                
    return(terms, terms_label, free_terms)

def build_filter(term):
    filters_template =  {'topic': 'topicID="%s"', 'format':'dataFormatID="%s"', 'operation':'operationID="%s"', 'data':'dataTypeID="%s"'}
    if 'topic' in term:
        filters = filters_template['topic']%(term)
    elif 'data' in term:
        filters = filters_template['data']%(term)
    elif 'operation' in term:
        filters = filters_template['operation']%(term)
    elif 'format' in term:
        filters = filters_template['format']%(term)
    return(filters)     

def query_for_terms(terms, EDAM=False):
    '''
    Takes a list of EDAM terms or free text keywords and does a query for each
    EDAM=True for edam terms, EDAM=False for freetext keywords. Default: EDAM=False.
    Return a dictionary of results of the form: {<term>: <dataframe of results>}
    '''
    free_filter_template = 'description="%s"'
    results = dict()
    results_detailed = dict()
    # Iteratre through terms
    for term in terms:
        term  = term.replace("/",'-')
        # Avoid duplicated queries
        if term not in results.keys():
            # Building the filters using the EDAM terms
            if EDAM == True:
                filter_ = [build_filter(term)]
            else:
                filter_ = [free_filter_template%(term)]
            # Do the query
            result = get_all_pages(filter_)
            # Put result in table
            result_df = results_to_table(result, colnames_general)
            result_detailed_df = results_to_table(result, colnames_detailed)
            # Put results table in dictionary with the results for the other terms
            results[term] = result_df
            results_detailed[term] = result_detailed_df
    return(results, results_detailed)

def count_tools_per_term(results):
    count_tools_per_term = {term :len(results[term]) for term in results.keys()}
    return(count_tools_per_term)

def tools_per_term(results):
    tools_per_term = {term:results[term]['name'] for term in results}  
    return(tools_per_term)

def merge_tools_lists(results):
    tools = set()
    for table in results:
        tools_per_term_ = tools_per_term(table)
        for term in tools_per_term_:
            for tool in tools_per_term_[term]:
                tools.add(tool)
    return(tools)

def save_results(results_general, terms_label, path):
    template_output = path + '/tools_%s.tsv'
    for term in results_general.keys():
        file_name = template_output%(terms_label[term])
        results_general[term].to_csv(file_name, index = False, sep='\t')

def save_lists_tools(tools_per_term,path, EDAM=False):
    if EDAM==True:
        template_output = path + '/tools_edam_%s.txt'
    else:
        template_output = path + '/tools_free_%s.txt'
    for term in tools_per_term.keys():
        with open(template_output%(term), 'w') as f:
            for item in tools_per_term[term]:
                f.write("%s\n" % item)

### Disc pipeline
terms_file='keywords/ETL_EDAM_curated.csv'
ETL_edam_terms, terms_label_ETL, free_terms = parse_zooma_results(terms_file)
print(ETL_edam_terms)
print(terms_label_ETL)
print(free_terms)
ETL_edam_results_general, ETL_edam_results_detailed  = query_for_terms(ETL_edam_terms, True)
path_output_ETL = "outputs/ETL"
Path(path_output_ETL).mkdir(parents=True, exist_ok=True)
save_results(ETL_edam_results_general, terms_label_ETL, path_output_ETL)
ETL_free_results_general, ETL_free_results_detailed  = query_for_terms(free_terms, False)
count_tools_per_term(ETL_edam_results_general)
count_tools_per_term(ETL_free_results_general)

tools_per_term_ETL = tools_per_term(ETL_edam_results_general)
tools_per_term_ETL = {terms_label_ETL[term]:tools_per_term_ETL[term] for term in tools_per_term_ETL.keys()}

tools_per_term_free_ETL = tools_per_term(ETL_free_results_general)
tools_per_term_free_ETL = {term:tools_per_term_free_ETL[term] for term in tools_per_term_free_ETL.keys()}
save_lists_tools(tools_per_term_ETL, path_output_ETL, True)
save_lists_tools(tools_per_term_free_ETL, path_output_ETL, False)


class biotools_search():
    
    def __init__(self, 
                 search_name = 'default_search_name',
                 output_path = None,
                 keywords_free_path = None,
                 keywords_edam_path = None):

        self.name = search_name
        self.output_path = output_path
        self.keywords_free_path = keywords_free_path
        self.keywords_edam_path = keywords_edam_path
    


    def get_results(self):
        # prep

        # get terms

        # get results
        self.results_free =  self.query_for_terms(False)

    def query_prep(self):
        # check which paths are defined and inform

        # check paths exist

        # return
    
    def make_request(URL):
    try:
        response = requests.get(URL)
    except:
        print('Could not make the request')
        return
    else:
        response = json.loads(response.text)
        return(response)

    def build_url(next_page, filters):
        call_template = "https://bio.tools/api/tool/?{attributes}{next_page}&format=json"
        if next_page:
            next_page = "&%s"%next_page
        else:
            next_page = ""
        attributes = '&'.join(filters)    
        url = call_template.format(next_page=next_page, attributes=attributes)
        return(url)


    def get_all_pages(filters):
        res = []
        next_page = "page=1"
        print('Starting making the requests...')
        while next_page:
            response = make_request(build_url(next_page, filters))
            print("Requesting: " + build_url(next_page, filters), end='\r')
            res = res + response["list"]
            next_page = response["next"]
            if next_page:
                next_page = next_page[1:]
        print('\nRequests finished.')
        return(res)

    def save_result(out_path, result):
        with open(out_path, 'w') as out:
            json.dump(result, out)
        print('Result saved as ' + out_path )
        

    colnames_general = ['name', 'description', 'type', 'topic', 'input', 'output']
    colnames_detailed = [ 'name', 'description', 'version', 'type', 'topic', 'links', 'publication', 'download', 'inst_instr', 'test', 'src', 'os', 'input', 'output', 'dependencies', 'documentation', 'license', 'termsUse', 'contribPolicy', 'authors', 'repository']
    def results_to_table(result, colnames):
        tools = bp.biotoolsToolsGenerator(result).instances
        # Load features into table
        colnames_features = colnames
        df_dict = {name : [] for name in colnames_features}

        for tool in tools:
            for field in colnames_features:
                df_dict[field].append(tool.__dict__.get(field))

        df_features = pd.DataFrame.from_dict(df_dict)
        df_features.drop_duplicates(subset ="name", keep = False, inplace = True) 
        return(df_features)


    def parse_zooma_results(input_file):
        with open(input_file, 'r') as inp:
            zooma_terms_df = pd.read_csv(input_file)
            # getting list of terms
            terms = zooma_terms_df['iri']
            terms = []
            free_terms = []
            terms_label = {}
            for index, row in zooma_terms_df.iterrows():
                if type(row['iri']) == str:
                    term = row['iri'].split('http://edamontology.org/')[1].strip('\n')
                    terms.append(term)
                    terms_label[term] = row['label'].strip('\n')
                else:
                    free_terms.append(row['keyword'].strip('\n'))
                    
        return(terms, terms_label, free_terms)

    def build_filter(term):
        filters_template =  {'topic': 'topicID="%s"', 'format':'dataFormatID="%s"', 'operation':'operationID="%s"', 'data':'dataTypeID="%s"'}
        if 'topic' in term:
            filters = filters_template['topic']%(term)
        elif 'data' in term:
            filters = filters_template['data']%(term)
        elif 'operation' in term:
            filters = filters_template['operation']%(term)
        elif 'format' in term:
            filters = filters_template['format']%(term)
        return(filters)     

    def query_for_terms(terms, EDAM=False):
        '''
        Takes a list of EDAM terms or free text keywords and does a query for each
        EDAM=True for edam terms, EDAM=False for freetext keywords. Default: EDAM=False.
        Return a dictionary of results of the form: {<term>: <dataframe of results>}
        '''
        free_filter_template = 'description="%s"'
        results = dict()
        results_detailed = dict()
        # Iteratre through terms
        for term in terms:
            term  = term.replace("/",'-')
            # Avoid duplicated queries
            if term not in results.keys():
                # Building the filters using the EDAM terms
                if EDAM == True:
                    filter_ = [build_filter(term)]
                else:
                    filter_ = [free_filter_template%(term)]
                # Do the query
                result = get_all_pages(filter_)
                # Put result in table
                result_df = results_to_table(result, colnames_general)
                result_detailed_df = results_to_table(result, colnames_detailed)
                # Put results table in dictionary with the results for the other terms
                results[term] = result_df
                results_detailed[term] = result_detailed_df
        return(results, results_detailed)

def count_tools_per_term(results):
    count_tools_per_term = {term :len(results[term]) for term in results.keys()}
    return(count_tools_per_term)

def tools_per_term(results):
    tools_per_term = {term:results[term]['name'] for term in results}  
    return(tools_per_term)

def merge_tools_lists(results):
    tools = set()
    for table in results:
        tools_per_term_ = tools_per_term(table)
        for term in tools_per_term_:
            for tool in tools_per_term_[term]:
                tools.add(tool)
    return(tools)

def save_results(results_general, terms_label, path):
    template_output = path + '/tools_%s.tsv'
    for term in results_general.keys():
        file_name = template_output%(terms_label[term])
        results_general[term].to_csv(file_name, index = False, sep='\t')

def save_lists_tools(tools_per_term,path, EDAM=False):
    if EDAM==True:
        template_output = path + '/tools_edam_%s.txt'
    else:
        template_output = path + '/tools_free_%s.txt'
    for term in tools_per_term.keys():
        with open(template_output%(term), 'w') as f:
            for item in tools_per_term[term]:
                f.write("%s\n" % item)
