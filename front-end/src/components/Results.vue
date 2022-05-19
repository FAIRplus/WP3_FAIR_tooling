<template>
<div>
  <div id='url'>
    <h5>URL:</h5>
    <p><a :href="build_url(run_id) " target='_blank'>{{ build_url(run_id) }}</a></p>
  </div>
  <v-expansion-panels 
    style="width:60%" 
    flat 
    hover>
    <v-expansion-panel >
      <v-expansion-panel-header>
        <h5>Input parameters</h5>
        <template v-slot:actions>
            <v-icon color="success">
              mdi-arrow-down-drop-circle-outline
            </v-icon>
          </template>
      </v-expansion-panel-header>
      <v-expansion-panel-content>
        <div style="width:100%, padding-top:1%">
          <v-data-table
            :headers="inputsHeaders"
            :items="inputParameters"
            :items-per-page="10"
            class="elevation-2"
          ></v-data-table>
        </div>
      </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  <br>
    <v-expansion-panels 
        flat 
        v-model="panel"
        hover>
      <v-expansion-panel
      expand
      v-model="panel">
      <v-expansion-panel-header>
        <h4>Results</h4>
        <template v-slot:actions>
            <v-icon color="success">
              mdi-arrow-down-drop-circle-outline
            </v-icon>
          </template>
      </v-expansion-panel-header>
      <v-expansion-panel-content>
        <div>
          <Table :tools="tools"/>
        </div>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</div>
</template>



<script>
import Table from './Table.vue'
export default {
  name: 'Results',
  props: ['tools', 'inputParameters', 'run_id'],
  components: {
    Table
    },
  data () {
    return {
      inputsHeaders: [
                {text: 'Keyword', value: 'keyword'},
                {text: 'Weight', value: 'weight'}
            ],
      activeResults: true,
      search: '',
      selected: null,
      isHovering: false,
      longResults:[],
      panel: 0
    }},
  methods:{
        build_url(id){
      if(this.tools.length===0){
        return('')
      }else{
        var url = 'https://fair-tool-discoverer.bsc.es/run/' + id
        return(url)
      }
    }
}}
</script>