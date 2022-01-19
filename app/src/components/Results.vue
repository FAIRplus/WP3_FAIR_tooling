<template>
<div>
  <v-expansion-panels flat>
    <v-expansion-panel>
      <v-expansion-panel-header><h5>Input parameters</h5></v-expansion-panel-header>
      <v-expansion-panel-content>
        <div style="width:60%">
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
    <v-expansion-panels flat v-model="panel">
      <v-expansion-panel
      expand
      v-model="panel">
      <v-expansion-panel-header><h4>Results</h4></v-expansion-panel-header>
      <v-expansion-panel-content>
        <div>
          <v-data-table
            :class="table"
            v-model="rowSelect"
            :headers="headers"
            :items="tools"
            :items-per-page="10"
            :search="search"
            :sort-by="['score']"
            :sort-desc="[true]"
            multi-sort
            class="elevation-0" 
          >
            <template v-slot:top>
              <v-toolbar flat>
                <v-text-field
                    v-model="search"
                    append-icon="mdi-magnify"
                    label="Search"
                    single-line
                ></v-text-field>
                <v-spacer></v-spacer>
                </v-toolbar>
            </template>
            <template v-slot:[`body`]="{ items }">
              <tbody>
                <tr 
                  @click="rowSelect(key)" 
                  v-for="(item, key) in items" :key="item.Tool"
                >
                  <td>
                    <i  v-if="arrowsDownShow(key, item.Tool)" class="fas fa-angle-down cell-arrow"></i>
                    <i  v-if="arrowsUpShow(key, item.Tool)" class="fas fa-angle-up cell-arrow"></i>
                  </td>
                  <td>
                    <a :href="item.URL">{{ item.Tool }}</a>
                  </td>
                  <td>
                    <div v-for="type in item.Type" :key="type">
                      {{ dictGet(type)['text'] }}
                    <!-- Complete dictionary of types-->
                    </div>
                  </td>
                  <td>
                    <SourceAvatar :avatarProps='avatars.biotools'/>
                    <SourceAvatar :avatarProps='avatars.bioconda'/>
                    <SourceAvatar :avatarProps='avatars.github'/>
                    <SourceAvatar :avatarProps='avatars.bioconductor'/>
                    <SourceAvatar :avatarProps='avatars.galaxy'/>
                    </td>
                  <td>
                    {{ trimIfNotSelected(item.Description, key) }}
                  </td>
                  <td>
                    <ul>
                      <li v-for="(topic, Tool) in trimListIfNotSelected(item.Topics, key)" :key="Tool">
                        {{ topic }}
                      </li>
                      <span v-if="item.Topics.length > 3">...</span>
                    </ul>
                  </td>
                  <td>
                    <ul>
                      <li v-for="(operation, Tool) in trimListIfNotSelected(item.Operations, key)" :key="Tool">
                        {{ operation }}
                      </li>
                      <span v-if="item.Operations.length > 3">...</span>
                    </ul>
                  </td>
                  <td id="gd">
                    {{ item.Citations }}
                    <!-- Add publication in hover or icon next to number that opens the paper -->
                  </td>
                  <td>
                    {{ item.License }}
                    <!-- Match license to spdx -->
                  </td>
                  <td>
                    {{ item.keywords_score }}
                  </td>
                </tr>
              </tbody>
            </template>
          </v-data-table>
        </div>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</div>
</template>

<style scoped>
.v-data-table >>> th {
  font-size: smaller !important; 
}

.v-data-table.v-data-table.v-data-table >>> tr:hover  {
  background-color: white !important;
}

.v-data-table.v-data-table.v-data-table >>> td  {
  font-size: smaller !important;
  padding: .5em .5em 1em 1em;
}
#descr_panel{
  font-size: smaller !important;
}

.cell-arrow{
  color: darkgray;
}

.avatar-source{
  margin-top: 0.4em;
  margin-right: 0.2em;
}

.gd{
  padding: 0%;
  margin: 0%
}
.gd .modebar{
      display: none !important;
}
</style>

<script>
import SourceAvatar from './SourceAvatar.vue'
import Plotly from 'plotly.js-dist-min'
var layout = {title:false,
              showlegend: false,
              margin: { l:10, t:10, b:14, r:10}}
var trace1 = {
  x: [2017, 2018, 2019, 2020],
  y: [2, 14, 23, 35],
  type: 'scatter'
};

var trace2 = {
  x: [2017, 2018, 2019, 2020],
  y: [0, 0, 3, 15],
  type: 'scatter'
};

var data = [trace1, trace2];

export default {
  name: 'Results',
  props: ['tools', 'inputParameters'],
  components: {
    SourceAvatar
  },
  data () {
    return {
      activeResults: true,
      avatars: {
        biotools: {
          src:'elixir-logo.svg',
          color:'orange',
          content:'bio.tools',
          url:'bio.tools'
        },
        bioconda: {
          src:'bioconda-logo.svg',
          color:'#005500',
          content:'bioconda',
          url:''
        },
        github: {
          src:'github-logo.svg',
          color:'black',
          content:'GitHub',
          url:'github.org'
        },
        bioconductor: {
          src:'bioconductor-logo.svg',
          color:'#2f93ba',
          content:'Bioconductor',
          url:''
        },
        galaxy: {
          src: 'galaxy-logo.svg',
          color: '#134798',
          content: 'Galaxy Eu',
          url:''
        }
      },
      panel: 0,
      search: '',
      selected: null,
      isHovering: false,
      longResults:[],
      headers: [
        {text: '', align: 'start', sortable: false, value: 'down', width: '1em'},
        {text: 'Tool', align: 'start', sortable: false, value: 'Tool'},
        {text: 'Type of Software', value: 'Type'},
        {text: 'Sources', value: 'sources'},
        {text: 'Description', value: 'Description', width: '20rem'},
        {text: 'Related Topics', value: 'Topics', width: '12rem'},
        {text: 'Functionality', value: 'Operations', width: '12rem'},
        {text: 'Number of Citations', value: 'Citations',  width: '12rem'},
        {text: 'License', value: 'License'},
        {text: 'Score', value: 'keywords_score'}
      ],
      inputsHeaders: [
        {text: 'Keyword', value: 'keyword'},
        {text: 'Weight', value: 'weight'}
      ],
      typesAbb: {
        'Command-line tool' : {
          'text': 'CMD',
          'hover': 'Command-line Tool'
        },
        'Web application': {
          'text': 'Web',
          'hover': 'Web Application'
        },
        'unknown': {
          'text': 'Unknown',
          'hover': 'Unknown'
        }
      }
    }
  },
  mounted() {
    this.tools.forEach((item) => {
      if(item.Description.length>200){
        this.longResults.push(item.Tool)
        return
      }
      if(item.Topics.length>3){
        this.longResults.push(item.Tool)
        return
      }
    }),
    Plotly.newPlot("gd", /* JSON object */ {
      "data": data,
      "config": { "displayModeBar": false  },
      "layout": layout
    })
  },
  methods:{
    rowSelect(idx) {
      console.log('selected', idx)
      if(this.selected === idx){
        this.selected = null;
      } else {
        this.selected = idx;
      }
    },
    arrowsDownShow(idx, toolID){
      if(this.longResults.includes(toolID) && idx != this.selected){
        return(true)
      }else{
        return(false)
      }
    },
    arrowsUpShow(idx, toolID){
      if(this.longResults.includes(toolID) && idx === this.selected){
        return(true)
      }else{
        return(false)
      }
    },
    trimIfNotSelected(value, idx){
      if(this.selected === idx){
        return(value)
      }else{
        if(value.length > 255){
          var short = `${value.substring(0,200)}...`
        }else{
          return(value)
        }
        return(short)
      }
    },
    trimListIfNotSelected(list, idx){
      if(this.selected === idx){
        return(list)
      }else{
        var short_list = list.slice(0,3)
        return(short_list)
      }
    },
    dictGet(key) {
      var result = this.typesAbb[key] || {'text':'', "hover":''}
      return(result)
    }
  }
}
</script>
