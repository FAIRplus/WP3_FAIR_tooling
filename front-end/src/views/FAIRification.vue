<template>
  <div class="v-container" id="index-main">
    <h6><span class="tools-icon"><i class="fas fa-tools"></i></span>
    What tools to use for FAIRification tasks?</h6>
    <p>
    The <b>FAIRification Tool Discoverer</b> suggests tools for common FAIRification tasks. <br>
    The tools are collected from public archives and curated for FAIRification capabilities 
    (see details in <a href="/Help">About</a>).
    </p>
    
    <p>Below are some manually curated tool lists.</p> 
    <ul>
      <li>Data vocabulary/ontology</li>
      <li>ETL process</li>
    </ul>
    <p>
    For detailed information about using such tools, or how to perform FAIRification, 
    please check the <a href="https://fairplus.github.io/the-fair-cookbook/content/home.html">FAIR Cookbook</a>.
    </p>
    <v-row class="lists">
    <v-col cols="6">
      <p>Some manually curated tool lists are shown below:</p>
    <v-expansion-panels>
      <v-expansion-panel
        v-for="(item) in keyw_lists"
        :key="item"
      >
        <v-expansion-panel-header>
          {{item.label}}
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <div v-for="(keyword) in item.terms" :key="keyword">
            {{keyword}}
          </div>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
    </v-col>
    </v-row>    
    <v-row>
    <p>
    For detailed information about using such tools, or how to perform <i>FAIRification</i>, 
    please check the <a href="https://fairplus.github.io/the-fair-cookbook/content/home.html">FAIR Cookbook<sup class="link-icon"><i class="fas fa-external-link-alt"></i></sup></a>.
    </p>
    </v-row>
  </div>
</template>
<style scoped>
#index-main {
  font-size: .9rem;
  margin-bottom: 3%;
  width: 62%;
  margin: auto
}
.lists{
  margin-bottom: 1em
}
.fas{
  margin: 1em
}
.tools-icon{
  color:#f99768;
  font-size: 1.5em
}
.v-container >>> a{
  color:#300761 !important;
  text-decoration: none
}
.link-icon{
  color:#300761;
  font-size: .6em;
  margin: 0%;
  padding: 0%
}
.link-icon >>> i{
  margin-left: 0.25em;
  margin-right: 0.25em
  }
.v-container {
  font-size: .2rem;
  margin-bottom: 3%;
  width: 90%;
}

</style>
<script>
export default {
  name: 'FAIRification',
  data () {
    return {
      keyw_lists : [
        {'label':'Data vocabulary/ontology','terms': ['Ontology annotation','Semantic annotation','Text mining',
'Text annotation','Entity tagging','Entity recognition','Named-entity and concept recognition',
'Ontology and terminology','Query expansion','Free text mapping','Text Annotation','Annotation','NLP']},
        {'label':'ETL process','terms': ['Data integration and warehousing','Data governance',
        'Data identity and mapping','Database management','Data quality management','Query and retrieval',
        'Information extraction','Format validation']}
      ]
    }
  }
}
</script>
