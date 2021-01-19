# This scripts reads keywords, finds corresponding EDAM ontology terms, and query bio.tools
# Input: a list of manual curated keywords
# Output: A list of tools for each topic

import requests
import pandas as pd

# Read keywords
def read_keywords(filename):
    with open (filename,'r') as f:
        keys = f.read().splitlines()
    return keys


# Query ZOOMA
def query_zooma(keyword):
    zooma_ep = "https://www.ebi.ac.uk/spot/zooma/v2/api/services/annotate?propertyValue="
    # use no manual curation. and select only terms from EDAM
    zooma_conf = "&filter=required:[none],ontologies:[edam]"
    query = zooma_ep + keyword + zooma_conf

    r = requests.get(query)
    if r.ok:
        # TODO revise
        results = r.json()
        all_matches = []
    # save all matched EDAM terms
    # for each match save iri, label,
        for i in results:
            extracted = [keyword, i["semanticTags"][0], i["annotatedProperty"]["propertyValue"], i["confidence"]]
            all_matches.append(extracted)
        return all_matches


# TODO: extract term definition and parent terms
# TODO: use one branch only

def query_ols_def(iri):
    # find the term definition in ols. using iri
    ols_ep = "http://www.ebi.ac.uk/ols/api/terms?iri="
    ols_query = ols_ep + iri
    try:
        response = requests.get(ols_query)
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error:",e)
        return 1


if __name__ == '__main__':
    topic = "ontology_annotation"
    keywords_raw = read_keywords("keywords/keywords_ontology_annotation_raw.txt")
    all_matches = []
    for i in keywords_raw:
        keywords_edam = query_zooma(i)
        all_matches.extend(keywords_edam)
    all_edam = pd.DataFrame(all_matches)
    all_edam.columns = ["keyword","iri","label","confidence"]
    all_edam.to_csv(topic+"_EDAM_all.csv", index = False)


