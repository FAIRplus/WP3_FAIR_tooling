<template>
<div class="container" id="examples-cont">
  <div class="row flex-container" id="row">
    <p><b>Example keyword lists</b></p>
    <div type="button" v-for="item in texts" :key="item.label" class="col-sm-2 flex-item card" @click="sampleInput(item)">
      {{ item.label }}
    </div>
  </div>
  <div class="btn-group-vertical">
      <button type="button" class="input-aid-btn" id="input_clear_button" @click="sampleInput('')">Clear</button>
  </div>
</div>
</template>
<style scoped>
#examples-cont{
  text-align: center;
  

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
.row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap:wrap;
  gap: 10px;
  border-style: solid;
  border-color:lightgrey;
  border-width: 1px;
  margin-top: 1em;
  padding: .5em;
  }

.row > p{
  margin-bottom: .5em;
}

.flex-item {
  flex-grow: 1;
  flex-shrink: 0;
  flex-basis: 45%;
  align-self: center;
  text-align: center;
  min-width: 45%;
  width: 45%;
}

.btn-group-vertical{
  margin-top: 2rem;
}

</style>

<script>
export default {
  name: 'SourceAvatar',
  props: [],
  data() {
    return {
      texts : [
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
    sampleInput(n){
      this.$emit("click", n.keywords)
    }
  }
}
</script>
