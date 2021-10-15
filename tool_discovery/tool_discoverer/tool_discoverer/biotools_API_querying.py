import json
import requests
import os
import pandas as pd

import biotools_parse as bp
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

    def __init__(self, label, terms_file, ranked, out_path, default_unspecified_keyword_score, verbosity):
        self.verbosity = verbosity
        self.label = label

        if self.verbosity:
            prompt_text = f"Loading input files..."
            print(f"{bcolors.OKBLUE}{prompt_text}{bcolors.ENDC}")    

        self.terms_file = terms_file
        self.parse_keywords()
        self.query_zooma()
        #self.parse_zooma_results()

        self.ranked_file = ranked
        if self.ranked_file:
            self.read_ranking()
            self.default_score = default_unspecified_keyword_score
            if self.default_score == None:
                self.default_score = 0.7
        else:
            self.default_score = 1.0

        self.out_path = out_path
        self.check_output_directory()


    def query_zooma(self):
        '''
        keywords is a set of strings to look up in zooma
        '''
        self.edam_terms = []
        self.free_terms = []
        self.terms_label = {}

        if self.verbosity:
            print("Looking up terms in ZOOMA")

        for keyword in self.keywords:
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

    def parse_keywords(self):
        try:
            keywords_df = pd.read_csv(self.terms_file)
        except Exception as err:
            error_text = f"ERROR: Something went wrong while opening and parsing keywords file '{self.terms_file}'."
            print(f"{bcolors.FAIL}{error_text}{bcolors.ENDC}")
            raise
        else:
            self.keywords = set()
            # Do zooma loockup
            for index, row in keywords_df.iterrows():
                self.keywords.add(row['keyword'])

                    
    def parse_zooma_results(self):
        try:
            zooma_terms_df = pd.read_csv(self.terms_file)
        except Exception as err:
            error_text = f"ERROR: Something went wrong while opening and parsing zooma results file '{self.terms_file}'."
            print(f"{bcolors.FAIL}{error_text}{bcolors.ENDC}")
            raise
        else:
            # getting list of terms
            self.edam_terms = []
            self.free_terms = []
            self.terms_label = {}
            for index, row in zooma_terms_df.iterrows():
                if type(row['iri']) == str:
                    term = row['iri'].split('http://edamontology.org/')[1].strip('\n')
                    self.edam_terms.append(term)
                    self.terms_label[term] = str(row['label']).strip('\n')
                else:
                    self.free_terms.append(str(row['keyword']).strip('\n'))
        
    def read_ranking(self):
        try:
            ranked_keywords = pd.read_csv(self.ranked_file)
        except Exception as err:
            error_text = f"ERROR: Something went wrong while parsing ranked terms file '{self.ranked_file}'."
            print(f"{bcolors.FAIL}{error_text}{bcolors.ENDC}")
            raise

        else:
            if True in list(ranked_keywords.duplicated(subset=['keyword'])):
                print(f"{bcolors.FAIL}ERROR: Duplicated keywords in {self.ranked_file}. Please, fix it and run again.{bcolors.ENDC}")
                exit()
            else:
                ranked_keywords['weight'] = ranked_keywords["weight"].apply(lambda x: float(x.strip('%'))*0.01)
                trim_strings = lambda x: x.strip() if isinstance(x, str) else x
                self.ranked_keywords = ranked_keywords.applymap(trim_strings)

    def check_output_directory(self):
        if len(self.out_path)==0:
            self.out_path = './'
        elif self.out_path == '.':
            self.out_path = './'

        if self.out_path[-1]!='/':
            self.out_path = self.out_path + '/'


    def build_filter(self, term):
        """
        Returns a bio.tools filter for a given EDAM term
        """
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


    def build_free_filter(self, term):
        """
        Returns a bio.tools filter for a given term. This filter is used to search free text
        """
        free_filter_template = 'description="%s"'
        return(free_filter_template%(term))
    

    def build_url(self, next_page, filters):
        """
        Returns a URL for querying bio.tools given the filters and the page to be queried
        """
        call_template = "https://bio.tools/api/tool/?{attributes}{next_page}&format=json"
        if next_page:
            next_page = "&%s"%next_page
        else:
            next_page = ""
        attributes = '&'.join(filters)    
        url = call_template.format(next_page=next_page, attributes=attributes)
        return(url)


    def make_request_biotools(self, next_page, filters):
        """
        Makes a request for given filter and an specified page
        """
        URL = self.build_url(next_page, filters)

        try:
            response = requests.get(URL)
        except Exception as err:
            error_text = f"ERROR: Something went wrong while making a request for URL: {URL}."
            print(f"{bcolors.FAIL}{error_text}{bcolors.ENDC}")
            raise(err)
        else:
            try:
                response = json.loads(response.text)
            except Exception as err:
                error_text = f"ERROR: Something went erong while parsing the JSON file after requesting {URL}."
                print(f"{bcolors.FAIL}{error_text}{bcolors.ENDC}")
                raise(err)
            else:
                return(response)

    def get_all_pages(self, filters):
        res = []
        next_page = "page=1"
        
        while next_page:
            response = self.make_request_biotools(next_page, filters)
            if self.verbosity:
                print(f"\t\tRequesting {self.build_url(next_page, filters)}", end='\r')
            res = res + response["list"]
            next_page = response["next"]
            if next_page:
                next_page = next_page[1:]
        if self.verbosity:
            print('\n\t\tRequests finished.')
        return(res)

    def get_citations(self, tool):
        total_citations = 0
        for publication in tool.publication:
            if publication:
                if publication['metadata'] and 'date' in publication['metadata'].keys():
                    total_citations += publication['metadata']['citationCount']
                        
        return(total_citations)

    def get_topics(self, tool):
        clean_topics = set()
        if tool.topic:
            for topic in tool.topic:
                clean_topics.add(topic['term'])
        return(list(clean_topics))

    def get_operations(self, tool):
        clean_ops = set()
        if tool.operation:
            for op in tool.operation:
                clean_ops.add(op['term'])
        return(list(clean_ops))
    
    def results_to_table(self, result, colnames):
        colnames_d = {
            'general' : ['name', 'biotoolsID', 'name_fancy', 'description', 'type', 'topic', 'input', 'output'],
            'detailed' : [ 'name', 'biotoolsID','name_fancy', 'description', 'version', 'type', 'topic', 'operation', 'links', 'publication', 'download', 'inst_instr', 'test', 'src', 'os', 'input', 'output', 'dependencies', 'documentation', 'license', 'termsUse', 'contribPolicy', 'authors', 'repository', 'citations']
        }
        tools = bp.biotoolsToolsGenerator(result).instances
        # Load features into table
        colnames_features = colnames_d[colnames]
        df_dict = {name : [] for name in colnames_features}

        for tool in tools:
            for field in colnames_features:
                if field == 'citations':
                    df_dict['citations'].append(self.get_citations(tool))
                elif field == 'topic':
                    df_dict['topic'].append(self.get_topics(tool))
                elif field == 'operation':
                    df_dict['operation'].append(self.get_operations(tool))

                else:
                    df_dict[field].append(tool.__dict__.get(field))
            
        df_features = pd.DataFrame.from_dict(df_dict)
        df_features.drop_duplicates(subset ="name", keep = False, inplace = True) 
        return(df_features)

    def query_for_terms(self, terms : list, EDAM=False):
        '''
        Takes a list of EDAM terms or free text keywords and does a query for each.
        EDAM=True for edam terms, EDAM=False for freetext keywords. Default: EDAM=False.
        Return a dictionary of results of the form: {<term>: <dataframe of results>}
        '''
    
        results = dict()
        results_detailed = dict()
        # Iteratre through terms
        for term in terms:
            term  = term.replace("/",'-')
            # Avoid duplicated queries
            if term not in results.keys():
                # Building the filters using the EDAM terms
                if EDAM == True:
                    filter_ = [self.build_filter(term)]
                else:
                    filter_ = [self.build_free_filter(term)]
                # Do the query
                if self.verbosity:
                    print(f'\tQuerying bio.tools for term "{term}"')

                result = self.get_all_pages(filter_)
                # Put result in table
                result_df = self.results_to_table(result, 'general')
                result_detailed_df = self.results_to_table(result, 'detailed')
                # Put results table in dictionary with the results for the other terms
                results[term] = result_df
                results_detailed[term] = result_detailed_df
        return(results, results_detailed)


    def query_biotools(self):
        search_performed = False
        # Querying EDAM terms
        if self.verbosity:
            if self.edam_terms:
                print(f"{bcolors.OKBLUE}Querying bio.tools for EDAM terms:{bcolors.ENDC}")
            else:
                text_warn = "No EDAM terms provided."
                print(f"{bcolors.WARNING}{text_warn}{bcolors.ENDC}")
        try:
            self.edam_results_general, self.edam_results_detailed  = self.query_for_terms(self.edam_terms, True)
        except Exception as err:
            error_text = 'ERROR: Something went wrong while querying bio.tools.'
            print(f'{bcolors.FAIL}{error_text}{bcolors.ENDC}')
            raise(err)
        else:
            search_performed = True
        
        # Querying free text terms
        if self.verbosity:
            if self.free_terms:
                print(f"{bcolors.OKBLUE}Querying bio.tools for free text terms:{bcolors.ENDC}")
            else:
                text_warn = "No free text keywords provided. Skipping free terms search."
                print(f"{bcolors.WARNING}{text_warn}{bcolors.ENDC}")

        try:
            self.free_results_general, self.free_results_detailed  = self.query_for_terms(self.free_terms, False)
        except Exception as err:
            error_text = 'Something went wrong while querying bio.tools.'
            print(f'{bcolors.FAIL}{error_text}{bcolors.ENDC}')
            raise(err)
        else:
            search_performed = True        
                    
        if search_performed == False:
            text_warn = "No search was performed, no keywords were provided. Exiting..."
            print(f"{bcolors.WARNING}{text_warn}{bcolors.ENDC}")


    def merge_tools_lists(self):
        self.all_tools = set()
        for tools_per_term in [self.tools_per_term, self.tools_per_term_free]:
            for term in tools_per_term:
                for tool in tools_per_term[term]:
                    self.all_tools.add(tool)
    

    def join_results(self):
        frames = []
        for term in self.edam_results_detailed:
            frames.append(self.edam_results_detailed[term])
        for term in self.free_results_detailed:
            frames.append(self.free_results_detailed[term])
        joint_results = pd.concat(frames)
        self.joint_results = joint_results.drop_duplicates(subset=['name'])
        

    def compute_tools_per_term(self, results, EDAM=False):
        tools_per_term = {term:results[term]['name'] for term in results}
        if EDAM:
            tools_per_term = {self.terms_label[term]:tools_per_term[term] for term in tools_per_term.keys()}
        return(tools_per_term)


    def process_results(self):
        if self.edam_results_general == {} and self.edam_results_detailed == {}:
            print(f"{bcolors.WARNING}No results found. Exiting...{bcolors.ENDC}")
            exit()
        # arrange by term
        self.tools_per_term = self.compute_tools_per_term(self.edam_results_general, True)
        self.tools_per_term_free = self.compute_tools_per_term(self.free_results_general, False)

        # join results
        self.join_results()
        self.merge_tools_lists()

    
    def calculate_max_matches(self):
        matches_tools = {}
        for tool in list(self.all_tools):
            matches = 0
            for l in self.tools_per_term_free.values():
                if tool in list(l):
                    matches += 1
            for l in self.tools_per_term.values():
                if tool in list(l):
                    matches += 1
            matches_tools[tool] = matches
        matches = pd.DataFrame(list(matches_tools.items()), columns= ['tool','search_count']).sort_values('search_count', ascending=False)
        self.max_matches = max(matches['search_count'])


    def compute_score(self, tool):
        w_matches = 0
        matches = 0
        for k,l in self.tools_per_term_free.items():
            if tool in list(l):
                if k not in self.keywords:
                    w_matches += self.default_score
                    matches += 1
                    if k not in self.default_score_keywords and self.verbosity:
                        warning_text = f'WARNING: No score specified for "{k}" by user. Assigning score of {self.default_score}'
                        print(f"{bcolors.WARNING}{warning_text}{bcolors.ENDC}")
                    self.default_score_keywords.add(k)
                    

                else:
                    w_matches += self.ranked_keywords.loc[self.ranked_keywords['keyword'] == k, 'weight'].item()
                    matches += 1
        
        for k,l in self.tools_per_term.items():
            if tool in list(l):
                if k not in self.keywords:
                    w_matches += self.default_score
                    matches += 1
                    if k not in self.default_score_keywords and self.verbosity:
                        warning_text = f'WARNING: No score specified for "{k}" by user. Assigning score of {self.default_score}'
                        print(f"{bcolors.WARNING}{warning_text}{bcolors.ENDC}")
                    self.default_score_keywords.add(k)
                else:
                    w_matches += self.ranked_keywords.loc[self.ranked_keywords['keyword'] == k, 'weight'].item()
                    matches += 1
        
        kw_score = w_matches/self.max_matches
        return(kw_score)


    def build_tool_row(self, tool):
        kw_score = self.compute_score(tool)
        tool_description = self.joint_results.loc[self.joint_results['name'] == tool, 'description'].iloc[0]
        biotoolsID = self.joint_results.loc[self.joint_results['name'] == tool, 'biotoolsID'].iloc[0]
        links = self.joint_results.loc[self.joint_results['name'] == tool, 'links'].tolist()[0]
        topic = self.joint_results.loc[self.joint_results['name'] == tool, 'topic'].tolist()[0]
        operation = self.joint_results.loc[self.joint_results['name'] == tool, 'operation'].tolist()[0]
        type_ = self.joint_results.loc[self.joint_results['name'] == tool, 'type'].tolist()[0]
        citations = self.joint_results.loc[self.joint_results['name'] == tool, 'citations'].tolist()[0]
        name_fancy = self.joint_results.loc[self.joint_results['name'] == tool, 'name_fancy'].tolist()[0]
        inputs = self.joint_results.loc[self.joint_results['name'] == tool, 'input'].tolist()[0]
        outputs = self.joint_results.loc[self.joint_results['name'] == tool, 'output'].tolist()[0]
        license_ = self.joint_results.loc[self.joint_results['name'] == tool, 'license'].tolist()[0]
        if links:
                tool_url = links[0].get('url')
        else:
            tool_url = None
        

        row = [name_fancy, "{:.3f}".format(kw_score), tool_description, topic, operation, inputs, outputs, type_, citations, tool_url, biotoolsID, license_]

        return(row)


    def rank_tools(self):
        if self.verbosity:
            promp_text = 'Ranking results...'
            print(f'{bcolors.OKBLUE}{promp_text}{bcolors.ENDC}')

        w_matches_tools = []
        if self.ranked_file == '':
            self.keywords = []
            
        else:
            self.keywords = self.ranked_keywords['keyword'].tolist()

        self.default_score_keywords=set()
        self.calculate_max_matches()

        for tool in list(self.all_tools):
            row = self.build_tool_row(tool)
            w_matches_tools.append(row)

        df_results=pd.DataFrame(w_matches_tools, columns = ['Tool', 'keywords_score', 'Description', 'Topics', 'Operations', 'Inputs','Outputs','Type', 'Citations', 'URL', 'biotoolsID', 'License'])
        df_results['keyword_rank'] = df_results['keywords_score'].rank(method='max')
        df_results['citations_rank'] = df_results['Citations'].rank(method='max')
        df_results['comp_score'] = df_results['keyword_rank']*0.6 + df_results['citations_rank']*0.4

        self.df_ranked_tools = df_results.sort_values('keyword_rank', ascending=False)


    def run_pipeline(self):
        self.query_biotools()
        self.process_results()
        self.rank_tools()


    def check_outdir_exist(self):
        # creates output directory if it does not exist
        import os
        os.makedirs(self.out_path, exist_ok=True)

    def check_file_name(self, filename, ext):
        '''
        If the filename+extension already exists, it returns a new numbered filename 
        Used by functions saving resutls to prevent overwriting existing files
        '''
        i = 1
        if os.path.exists(f"{filename}.{ext}"):
            i = 1
            while os.path.exists(f"{filename}({i}).{ext}"):
                i += 1
            new_filename = f"{filename}({i}).{ext}"
        else:
            new_filename = f"{filename}.{ext}"
        return(new_filename)
        

    def save_csv(self):
        filename = f"{self.out_path}{self.label}_ranked_tools"
        path = self.check_file_name(filename, 'csv')

        if self.verbosity:
            p_text = f"Saving results in CSV format to {path}"
            print(f'{bcolors.OKBLUE}{p_text}{bcolors.ENDC}')

        try:
            self.df_ranked_tools.to_csv(path, index=False)
        except Exception as err:
            error_text = f"Something went wrong while saving results to {path}"
            print(f'{bcolors.FAIL}{error_text}{bcolors.ENDC}')
            raise(err)


    def prep_description(self, desc):
        desc = desc[0].upper() + desc[1:]
        desc=desc.replace('\n\n', '<br>')
        desc=desc.replace('\n', '<br>')
        desc=f"<div class='desc short click_expand'>{desc}</div>"
        return(desc)

    def prep_link(self, link):
        if link == None:
            link=''
        else:
            link=f'<div class="link short click_expand"><a href="{link}" target="_blank">{link}</a></div>'
        return(link)
    
    def prep_citations(self, cits):
        cits=int(cits)
        cits=(f"{cits:,g}")
        cits = f"<div class='citations short click_expand'>{cits}</div>"
        return(cits)

    def prep_lists(self, items, label):
        content=""
        for i in items:
            content=f"{content}<li>{i}</li>"
        content = f"<div class='{label} short click_expand'><ul>{content}</ul></div>"
        return(content)

    def prep_generic(self, score):
        content = f"<div class='short click_expand'>{score}</div>"
        return(content)

    def prep_name(self, row):
        label = row['biotoolsID']
        link=f'https://bio.tools/{label}'
        name = row['Tool']
        cont=f'<div class="name short click_expand"><a href="{link}" target="_blank">{name}</a></div>'
        return(cont)

    def prep_inputs(self, inputs, label):
        content = ""
        for item in inputs:
            if 'data' in item.keys():
                data = item['data'].get('term')
                if 'format' in item.keys():
                    format_ = item['format'].get('term')
                    if format_:
                        content = f"{content}<li>{data} : {format_}</li>"
                    else:
                        content = f"{content}<li>{data}</li>"
        content = f"<div class='{label} short click_expand'><ul>{content}</ul></div>"
        return(content)
            

    def prepare_html_table(self):

        self.html_df=self.df_ranked_tools[['Tool', 'keywords_score', 'Description', 'Topics', 'Operations', 'Inputs','Outputs','Type', 'Citations', 'URL', 'biotoolsID', 'License']].copy()
        self.html_df = self.html_df.rename(columns={'keywords_score':'Score'})
        self.html_df = self.html_df.rename(columns={'Operations':'Functionality'})
        self.html_df['Description'] = self.html_df['Description'].apply(self.prep_description)
        self.html_df['URL'] = self.html_df['URL'].apply(self.prep_link)
        self.html_df['Citations'] = self.html_df['Citations'].apply(self.prep_citations)
        self.html_df['Type'] = self.html_df['Type'].apply(self.prep_lists, label='type')
        self.html_df['Topics'] = self.html_df['Topics'].apply(self.prep_lists, label='topic')
        self.html_df['Functionality'] = self.html_df['Functionality'].apply(self.prep_lists, label='operation')
        self.html_df['Score'] = self.html_df['Score'].apply(self.prep_generic)
        self.html_df['Tool'] = self.html_df.apply(self.prep_name, axis=1)
        self.html_df['Inputs'] = self.html_df['Inputs'].apply(self.prep_inputs, label='formats')
        self.html_df['Outputs'] = self.html_df['Outputs'].apply(self.prep_inputs, label='formats')
        self.html_df['License'] = self.html_df['License'].apply(self.prep_generic)
        self.html_df = self.html_df.drop('biotoolsID', 1)

        self.html_df = self.html_df.sort_values('Score', ascending=False)

    def save_html(self):
        from html_temp import template

        self.prepare_html_table()
        html_table = self.html_df.to_html(border = 0, escape=False, table_id='my-table', col_space =50, index=False)
        html_results = template.format(name=self.label, keywords=', '.join(self.keywords), content=html_table)

        filename = f"{self.out_path}{self.label}_ranked_tools"
        path = self.check_file_name(filename, 'html')

        if self.verbosity:
            promp_text = f"Saving results in HTML format to {path}"
            print(f'{bcolors.OKBLUE}{promp_text}{bcolors.ENDC}')

        try:
            with open(path,'w') as out_file:
                out_file.write(html_results)
        except Exception as err:
            error_text = f"Something went wrong while saving results to {path}"
            print(f'{bcolors.FAIL}{error_text}{bcolors.ENDC}')
            raise(err)

    def prep_md_name(self, row):
        name = row['Tool']
        biotoolsID = row['biotoolsID']
        content = f"[{name}](https://bio.tools/{biotoolsID})"
        return(content)

    def prep_md_desc(self, desc):
        desc = desc.strip()
        desc = desc[0].upper() + desc[1:]
        if desc[-1] != '.':
            desc += '.'

        desc=desc.replace('\n\n', '<br>')
        desc=desc.replace('\n', '<br>')
        desc=desc.replace('|', '<br>')
        return(desc)
    
    def prep_md_lists(self, items):
        if items:
            new_items = f"{items[0]}"
            if len(items)>1:
                for item in items[1:]:
                    new_items += f", {item}"
            return(new_items)
        else:
            return("")

    def prep_md_lists_fancy(self, items):
        new_items = ""
        for item in items:
            new_items = f"<li>{item}</li>"
        new_items = f"<ul>{new_items}</ul>"
        return(new_items)


    def save_md(self):
        self.md_df = self.df_ranked_tools[['Tool', 'keywords_score', 'Description', 'Topics', 'Operations', 'Type', 'biotoolsID', 'License']].copy()
        self.md_df['Tool'] = self.md_df.apply(self.prep_md_name, axis=1)
        self.md_df['Description'] = self.md_df['Description'].apply(self.prep_md_desc)
        self.md_df['Type'] = self.md_df['Type'].apply(self.prep_md_lists_fancy)
        self.md_df['Topics'] = self.md_df['Topics'].apply(self.prep_md_lists_fancy)
        self.md_df = self.md_df.rename(columns={'Operations':'Functionality'})
        self.md_df['Functionality'] = self.md_df['Functionality'].apply(self.prep_md_lists_fancy)
        self.md_df["How To"] = ""
        self.md_df = self.md_df.sort_values('keywords_score', ascending=False)
        self.md_df = self.md_df.drop('biotoolsID', 1)
        self.md_df = self.md_df.drop('keywords_score', 1)
        self.md_df = self.md_df.iloc[:10]


        md_table = self.md_df.to_markdown(index=False)

        filename = f"{self.out_path}{self.label}_ranked_tools"
        path = self.check_file_name(filename, 'md')

        if self.verbosity:
            p_text = f"Saving results in MarkDown format to {path}"
            print(f'{bcolors.OKBLUE}{p_text}{bcolors.ENDC}')

        try:
            with open(path,'w') as out_file:
                out_file.write(md_table)
        except Exception as err:
            error_text = f"Something went wrong while saving results to {path}"
            print(f'{bcolors.FAIL}{error_text}{bcolors.ENDC}')
            raise(err)



    def save_outputs(self):
        self.check_outdir_exist()
        self.save_csv()
        self.save_html()
        self.save_md()
        

        

