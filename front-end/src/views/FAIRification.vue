<template>
  <div class="v-container" id="index-main">
    <h5><span class="tools-icon"><i class="fas fa-toolbox"></i></span>
    What tools to use for FAIRification tasks?</h5>
    <v-row>
    <p>
    The <b>FAIRification Tool Discoverer</b> suggests tools for common FAIRification tasks. 
    The tools are collected from public archives and curated for FAIRification capabilities 
    (see details in <a href="/Help">About<sup class="link-icon"><i class="fas fa-external-link-alt"></i></sup></a>).
    </p>
    </v-row>
    <v-row class="lists">
    <v-col cols="6">
      <p>Below are some manually curated tool lists:</p>
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

</style>
<script>
export default {
  name: 'FAIRification',
  data () {
    return {
      keyw_lists : [
        {'label':'Data vocabulary/ontology','terms': [1,2,3,4]},
        {'label':'ETL process','terms': [1,2,3,4,5]}
      ]
    }
  }
}
</script>
