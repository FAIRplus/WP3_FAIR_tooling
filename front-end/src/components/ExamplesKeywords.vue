<template>
<div>
  <v-row>
  <v-col cols="14" id='main-col'>
    <v-card elevation="0" id="examples-cont">
      <p><b>Example keyword lists</b></p>
      <v-btn 
      v-for="item in texts" 
      :key="item.PreferredLabel"
      dark
      outlined
      max-width="13.5em"
      min-width="4em"
      min-height="4.5em"
      small
      :color="item.color"
      @click="sampleInput(item.keywords)">
        {{ item.label }}
      </v-btn>
    </v-card>
  </v-col>
  </v-row>
</div>
</template>
<style scoped>
#examples-cont{
  text-align: center;
  margin-top: 0;
  margin-left: 4%;
  margin-right: 1%;
  border-width: 1px;
}

#main-col{
  padding: 0;
}

.v-btn{
  text-transform: unset !important;
  margin: .4em;
  font-size: .7rem;
  white-space: normal;
  display: inline-block;
}


.text {
  color: black;
}
.card{
  margin: .3rem;
  font-size: 0.8em;
  padding-top: 0.2rem;
  padding-bottom: 0.2rem;
  padding-right: 0%;
  padding-left: 0%;
  text-align: center;
}
.v-card > p{
  font-size: 1.1rem;
  color: #454545;
  font-family: 'Lexend Deca'
}

.row > p{
  margin-bottom: .5em;
}

</style>

<script>
import IDminting from '../assets/IDminting.json'
export default {
  name: 'ExamplesKeywords',
  props: [],
  data() {
    return {
      IDminting : IDminting,
      texts: [{'label':'Ontology Annotation','color': '#ad6911', 'keywords': []},
      {'label':'Ontology Management','color': '#ad6911', 'keywords': []},
      {'label':'Ontology Engineering', 'color': '#ad6911', 'keywords': []},
      {'label':'Identifier Minting', 'color': '#8A2549', 'keywords': IDminting},
      {'label':'Identifier Mapping', 'color': '#8A2549', 'keywords': []},
      {'label':'Extract, Transform, Load', 'color': '#484848','keywords': []}],
      texts__ : [
        {'label':'Extract, Transform, Load', 
        'keywords':'Data integration and warehousing, 1\n\
data governance, 1\n\
Data identity and mapping, 1\n\
Data submission annotation and curation, 1\n\
Database management, 1\n\
workflows, 1\n\
Data quality management, 1\n\
parsing, 1\n\
deposition, 1\n\
aggregation, 1\n\
formatting, 1\n\
Query and retrieval, 1\n\
Information extraction, 1\n\
Format validation, 1\n\
data store, 1\n\
data warehous, 1\n\
data lake, 1\n\
aggregated data, 1\n\
ETL, 1\n\
Ingest, 1\n\
Retriev, 1\n\
Cloud migration, 1\n\
Database replication, 1\n\
dataflow, 1\n\
integrat, 1\n\
extract, 1\n\
transform, 1\n\
data cleaning, 1\n\
loading, 1\n\
validat, 1\n\
query, 1\n\
provenance, 1\n\
Database management, 1\n\
Data quality, 1\n\
parsing, 1\n\
deposit, 1\n\
format, 1\n\
data unification, 1\n\
provenance, 1\n\
workflow, 1\n\
transfer'},
        {'label':'Ontology Annotation',
         'keywords':'Ontology annotation, 1\n\
Semantic annotation, 1\n\
Text mining, 1\n\
Entity tagging, 1\n\
Entity recognition, 1\n\
Query expansion, 1\n\
Named-entity and concept recognition, 1\n\
Ontology and terminology, 1\n\
Text annotation, 1\n\
Free text mapping, 1\n\
Ontology and terminology, 1\n\
Entity recognition, 1\n\
Semantic enrichment, 1'},
        {'label':'Identifier minting',
         'keywords':'Identifier minting, 1\n\
Identifier resolution, 1\n\
GUID, 1\n\
Accession, 1\n\
Identifier, 1'}
      ]
    }
  },
  methods: {
    sampleInput(item){
      this.$emit("click", item)
    }
  }
}
</script>
