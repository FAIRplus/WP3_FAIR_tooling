
# coding: utf-8

# # bio.tools querying

# ## Overview

# ## Code

# In[1]:


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


def get_citations(tool):
    total_citations = 0
    for publication in tool.publication:
        if publication:
            if publication['metadata'] and 'date' in publication['metadata'].keys():
                total_citations += publication['metadata']['citationCount']
                    
    return(total_citations)


def get_topics(tool):
    clean_topics = set()
    if tool.topic:
        for topic in tool.topic:
            clean_topics.add(topic['term'])
    return(list(clean_topics))



colnames_general = ['name', 'description', 'type', 'topic', 'input', 'output']
colnames_detailed = [ 'name', 'description', 'version', 'type', 'topic', 'links', 'publication', 'download', 'inst_instr', 'test', 'src', 'os', 'input', 'output', 'dependencies', 'documentation', 'license', 'termsUse', 'contribPolicy', 'authors', 'repository', 'citations']
def results_to_table(result, colnames):
    tools = bp.biotoolsToolsGenerator(result).instances
    # Load features into table
    colnames_features = colnames
    df_dict = {name : [] for name in colnames_features}

    for tool in tools:
        for field in colnames_features:
            if field == 'citations':
                df_dict['citations'].append(get_citations(tool))
            elif field == 'topic':
                df_dict['topic'].append(get_topics(tool))
            else:
                df_dict[field].append(tool.__dict__.get(field))
        
    df_features = pd.DataFrame.from_dict(df_dict)
    df_features.drop_duplicates(subset ="name", keep = False, inplace = True) 
    return(df_features)


def parse_zooma_results(input_file):
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
    
def read_ranking(filename):
    ranked_keywords = pd.read_csv(filename)
    
    ranked_keywords['weight'] = ranked_keywords["weight"].apply(lambda x: float(x.strip('%'))*0.01)
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    ranked_keywords = ranked_keywords.applymap(trim_strings)
    return ranked_keywords

def get_description(tool_name):
    url_temp ='https://bio.tools/api/tool/?name="{name}"&format=json'
    ep = 'https://bio.tools/api/tool/?name="'
    query = url_temp.format(name=tool_name)
    try:
        response = requests.get(query)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    finally:
        response = json.loads(response.text)
        descriptions = [l['description'] for l in response['list']]
    
    return(descriptions)



def rank_tools(tool_list,ranked_keywords,tools_per_term, tools_per_term_free, joint_results, max_matches):
    w_matches_tools = []
    keywords = ranked_keywords['keyword'].tolist()
    print(keywords)
    for tool in list(tool_list):
        w_matches = 0
        matches = 0
        for k,l in tools_per_term_free.items():
            if tool in list(l):
                if k not in keywords:
                    print('%s not in keywords list. Assigning score of 0.7'%k)
                    w_matches += 0.7
                    matches += 1
                else:
                    w_matches += ranked_keywords.loc[ranked_keywords['keyword'] == k, 'weight'].item()
                    matches += 1
                    
        for k,l in tools_per_term.items():
            if tool in list(l):
                if k not in keywords:
                    print('%s not in keywords list. Assigning score of 0.7'%k)
                    w_matches += 0.7
                    matches += 1
                else:
                    w_matches += ranked_keywords.loc[ranked_keywords['keyword'] == k, 'weight'].item()
                    matches += 1

        tool_description = joint_results.loc[joint_results['name'] == tool, 'description'].iloc[0]
        links = joint_results.loc[joint_results['name'] == tool, 'links'].tolist()[0]
        topic = joint_results.loc[joint_results['name'] == tool, 'topic'].tolist()[0]
        type_ = joint_results.loc[joint_results['name'] == tool, 'type'].tolist()[0]
        citations = joint_results.loc[joint_results['name'] == tool, 'citations'].tolist()[0]
        
        if links:
            tool_url = links[0].get('url')
        else:
            tool_url = None
            
        biotools_url = 'https://bio.tools/%s'%tool
        
        kw_score = w_matches/max_matches

        row = [tool, "{:.3f}".format(kw_score), tool_description, topic, type_, citations, tool_url, biotools_url]
        w_matches_tools.append(row)

    df_results=pd.DataFrame(w_matches_tools, columns = ['Tool', 'keywords_score', 'Description', 'Topics', 'Type', 'Citations', 'URL', 'bio.tools URL'])
    df_results['keyword_rank'] = df_results['keywords_score'].rank(method='max')
    df_results['citations_rank'] = df_results['Citations'].rank(method='max')
    df_results['Score'] = df_results['keyword_rank']*0.6 + df_results['citations_rank']*0.4

    score_ranked=df_results.sort_values('keyword_rank', ascending=False)
    
    return(score_ranked)
    
def join_results(results_1, results_2):
    frames = []
    for term in results_1:
        frames.append(results_1[term])
    for term in results_2:
        frames.append(results_2[term])
    joint_results = pd.concat(frames)
    joint_results = joint_results.drop_duplicates(subset=['name'])
    return(joint_results)

def count_matches_edam_free(tools_per_term, tools_per_free_term, all_tools):
    matches_tools = {}
    for tool in list(all_tools):
        matches = 0
        for l in tools_per_free_term.values():
            if tool in list(l):
                matches += 1
        for l in tools_per_term.values():
            if tool in list(l):
                matches += 1
        matches_tools[tool] = matches
    return(matches_tools)

'''
plt.hist(ETL_annot_count_df['ETL annotations count'],alpha=0.5)
plt.xlim([2, 7])
plt.ylim([0, 50])
plt.title('ETL related terms each tool ')
plt.xlabel('Number of ETL terms')
plt.ylabel('Number of discovered tools')
plt.show()
'''