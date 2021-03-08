import json
import pandas as pd
import yaml
import sys


global webTypes
webTypes = ['Web API', 'Web application', 'Web service', 'Suite', 'Workbench', 'Database portal']


def prepFAIRcomp(instances):
    global stdFormats
    stdFormats= getFormats(instances)


def getFormats(instances):
    inputs = [a.input for a in instances]
    inputs_ = [a for a in inputs]
    inputsNames = []

    nonSFormats = ['txt', 'text', 'csv', 'tsv', 'tabular', 'xml', 'json', 'nucleotide', 'pdf', 'interval' ]
    for List in inputs_:
        for eachD in List:
            if 'format' in eachD.keys():
                if ' format' not in eachD['format']['term'] and eachD['format']['term'].lstrip() not in nonSFormats:
                    if '(text)' not in eachD['format']['term']:
                        if eachD['format']['term'].lstrip() not in inputsNames:
                            inputsNames.append(eachD['format']['term'].lstrip())
    return(inputsNames)

class instance(object):

    def __init__(self, name):

        # TODO: restrict the format of properties

        # TODO: include @id
        self.name = name
        self.description = None # string
        self.version = None
        self.super_type = None
        self.type = None
        self.links =[]
        self.publication =  0 # number of related publications [by now, for simplicity]
        self.download = []  # list of lists: [[type, url], [], ...]
        self.inst_instr = False # boolean // FUTURE: uri or text
        self.test = False # boolean // FUTURE: uri or text
        self.src = [] # string
        self.os = [] # list of strings
        self.input = [] # list of dictionaries biotools-like {'format' : <format> , 'uri' : <uri> , 'data' : <data> , 'uri': <uri>}
        self.output = [] # list of dictionaries biotools-like {'format' : <format> , 'uri' : <uri> }
        self.dependencies = [] # list of strings
        self.documentation = [] # list of lists [[type, url], [type, rul], ...]
        self.license = False # string
        self.termsUse = False #
        self.contribPolicy = False
        self.authors = [] # list of strings
        self.repository = []
        self.source = [] #string
        self.bioschemas = False
        self.https = False
        self.operational = False
        self.ssl = False
        self.topic = False
    
    def compF1_2(self):
        '''
        Identifiability of version:
        Whether there is a scheme to uniquely and properly identify the software version.
        A version of the form X.X is considered acceptable: True. Anything else is False
        '''
        if self.version != None:
            vers_veredicts = []
            for v in self.version:
                if len(v.split('.'))==2:
                    vers_veredicts.append(True)
                else:
                    vers_veredicts.append(False)
            # for now, a single True is enough, can be changed in the future, not allowing any False
            if True in vers_veredicts:
                return(True)
        return(False)

    global struct_meta
    # TODO this list must depend on the analyzed sources. Take from config.yaml
    struct_meta = ['biotools', 'bioconda', 'bioconductor', 'galaxyShed', 'galaxyConfig']
    def compF2_1(self):
        '''
        Structured Metadata
        Metadata is adjusted to specific metdata formats
        The sources in struct_meta are structured. If these sources are among self.source: True. Otherwise: False
        '''
        if True in [a in struct_meta for a in self.source]:
            return(True)
        else:
            return(False)

    global softReg
    softReg = ['biotools', 'bioconda', 'bioconductor']
    def compF3_1(self):
        '''
        Searchability in registries
        Whether software is included in the main software registries.
        If the source is among the software registries: True. Otherwise: Falsecource
        '''
        if True in [a in softReg for a in self.source]:
            return(True)
        else:
            return(False)

    def compF3_2(self):
        '''
        Searchabiliy in software repositories
        Whether software can be found in any of the major software repositories e.g. GitHub, GitLab, SourceForge, 
        If the instance has an associated repository uri: True. Otherwise: False
        '''
        if len(self.repository)>0:
            return(True)
        else:
            return(False)

    def compF3_3(self):
        '''
        Searchability in literature.
        Whether software can be found in specialized literatue services e.g. EuropePMC, PubMed, Journals Site, bioArxiv.
        If the instance at least one associated publication: True. Otherwise: False
        '''
        if self.publication>0:
            return(True)
        else:
            return(False)

    ##============== Accessibility metrics computation functions ================

    def compA1_1(self):
        '''
        WEB
        Existence of API or web 
        Whether it is possible to access a working version of the tool through and API or web. 
        A 200 status when accessing the links provided is consired acceptable.
        '''
        if self.super_type == 'web':
            import urllib.request
            status = []
            for l in self.links:
                url = l['url']
                if len(url)>0:
                    if 'http:' in url:
                        try:
                            re = urllib.request.urlopen(url)
                        except:
                            continue
                        else:
                            status.append(re.status)
                    elif 'ftp:' in url:
                        try:
                            a, b=urllib.request.urlretrieve(url, r'%s'%(url.split('/')[-1]))
                        except:
                            continue
                        else:
                            status.append(200)
            if 200 in status:
                return(True)
            else:
                return(False)
        else:
            return(False)

    def compA1_2(self):
        '''
        NO WEB
        Existence of downloadable and buildable software working version
        If there is a download link: True ## we do not check if it is available. 
        '''
        if self.super_type == 'no_web':
            if len(self.download)>0:
                return(True)
            else:
                return(False)
        else:
            return(False)

    def compA1_3(self):
        '''
        NO WEB
        Existence of installation instructions
        Whether there is a set of instructions and other necessary information the user can follow to build the software
        We check self.inst_instructions (already a boolean)
        '''
        if self.super_type == 'no_web':
            return(self.inst_instr)
        else:
            return(False)

    def compA1_4(self):
        '''
        Existence of test data
        Whether test data is available
        We check self.test (already a boolean)
        '''
        return(self.test)

    def compA1_5(self):
        '''
        NO WEB
        Existence of software source code
        Whether software source code is available 
        '''
        if self.super_type == 'no_web':
            if len(self.src)>0:
                return(True)
            else:
                return(False)
        else:
            return(False)


    def compA3_2(self):
        '''
        NO WEB
        Availability of version for free OS
        Whether the software can be used in a free operative system
        '''
        if self.super_type == 'no_web':
            if 'Linux' in self.os:
                return(True)
            else:
                return(False)
        else:
            return(False)

    def compA3_3(self):
        '''
        No WEB
        Availability for several OS
        Whether there are versions of the software for several operative systems
        '''
        if self.super_type == 'no_web':
            if len(self.os)>1:
                return(True)
            else:
                return(False)
        else:
            return(False)

    def compA3_4(self):
        '''
        NO WEB
        Availability on free e-Infrastructures
        Whether the software can be used in a free e-infrastructure
        We are only considering galaxy servers and vre
        '''
        if self.super_type == 'no_web':
            eInfra = ['vre.multiscalegenomics.eu', 'galaxy.', 'usegalaxy.']
            for url in self.links:
                for e in eInfra:
                    if e in url['url']:
                        return(True)
                else:
                    return(False)
            return(False)
        else:
            return(False)


    def compA3_5(self):
        '''
        NO WEB
        Availability on several e-Infrastructures
        Whether the software can be used in several e-infrastructure
        '''
        if self.super_type == 'no_web':
            count = 0
            eInfra = ['vre.multiscalegenomics.eu', 'galaxy.', 'usegalaxy.']
            for url in self.links:
                for e in eInfra:
                    if e in url['url']:
                        count += 1
            if count>1:
                return(True)

            return(False)
        else:
            return(False)
    
    ##============== Interoperability metrics computation functions ================
    def compI1_1(self):
        '''
        Usage of standard data formats
        Whether the input and output datatypes are formally specified and related to accepted ontologies
        '''
        for i in self.input:
            if 'format' in i.keys():
                if i['format']['term'] in stdFormats:
                    return(True)

        for i in self.output:
            if 'format' in i.keys():
                if i['format']['term'] in stdFormats:
                    return(True)

        return(False)

    def compI1_3(self):
        '''
        Verificability of data formats
        Whether input/output data are specified using verifiable schemas (e.g. XDS, Json schema, ...)
        '''
        if self.compI1_1() == True:
            return(True)

        verifiable_formats = ['json', 'xml', 'rdf', 'xds']
        formats = self.input + self.output
        terms = set()
        for i in formats:
            if 'format' in i.keys():
                terms.add(i['format']['term'])
        
        for term in terms:
            if term in verifiable_formats:
                return(True)

        return(False)


    def compI1_4(self):
        '''
        Flexibility of data format supported
        Whether the software allows to choose among various input/output data formats, or provide the necessary tools to convert other common formats into the supported ones.
        '''
        ins = []
        formats = self.input + self.output
        for i in formats:
            if 'format' in i.keys():
                ins.append(i['format']['term'])

        if len(ins)>1:
            return(True)
        else:
            return(False)

    #def compI1_5(self):
    def compI2_1(self):
        '''
        Existence of API/library version 
        Whether the software has API /library versions to be included in users' pipelines
        '''
        interTypes = ['Library', 'Web API']
        for t in self.type:
            if t in interTypes:
                return(True)
        else:
            return(False)

    def compI3_1(self):
        '''
        Dependencies statement
        Whether the software includes details about dependencies
        '''
        if len(self.dependencies)>0:
            return(True)
        else:
            return(False)

    def compI3_2(self):
        '''
        Dependencies are provided
        Whether the software includes its dependencies or mechanisms to access them
        '''
        # checking source
        if 'galaxyShed' in self.source:
            return(True)
        elif 'bioconda' in self.source:
            return(True)
        elif 'bioconductor' in self.source:
            return(True)
        
        #checking links
        sources_with_dependencies = ['bioconda', 'bioconductor', 'galaxy.']
        for url in self.links:
            if True in  [a in url for a in sources_with_dependencies]:
                return(True)
        
        return(False)
    
    # ===================== Reusability ==============================================================

    def compR1_1(self):
        '''
        Existence of usage guides
        Whether software user guides are provided
        '''
        noGuide = ['NEWS', 'LICENSE', 'Terms of use']
        for doc in self.documentation:
            if doc[0][0] not in noGuide: # doc[0] is the type of document
                return(True)

        return(False)


    def compR2_1(self):
        '''
        WEB
        Existence of terms of use
        Whether Terms of Use are stated
        '''
        if self.super_type == 'web':
            for doc in self.documentation:
                if doc[0][0] == 'Terms of use':
                    return(True)
            if self.license:
                if len(self.license)>0:
                    return(False)
                else:
                    return(False)
            else:
                return(False)
        else:
            return(False)

    def compR2_2(self):
        '''
        NO WEB
        Existence of conditions of use
        Whther conditions of installation and usage are stated
        '''
        for doc in self.documentation:
            if doc[0][0].lower() == 'conditions of use':
                return(True)
            if doc[0][0].lower() == 'terms of use':
                return(True)

        return(False)

    def compR3_2(self):
        '''
        Existence of credit
        Whether credit for contributions is provided
        '''
        if len(self.authors)>0:
            return(True)
        else:
            return(False)

    def compR4_1(self):
        '''
        Usage of version control
        Whether the software follows a version-control system
        '''
        for repo in self.repository:
            if 'github' in repo or 'mercurial-scm' in repo:
                return(True)
        return(False)
    
    def FAIRscores(self):
        self.F = 0
        self.F += self.metrics.F1_2*0.4
        self.F += self.metrics.F2_1*0.2

        acc = [self.metrics.F3_1, self.metrics.F3_2, self.metrics.F3_3].count(True)
        if acc == 1:
            self.F += 0.7*0.4
        elif acc == 2:
            self.F += 0.85*0.4
        elif acc == 3:
            self.F += 1*0.4

        self.A = 0
        if self.super_type == 'web':
            self.A += (self.metrics.A1_1*0.6 + self.metrics.A1_4*0.4)*0.7
            self.A += self.metrics.A1_3*0.3
        else:
            self.A += (self.metrics.A1_2*0.5 + self.metrics.A1_3*0.2 + self.metrics.A1_4*0.1 + self.metrics.A1_5*0.2)*0.7
            self.A += (self.metrics.A3_2+self.metrics.A3_3+self.metrics.A3_4+self.metrics.A3_5)*(0.25)*0.3

        self.I = 0
        self.I += (self.metrics.I1_1*0.5+self.metrics.I1_3*0.3+self.metrics.I1_4*0.2)*0.6
        self.I += self.metrics.I2_1*0.1
        self.I += (self.metrics.I3_1+self.metrics.I3_2)*(1/2)*(0.3)

        self.R = 0
        self.R += self.metrics.R1_1*0.3
        if self.metrics.R2_1:
            self.R += 0.3
        elif self.metrics.R2_2:
            self.R += 0.3
        self.R += self.metrics.R3_2*0.2
        self.R += self.metrics.R4_1*0.2



    def generateFAIRMetrics(self):
        # FINDABILITY
        self.metrics = FAIRmetrics()

        #self.metrics.F1_1 = True # all have a name
        self.metrics.F1_2 = self.compF1_2() #
        self.metrics.F2_1 = self.compF2_1()
        #self.metrics.F2_2 = True # by now, not accepted metadata standard known
        self.metrics.F3_1 = self.compF3_1() # in this script, all biotools
        self.metrics.F3_2 = self.compF3_2()
        self.metrics.F3_3 = self.compF3_3()
        # ACCESIBILITY
        self.metrics.A1_1 = self.compA1_1()
        self.metrics.A1_2 = self.compA1_2()
        self.metrics.A1_3 = self.compA1_3()
        self.metrics.A1_4 = self.compA1_4()
        self.metrics.A1_5 = self.compA1_5()

        #self.metrics.A2_1 = False
        #self.metrics.A2_2 = False

        #self.metrics.A3_1 = self.compA3_1()
        self.metrics.A3_2 = self.compA3_2()
        self.metrics.A3_3 = self.compA3_3()
        self.metrics.A3_4 = self.compA3_4()
        self.metrics.A3_5 = self.compA3_5()

        self.metrics.I1_1 = self.compI1_1()  # TO DO
        #self.metrics.I1_2 = False # NOT FOR NOW
        self.metrics.I1_3 = self.compI1_3()
        self.metrics.I1_4 = self.compI1_4()
        #self.metrics.I1_5 = False # NOT FOR NOW

        self.metrics.I2_1 = self.compI2_1()
        #self.metrics.I2_2 = self.compI2_2()

        self.metrics.I3_1 = self.compI3_1()
        self.metrics.I3_2 = self.compI3_2()
        #self.metrics.I3_3 = self.compI3_2() # Same as befor, BY NOW

        self.metrics.R1_1 = self.compR1_1()
        #self.metrics.R1_2 = False #NOT FOR NOW

        self.metrics.R2_1 = self.compR2_1()
        self.metrics.R2_2 = self.compR2_2()

        #self.metrics.R3_1 = False # Not for now

        self.metrics.R3_2 = self.compR3_2()

        self.metrics.R4_1 = self.compR4_1()
        #self.metrics.R4_2 = False # By now
        #self.metrics.R4_3 = False # By now


class FAIRmetrics(object):

    def __init__(self):
        #self.F1_1 = None # uniqueness of name
        self.F1_2 = None # idenfibiability of version

        self.F2_1 = None # structured metadata
        #self.F2_2 = None # standarized metadata

        self.F3_1 = None # searchability in registries
        self.F3_2 = None # searchability in software repositories
        self.F3_3 = None # searchability in literature

        self.A1_1 = None # Existance of API or web 
        self.A1_2 = None # Existance of downloadable and buildable software working version
        self.A1_3 = None # Existance of installation instructions
        self.A1_4 = None # Existance of test data
        self.A1_5 = None # Existance of software source code

        #self.A2_1 = None # Metadata of previous versions at software repositories
        #self.A2_2 = None # Existence of accesible previous versions of the software

        #self.A3_1 = None # Registration compulsory
        self.A3_2 = None # Availability of version for free OS
        self.A3_3 = None # Availability for several OS
        self.A3_4 = None # Availability on free e-Infrastructures
        self.A3_5 = None # Availability on several e-Infrastructures

        self.I1_1 = None # Usage of standard data formats
        #self.I1_2 = None # Usage of standard API framework
        self.I1_3 = None # Verificability of data formats
        self.I1_4 = None # Flexibility of data format supported
        #self.I1_5 = None # Generation of provenance information

        self.I2_1 = None # Existance of API/library version 
        #self.I2_2 = None # E-infrastructure compatibility

        self.I3_1 = None #Dependencies statement
        self.I3_2 = None #Dependencies are provided
        #self.I3_3 = None # Whether the software is distributed via a dependencies aware system

        self.R1_1 = None # Existence of usage guides
        #self.R1_2 = None # Existence of usage examples

        self.R2_1 = None # Existence of terms of use
        self.R2_2 = None # Existence of conditions of use

        #self.R3_1 = None # Contributors policy specification
        self.R3_2 = None # Existence of credit

        self.R4_1 = None # Usage of version control
        #self.R4_2 = None # Existence of release policy
        #self.R4_3 = None # Metadata of previous versions at software repositories



class toolGenerator(object):
    def __init__(self, tools, source):
        self.tools = tools
        self.source = source
        self.instances = []


def cleanVersion(version):
    if version != None:
        if '.' in version:
            return(version.split('.')[0]+'.'+ version.split('.')[1])
        else:
            return(version)
    else:
        return(version)


def lowerInputs(listInputs):
    newList = []
    if len(listInputs)>0:
        for format in listInputs:
            newFormat = {}
            for a in format.keys():
                newInner = {}
                if format[a] != []:
                    if type(format[a]) == list:
                        for eachdict in format[a]:
                            for e in eachdict.keys():
                                newInner[e] = eachdict[e].lower()
                            newFormat[a] = newInner
                    else:
                        for e in format[a].keys():
                            newInner[e] = format[a][e].lower()
                        newFormat[a] = newInner
        newList.append(newFormat)
    else:
        return([])
    return(newList)

def parse_type(tool):
    types = tool.get("toolType")
    types_web  = []
    types_noweb = []
    if types:
        for t in types:
            if t in webTypes:
                types_web.append(t)
            else:
                types_noweb.append(t)
    return(types_web, types_noweb)




class biotoolsToolsGenerator(toolGenerator):

    def __init__(self, tools, source = 'biotools'):

        toolGenerator.__init__(self, tools, source)

        for tool in self.tools:
            
            if tool.get("toolType"):
                types_web, types_noweb = parse_type(tool)
                if types_web:
                    self.build_instance(tool, types_web, 'web')
                if types_noweb:
                    self.build_instance(tool, types_noweb, 'no_web')
            else:
                # if no type stated, we assume it is no-web since these are the most common
                self.build_instance(tool, None, 'no_web')


    def build_instance(self, tool, types, super_type):

            name = tool['name'].lower()

            newInst = instance(name)
            newInst.super_type = super_type
            newInst.type = tool.get("toolType")
            newInst.version = self.parse_versions(tool)
            newInst.description = tool.get('description')
            newInst.homepage = tool.get('homepage')
            newInst.publication = tool['publication']
            newInst.download = self.parse_download(tool)
            newInst.src = self.parse_src(tool)
            newInst.os = tool.get('operatingSystem')
            newInst.input = self.parse_input(tool)
            newInst.output = self.parse_output(tool)
            newInst.documentation = self.parse_documentation(tool)
            newInst.inst_instr = self.parse_install_instr(tool, newInst)
            newInst.license = tool.get('license')
            newInst.authors = self.parse_authors(tool)
            newInst.repository = self.parse_repositories(tool)
            newInst.topic = tool.get('topic')
            newInst.links = tool.get('link')

            newInst.source = ['biotools']

            self.instances.append(newInst)
    

    def parse_versions(self, tool):
        versions = []
        if type(tool.get("version")) == list:
            for v in tool.get("version"):
                versions.append(cleanVersion(v))
        return(versions)


    def parse_download(self, tool):
        links = [ [tol['type'], tol['url']] for tol in tool['download'] ]
        return(links)


    def parse_src(self, tool):
        src = []
        for down in [a for a in tool['download'] if a['type'] == 'Source package']:
            src.append(down['url'])
        for down in [a for a in tool['download'] if a['type'] == 'Source code']:
            src.append(down['url'])
        return(src)
    
    def parse_input(self, tool):
        inputs = []
        if len(tool['function'])>0:
            inputs = [f['input'] for f in tool['function']]
            return(lowerInputs(inputs[0]))
        else:
            return([])

    def parse_output(self, tool):
        outputs = []
        if len(tool['function'])>0:
            outputs = [f['input'] for f in tool['function']]
            return(lowerInputs(outputs[0]))
        else:
            return([])

    def parse_documentation(self, tool):
        doc = [ [tol['type'], tol['url']] for tol in tool['documentation'] ]
        return(doc)
    
    def parse_install_instr(self, tool, newInst):
        for d in newInst.documentation:
            if 'manual' in d[0][0].lower():
                return(True)
        else:
            return(False)
        
    def parse_authors(self, tool):
        newAuth = []
        for dic in tool['credit']:
            if dic['name'] not in newAuth and dic['name']!=None:
                newAuth.append(dic['name'])
        return(newAuth)
    
    def parse_repositories(self, tool):
        repos = []
        for link in tool['link']:
            if "Repository" in link['type']:
                repos.append(link['url'])
        return(repos)


def parse_biotools_metadata(in_file):
    # open json
    with open(in_file, "r") as infile:
        entries = json.load(infile)    
    
    # parse the set of entries => intances
    tools = biotoolsToolsGenerator(entries).instances 
    return(tools)


def get_config(args):
    config_file = args[1]
    with open(config_file, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            return(config)
        except yaml.YAMLError as exc:
            print(exc)


if __name__ == "__main__":

    config = get_config(sys.argv)
    infile = config['input_file']
    instances = parse_biotools_metadata(infile)
   
    prepFAIRcomp(instances)
    print("Preapared for FAIRsoft measurement")
    print("Calculating instances FAIRsoft metrics and scores ...")
    for inst in instances:
        inst.generateFAIRMetrics()
        inst.FAIRscores()
    
    # preparing data frame for handling and visualization

    # Features
    colnames_features = [ 'name', 'description', 'version', 'type', 'topic', 'links', 'publication', 'download', 'inst_instr', 'test', 'src', 'os', 'input', 'output', 'dependencies', 'documentation', 'license', 'termsUse', 'contribPolicy', 'authors', 'repository']
    df_dict = dict()
    for name in colnames_features:
        df_dict[name] = []
        
    for tool in instances:
        for field in colnames_features:
            df_dict[field].append(tool.__dict__.get(field))
       
    df_feaures = pd.DataFrame.from_dict(df_dict)

    df_feaures.to_csv(config['output_path']+'/'+config['output_name']+'.csv', index=False)

    