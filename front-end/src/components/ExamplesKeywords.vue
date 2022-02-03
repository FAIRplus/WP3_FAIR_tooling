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
        {'label':'Ontology Annotation',
         'keywords':'Ontology annotation,1\n\
Semantic annotation,0.8\n\
Text mining,0.5\n\
Text annotation,0.5\n\
Entity tagging,0.5\n\
Entity recognition,0.75\n\
Named-entity and concept recognition,0.75\n\
Ontology and terminology,1\n\
Query expansion,0.75\n\
Free text mapping,1\n\
Text Annotation,1\n\
Annotation,0.5\n\
NLP,0.5\n\
Knowledge graph,0.5'},
        {'label':'Ontology Engineering',
        'keywords':'Module extraction,1\n\
Ontology slims,1\n\
Ontology and terminology,1\n\
Reasoning,0.5\n\
Reasoning Engine,1\n\
Semantic enrichment,0.7\n\
Customise ontology,1\n\
Update ontology,1\n\
Application ontology,0.8\n\
Ontology engineering,1'},
        {'label':'Ontology Management',
        'keywords':'Ontology and terminology,1\n\
Ontology Model,1\n\
Knowledge graph,0.8\n\
Vocabulary management,1\n\
Ontology identifier,1\n\
Ontology metadata,1\n\
Ontology visualisation,1\n\
Pntology management,1'},
        {'label':'Identifier Minting',
         'keywords':'Identifier Minting, 1\n\
Identifier resolution, 1\n\
GUID, 1\n\
Accession, 1\n\
Identifier, 1'},
        {'label':'Indentifier Mapping',
        'keywords':'Id mapping,1\n\
Accession,0.5\n\
Identifier,1\n\
Identifier mapping,1\n\
Accession mapping,1\n\
Database cross-mapping,1\n\
Cross-mapping,0.7'},
{'label':'Extract, Transform, Load', 
        'keywords':'Data store,1\n\
ETL,1\n\
Cloud migration,0.5\n\
Database replication,0.5\n\
dataflow,0.5\n\
integrat,1\n\
extract,1\n\
transform,1\n\
data cleaning,1\n\
loading,0.5\n\
validation,1\n\
data query,0.5\n\
provenance,0.5\n\
Data quality,0.5\n\
deposit,1\n\
format,0.3\n\
data unification,1\n\
workflow,0.5\n\
transfer,0.5\n\
Data integration and warehousing,0.7\n\
data governance,0.7\n\
Data identity and mapping,0.7\n\
Database management,0.7\n\
Data quality management,0.7\n\
parsing,0.7\n\
deposition,0.7\n\
formatting,0.7\n\
Query and retrieval,0.7\n\
Information extraction,0.7\n\
Format validation",0.7'}
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
