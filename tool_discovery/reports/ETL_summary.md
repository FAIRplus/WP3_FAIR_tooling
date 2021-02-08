# ETL tools

## Definition
Data Extraction, transformation, and loading (ETL) is the process of collecting data from one source to a desinated system in which the data is represented differently.[1]
(Define the FAIRplus ETL based on [the spreadsheet](https://docs.google.com/spreadsheets/d/1loEoROKxxh2gYEtXSiA0ziJjkTGJ2MYw3Xgzt1Z9JeI/edit#gid=0) focus on identifying tools for data content extraction and harmonisation. Extracting data from different sources and transforming it into a cohesive dataset.Scalable and portable ETL systems/processes to support data exchange with different validation and transform rules in both local and cloud servers
Build a scalable ETL system/process to surpport data exchange with different validation and transform rules. 

## FAIRplus use case and process
Our use case is ([Karsten's use case](https://github.com/FAIRplus/WP3_FAIR_tooling/issues/30)) We have identified a data set (maybe internally or externally) that we would like to import into our larger repository. 

Our ETL process is(Sukhi's diagram):

## Tools

#### Query and retrieval
- [TAMR]()
A commercial tool for information extraction
- [Bert]()
For information extraction

|name|description|link|
|--|--|--|
|bridgedbr|Use BridgeDb functions and load identifier mapping databases in R.|
|identifiers.org|Resolver of URIs.|
|...|...|


Complete list here.
https://github.com/FAIRplus/WP3_FAIR_tooling/blob/main/tool_discovery/outputs/ETL/tools_Data%20identity%20and%20mapping.tsv#L1

#### Annotation and curation
- [SDTM]()
A commercial software for data parsing
- [Dublin Core]()
Metadata management

#### Aggreation
- [TriFacta]()
A commercial tool for data quality managment


#### Deposition
- [Informatica]()
information extraction, cloud migration
- [REDCap]()
- [TransMART]()
data storage, clinical data
- [Collibra]()
data catalog, schema validation, governance, entity versioning

## Example use case 
For ETL for OHDSI 
| Data validation            | Python scripts or SQL scripts |                                                                                                                                                                                                                                                                                              |   |   |
|----------------------------|-------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---|---|
| Data harmonisation         | OMOP model                    |                                                                                                                                                                                                                                                                                              |   |   |
| Field mapping              | Rabbit in a Hat               | Tool does not do any transformation, only for documentation. OMOP models loaded into program. It is also possible to upload own model to use in the tool.Visual mapping tool (drag and drop). Uses output from White Rabbit. Output of the tool is a Word document (no code) of the mapping. |   |   |
| Formatting                 | Python scripts or SQL scripts |                                                                                                                                                                                                                                                                                              |   |   |
| Conversion                 | Python scripts or SQL scripts |                                                                                                                                                                                                                                                                                              |   |   |
| Mapping data to ontologies | Usagi                         | Link to actual tool.       |




# References: 
1. https://en.wikipedia.org/wiki/Extract,_transform,_load

