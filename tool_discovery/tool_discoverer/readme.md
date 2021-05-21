## Introduction 
This is a Python program makes a search in [bio.tools](https://bio.tools) given a table of keywords (free text terms) and matching [EDAM](https://edamontology.org/page) terms (`terms_file`). It returns a list of tools ranked by the number of keywords and [EDAM](https://edamontology.org/page) terms in their metadata. This number is normalized to calculate the 'score' associated to each tool in the results table. 
Moreover, keywords can be assigned a weight relative to its importance to modulate their impact in the tools ranking. To do so, the corresponding file containing keyword-weight association (`ranked_terms_file`) must be provided. 
It is assumed that the `terms_file` is a result of running [ZOOMA](https://www.ebi.ac.uk/spot/zooma/) on a list of free text terms.

## Requirements
```
[packages]
requests = "*"
pandas = "*"
tabulate = "*"

[requires]
python_version = "3.6"
```
This program has been tested using Python 3.6.9 and the following packages:
```
certifi==2020.12.5
chardet==4.0.0
idna==2.10
numpy==1.19.5
pandas==1.1.5
python-dateutil==2.8.1
pytz==2021.1
requests==2.25.1
six==1.16.0
tabulate==0.8.9
urllib3==1.26.4
```

## Usage

```bash
python3 tool_discoverer.py <configuration_file> [-v] [-h]
```
* `configuration_file`: path of configuration file.
* `-v, --verbose`: print detail information about the program progress to prompt.
* `-h, --help`: show help message.

### Configuration file
The configuration file is a plain text .ini file were five parameters are specified. It has the following form:
```ini
[required]
terms_file = keywords/ontology_annotation_EDAM_curated.csv
[optional]
ranked_terms_file = keywords/ontology_annotation_EDAM_ranked.csv
default_unspecified_keyword_score = 0.75
output_directory = results
name = example
```
**Required parameters**
* `terms_file`: path of file that contains keywords and matching EDAM terms and IRIs.
**Optional parameters**
* `ranked_terms_file`: path of file that contains the scores assigned to each keyword. If empty, all keywords will be assigned a weight = 1.
* `default_unspecified_keyword_weight`: the weight automatically assigned to keywords that are not included in the 'ranked_terms_file'. If empty, 0.7 will be assigned.
* `output_directory`: directory where results are stored. If empty, results will be saved in the working directory.
* `name`: name associated to the execution and is used to name the result files.

### `terms_file` file format
CSV file of three columns: `keyword`, `label` and `iri`. Each row corresponds to a keyword.
* `keyword`: term to be included in the search.
* `label`: EDAM label.
* `iri`: EDAM IRI.

### `ranked_terms_file` file format
CSV file of two columns: `keyword`, `weight`. Each row correspond to a keyword.
* `kyeword`: term to be included in the search.
* `weight`: weight assigned the keyword. In order for the maximum score to be 1, weights must be in the interval [0,1].