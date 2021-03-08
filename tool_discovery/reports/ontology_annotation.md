# Tools for ontology strategies

## Main objectives
This recipe identifies tools for different operation in ontology strategies, such as ontology annotation, ontology mapping, ontology management, etc. It aims to provide a start point for implementing ontology strategy related FAIRifications.

>The lists of tools in this document are generated either by manual curation, which reflects what is being used in the industry or discovered automatically from bio.tools repository.Instead of providing comprehensive lists covering all types of tools, we aim to provide some tools as examples to allow people to start the exploration.
>
>_Contents in this table are generated in March 2021, for updated contents, please check the [FAIR tooling repository]()._


## Overview

The figure below shows concepts around ontology strategies. Ontology annotation is an important section in this diagram.

```mermaid
graph LR
    subgraph Ontology strategies<br>

        A[Ontology recommendation]
        B[Ontology annotation]
        C[Ontology mapping]
        
        subgraph Ontology management
            A[Ontology engineering]
            A1[Ontology management]
        end
    end
```
The table below is an overview of ontology strategies tools identified. Details of each tools are also provided below.

<table>
  <tr>
   <td><strong>Ontology annotation</strong>
   </td>
   <td><strong>Ontology mapping</strong>
   </td>
   <td><strong>Ontology management</strong>
   </td>
   <td>
<strong>Ontology engineering</strong>
   </td>
  </tr>
  <tr>
   <td><a href="https://github.com/dmis-lab/biobert">BioBert</a>
   </td>
   <td><a href="https://www.ebi.ac.uk/spot/oxo/index">OxO</a>
   </td>
   <td><a href="http://www.aber-owl.net/">AberOWL</a>
   </td>
   <td><a href="https://github.com/enanomapper/slimmer">eNanoMapper Slimmer</a>
   </td>
  </tr>
  <tr>
   <td><a href="https://bioportal.bioontology.org/annotatorplus">NCBI BioPortal Annotator</a>
   </td>
   <td>
   </td>
   <td><a href="https://bioportal.bioontology.org/">BioPortal</a>
   </td>
   <td><a href="http://owlcs.github.io/owlapi/">OWLAPI</a>
   </td>
  </tr>
  <tr>
   <td><a href="https://github.com/ISA-tools/OntoMaton">OntoMaton</a>
   </td>
   <td>
   </td>
   <td><a href="https://www.scibite.com/platform/centree/">Centree Ontology Manager</a>
   </td>
   <td><a href="https://protege.stanford.edu/">Protégé</a>
   </td>
  </tr>
  <tr>
   <td><a href="https://www.ontotext.com/products/ontotext-platform/">OntoText</a>
   </td>
   <td>
   </td>
   <td><a href="https://www.ebi.ac.uk/ols/index">OLS</a>
   </td>
   <td><a href="http://robot.obolibrary.org/">ROBOT</a>
   </td>
  </tr>
  <tr>
   <td><a href="https://semantic-web.com/poolparty-semantic-suite/">PoolParty Semantic Suite</a>
   </td>
   <td>
   </td>
   <td><a href="http://www.ontobee.org/">Ontobee</a>
   </td>
   <td><a href="https://www.topquadrant.com/products/topbraid-composer/">TopBraid Composer</a>
   </td>
  </tr>
  <tr>
   <td><a href="https://prodi.gy/">Prodigy</a>
   </td>
   <td>
   </td>
   <td><a href="https://www.poolparty.biz/">PoolParty</a>
   </td>
   <td><a href="http://vocbench.uniroma2.it/">VocBench</a>
   </td>
  </tr>
  <tr>
   <td><a href="https://www.scibite.com/platform/termite/">Termite</a>
   </td>
   <td>
   </td>
   <td>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td><a href="https://www.ebi.ac.uk/spot/zooma/">ZOOMA</a>
   </td>
   <td>
   </td>
   <td>
   </td>
   <td>
   </td>
  </tr>
</table>

## Operations

### Ontology annotation
The process of linking free text or data items to’ tokens’ (defined terms from a lexicon) which provide semantic value. For example, free text "type 2 diabetes" can be be annotated with [terms](http://purl.obolibrary.org/obo/MONDO_0005148) in the MONDO disease ontology. 

__Manual identified tools__ (Tools that are manually collected)
|Tool|Description|License|Topics|Platform|
|---|--|--|--|--|
|[ZOOMA](https://www.ebi.ac.uk/spot/zooma/)|A tool for mapping free text annotations to ontology term based on a curated repository of annotation knowledge|[EMBL-EBI Terms of Use](https://www.ebi.ac.uk/about/terms-of-use/)|Ontology and terminology,<br>Systems biology,<br>Data identity and mapping|Web application,<br> API|
|[NCBI BioPortal Annotator](https://bioportal.bioontology.org/annotatorplus)|Get annotations for biomedical text with classes from the ontologies.|[NioPortal Terms of Use](https://www.ebi.ac.uk/about/terms-of-use/)|Ontology and terminology,<br>Systems biology,<br>Data identity and mapping|Web application,<br> API|
|[BioBert](https://github.com/dmis-lab/biobert)|A biomedical language representation model designed for biomedical text mining tasks such as biomedical named entity recognition, relation extraction, question answering.|[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)|text mining,<br> named-entity recognition,<br> natural language processing|Python|
|[Termite](https://www.scibite.com/platform/termite/)|Semantic enrichment to unlock the value of unstructured text and simplify the identification of new potential biomarker leads from scientific text.|Commercial tool|Ontology and terminology|
|[PoolParty Semantic Suite](https://semantic-web.com/poolparty-semantic-suite/)|Automate the handling of heterogeneous metadata systems and the creation of enterprise knowledge graphs.design knowledge graphs at your own pace and with speed. Create your own ontologies and custom schemes by reusing already existing ontologies such as FOAF, FIBO, schema.org and CHEBI, among others. Apply them to your existing taxonomies with ease.|Commercial tool|Content enrichment,<br>Data integration|
|[OntoMaton](https://github.com/ISA-tools/OntoMaton)| A tool facilitating ontology search and tagging functionalities within Google Spreadsheets.|[CPAL license](https://opensource.org/licenses/CPAL-1.0)||Google Add-ons|
|[Prodigy](https://prodi.gy/)|A modern annotation tool for creating training and evaluation data for machine learning models. You can also use Prodigy to help you inspect and clean your data, do error analysis and develop rule-based systems to use in combination with your statistical models.|Commercial tool|Data annotation|Python, Web application,API|
|[OntoText](https://www.ontotext.com/products/ontotext-platform/)|Connect and publish complex enterprise knowledge with standard-compliant semantic graph database;Customize and apply analytics to link documents to graphs, extract new facts, classify and recommend content...|Commercial tool|




Tools that are discovered from the Bio.Tools platform.

Other Tools discovered in the bio.tools registery: 

|Tool|Description|License|Topics| Platform |
|:--:|:----:|:--:|:--:|:------:|:--:|


### Ontology mapping
The process of determining correspondences between equivalent concepts in alternative ontologies, and other vocabularies. This may include mapping to convey different levels of granularity.

|Tool|Description|License|Topics|Platform|
|---|--|--|--|--|
|[OxO](https://www.ebi.ac.uk/spot/oxo/index)|a service for finding mappings (or cross-references) between terms from ontologies, vocabularies and coding standards. OxO imports mappings from a variety of sources including the Ontology Lookup Service and a subset of mappings provided by the UMLS. We're still developing the service so please get in touch if you have any feedback.|[EMBL-EBI Terms of Use](https://www.ebi.ac.uk/about/terms-of-use/)|GUI and API|

Tools that are discovered from the Bio.Tools platform.
|Tool|Description|License|Topics|Platform|
|---|--|--|--|--|--|


### Ontology management
The process of managing ontologies and other vocabularies in semantic web-linked data environments.This includes policies for update and maintenance of constituent and new terms.

|Tool|Description|License|Topics|Type|
|---|--|--|--|--|
|[OLS](https://www.ebi.ac.uk/ols/index)|a repository for biomedical ontologies that aims to provide a single point of access to the latest ontology versions.|[EMBL-EBI Terms of Use](https://www.ebi.ac.uk/about/terms-of-use/)||Web Application, API|
|[BioPortal](https://bioportal.bioontology.org/)|A repository of biomedical ontologies|[BioPortal Terms of Use](https://www.bioontology.org/terms/)||Web Application, API|
|[PoolParty](https://www.poolparty.biz/) |Knowledge Engineering & Knowledge Graph Management. Taxonomy, ontology and linked dataset management |Commercial tool|Ontology and terminology|
|[Centree Ontology Manager](https://www.scibite.com/platform/centree/)|a centralised, enterprise-ready resource for ontology management and transforms the experience of maintaining and releasing ontologies for research-led businesses.|Commercial tool||Web application, API|
|[Ontobee](http://www.ontobee.org/)|A linked data server designed for ontologies. Ontobee is aimed to facilitate ontology data sharing, visualization, query, integration, and analysis.|[Apache 2.0](http://www.apache.org/licenses/LICENSE-2.0.html)||Web application|
|[AberOWL](http://www.aber-owl.net/)|A framework for ontology-based access to biological data. It consists of a repository of bio-ontologies, a set of webservices which provide access to OWL(-EL) reasoning over the ontologies, and several frontends which utilise the ontology repository and reasoning services.|||Web application, API|


Tools that are discovered from the Bio.Tools platform.
|Tool|Description|License|Topics|Platform|
|---|--|--|--|--|--|

#### Ontology engineering

The process of developing and maintaining ontologies during the ontology life cycle.

|Tool|Description|License|Topics|Type|
|---|--|--|--|--|
|[Protégé](https://protege.stanford.edu/)|A free, open source ontology editor and a knowledge management system|[2-Clause BSD](https://opensource.org/licenses/BSD-2-Clause)||Web application, Desktop application|
|[ROBOT](http://robot.obolibrary.org/)|An open source library and command-line tool for automating ontology development tasks. ROBOT provides ontology processing commands for a variety of tasks, including commands for converting formats, running a reasoner, creating import modules, running reports, and various other tasks.|[BSD 3-Clause License](https://raw.githubusercontent.com/ontodev/robot/master/LICENSE.txt)||Command-line tool|
|[OWLAPI](http://owlcs.github.io/owlapi/)|A Java API and reference implmentation for creating, manipulating and serialising OWL Ontologies|LGPL and Apache||API|
|[eNanoMapper Slimmer](https://github.com/enanomapper/slimmer)|A slim tool to slim ontologies as part of ontology integration. It allows users to provide configuration files that specify which parts of an ontology should be kept and/or removed, allowing to just select parts of the ontology you like.|[MIT license](https://opensource.org/licenses/MIT)||Java|
|[TopBraid Composer](https://www.topquadrant.com/products/topbraid-composer/)|TopBraid Composer Maestro Edition is used to develop ontology models, configure data source integration, and create semantic services and user interfaces.|[Commercial tool](https://www.topquadrant.com/legal/)||
|[VocBench](http://vocbench.uniroma2.it/)|a web-based, multilingual, collaborative development platform for managing OWL ontologies, SKOS(/XL) thesauri, Ontolex-lemon lexicons and generic RDF datasets.|[License](https://bitbucket.org/art-uniroma2/vocbench3/src/master/LICENSE)||Desktop application|

Tools that are discovered from the Bio.Tools platform.
|Tool|Description|License|Topics|Platform|
|---|--|--|--|--|--|

## Implementation examples
To show how these tools can be used in real life examples, please check the related recipes.
- [Which vocabulary to use?](https://fairplus.github.io/the-fair-cookbook/content/recipes/interoperability/selecting-ontologies.html)
- [Building an application ontology with Robot](https://fairplus.github.io/the-fair-cookbook/content/recipes/interoperability/ontology-robot-recipe.html)



