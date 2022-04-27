<template>
    <div>
        <v-card elevation="2" style="margin-bottom:4em; margin-top:2em">
            <v-col cols="12" class="py-2">
            <h5>
                Filters
            </h5>
            </v-col>
            <v-col
            cols="12"
            class="py-2"
            >
                <p>
                    Availability
                </p>
                <v-btn-toggle
                v-model="toggle_sources"
                multiple
                dense
                group
                >
                    <FilterBtn 
                        v-for="label in filtersMapping.sources" 
                        :key="filtersMapping.sources.indexOf(label)" 
                        :label="label" 
                        icon />
                    
                </v-btn-toggle>
            </v-col>
            <v-col
            cols="12"
            class="py-2"
            >
                <p>
                    Type of Software
                </p>
                <v-btn-toggle
                    v-model="toggle_types"
                    multiple
                    dense
                    group
                >   
                    <FilterBtn  
                        v-for="item in filtersMapping.types" 
                        :key="filtersMapping.types.indexOf(item)" 
                        :label="item" 
                        />

                </v-btn-toggle>
            </v-col>
        </v-card >
    <v-data-table
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
    <template v-slot:[`body`]="{ items }">
        <tbody>
        <tr 
            @click="rowSelect(key)" 
            v-for="(item, key) in items" :key="item._id.toString()"
        >
            <td>
            <i  v-if="arrowsDownShow(key, item.name)" class="fas fa-angle-down cell-arrow"></i>
            <i  v-if="arrowsUpShow(key, item.name)" class="fas fa-angle-up cell-arrow"></i>
            </td>
            <td>
            <b><big>{{ item.name }}</big></b>
            </td>
            <td>
                {{ dictGet(item.type).hover }}
            </td>
            <td>
            <SourceAvatar 
                v-for="source in avatars"
                :key="source.content" 
                :avatarProps="source"
                :sources_labels='item.sources_labels' />

            </td>
            <td>
            <span v-html="descriptionSpan(trimIfNotSelected(item.description[0], key))"></span>
            </td>
            <td>
            <ul>
                <li v-for="(topic, name) in trimListIfNotSelected(item.edam_topics, key)" :key="name">
                {{ topic.label }}
                </li>
                <span v-if="item.edam_topics.length > 5 && arrowsUpShow(key, item.name) == false">...</span>                      
            </ul>
            </td>
            <td>
            <ul>
                <li v-for="(operation, name) in trimListIfNotSelected(item.edam_operations, key)" :key="name">
                {{ operation.label }}
                </li>
                <span v-if="item.edam_operations.length > 5 && arrowsUpShow(key, item.name) == false">...</span>
            </ul>
            </td>
            <td>
            <ul>
                <div v-for="(pdata, year) in build_pubs(item, key)" :key="year" class='publications'>
                <v-icon class='fas fa-circle' :color = 'pdata.color' size="10"></v-icon> 
                <span v-html="pdata['label']" />
                    <a v-for="(link, year) in pdata['links']" :key="year"  :href="link" target="_blank">  
                    <i class='fas fa-external-link-alt' size="3"></i>
                    </a>
                </div>
            </ul>
            </td>
            <td>
            <PubPlot :pubPlotProps='item' v-if="item.citations.length!=0"/>
            </td>
            <td>
            {{ item.license[0] }}
            <!-- Match license to spdx-->
            </td>
            <td>
            {{ formatNumber(item.score) }} 
            </td>
        </tr>
        </tbody>
    </template>
    </v-data-table>
    </div>
</template>

<script>
import PubPlot from './PubPlot.vue'
import SourceAvatar from './SourceAvatar.vue'
import FilterBtn from './FilterBtn.vue'


export default {
    name : 'Table',
    props: ["tools"],
    components : {
        PubPlot,
        SourceAvatar,
        FilterBtn
    },
    data() {
        return {
            toggle_sources: [0,1,2,3,4,5,6],
            toggle_types: [0,1,2,3,4],
            activeResults: true,
            panel: 1,
            search: '',
            selected: null,
            isHovering: false,
            longResults:[],
            avatars: {
                biotools: {
                    src:'elixir-logo.svg',
                    color:'orange',
                    content:'bio.tools',
                    url:'bio.tools',
                    label: 'biotools',
                },
                bioconda: {
                    src:'bioconda-logo.svg',
                    color:'#005500',
                    content:'bioconda',
                    url:'',
                    label:'bioconda'
                },
                github: {
                    src:'github-logo.svg',
                    color:'black',
                    content:'GitHub',
                    url:'github.org',
                    label:'github'
                },
                bioconductor: {
                    src:'bioconductor-logo.svg',
                    color:'#2f93ba',
                    content:'Bioconductor',
                    url:'',
                    label:'bioconductor'
                },
                galaxy: {
                    src: 'galaxy-logo.svg',
                    color: '#134798',
                    content: 'Galaxy Eu',
                    url:'',
                    label: 'galaxy'
                },
                sourceforge: {
                    src: 'sourceforge-logo.svg',
                    color: '#ff6602',
                    content: 'SourceForge',
                    url:'',
                    label: 'sourceforge'
                },
                bitbucket: {
                    src: 'bitbucket-logo.svg',
                    color: '#005ed9',
                    content: 'Bitbucket',
                    url:'',
                    label: 'bitbucket'
                },
                other: {
                    src: 'other.svg',
                    color: '#535682',
                    content: 'Homepage',
                    url:'',
                    label: 'other'
                }
            },
            linksURLs: [
                {id : 'doi',  template : 'https://doi.org/'},
                {id : 'pmcid', template : 'https://www.ncbi.nlm.nih.gov/pmc/articles/'},
                {id : 'pmid', template :'https://pubmed.ncbi.nlm.nih.gov/'},
                {id : 'url', template: ''}
                ],
            inputsHeaders: [
                {text: 'Keyword', value: 'keyword'},
                {text: 'Weight', value: 'weight'}
            ],
            typesAbb: {
                'cmd' : {
                'text': 'CMD',
                'hover': 'Command-line Tool'
                },
                'web': {
                'text': 'Web',
                'hover': 'Web Application'
                },
                'db' : {
                'text': 'DB',
                'hover': 'Database'
                },
                'lib' : {
                'text': 'Lib',
                'hover': 'Library'
                },
                'unknown': {
                'text': 'Unknown',
                'hover': 'Unknown'
                }
            },
            plot_colors: [
            '#1f77b4',
            '#ff7f0e',
            '#2ca02c',
            '#d62728',
            '#9467bd',
            '#8c564b',
            '#e377c2',
            '#7f7f7f',
            '#bcbd22',
            '#17becf' 
            ],
            filtersMapping: {
                sources : ['biotools', 'github', 'bioconda','galaxy', 'sourceforge', 'bioconductor', 'bitbucket'],
                types : ['cmd', 'web', 'library', 'db', 'suite']
            }
        }
    }, 
    computed: {
        headers () {
            return [
                {text: '', align: 'start', sortable: false, value: 'down', width: '1em'},
                {text: 'Tool Name', align: 'start', sortable: false, value: 'name', width: '5rem'},
                {
                    text: 'Type of Software', 
                    value: 'type', 
                    width: '6rem',
                    filter: value => {
                        return this.filter(this.toggle_types, this.typeMapping, value)
                    }
                },
                {
                    text: 'Availability', 
                    value: 'source', 
                    width: '6rem', 
                    filter: value => {
                        return this.filter(this.toggle_sources, this.sourceMapping, value)
                        }
                },
                {text: 'Description', value: 'description', width: '13rem'},
                {text: 'Related Topics', value: 'edam_topics', width: '8rem'},
                {text: 'Functionality', value: 'edam_operations', width: '8rem'},
                {text: 'Publications', value: 'publications', width: '14rem'},
                {text: 'Number of Citations', value: 'publications',  width: '13rem'},
                {text: 'License', value: 'license', width: '5rem'},
                {text: 'Score', value: 'score', width: '3rem'}
                ]
            },
    },
    mounted() {
    this.tools.forEach((item) => {
      if(item.description[0].length>320){
        this.longResults.push(item.name)
      }
      if(item.edam_operations.length>5){
        this.longResults.push(item.name)
      }
      if(item.edam_topics.length>5){
        this.longResults.push(item.name)
      }
    })},
    methods : {
        filter(toggleArray, mappingFunct, value){
            /* Convert filters index to sources labels*/
            var mapped_filters = toggleArray.map(mappingFunct)
            
            /* Overlap between tool sources and filters*/
            const overlapArray = mapped_filters.filter(item => value.includes(item))
            /* If overlap, show tool */
            console.log(overlapArray)
            if(overlapArray.length>0){
                return value
            }else{
                return false
            }   
        },
        sourceMapping(x){
            return this.filtersMapping.sources[x]
        },
        typeMapping(x){
            return this.filtersMapping.types[x]
        },
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
        if(value.length > 320){
          var short = `${value.substring(0,320)} ...`
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
            var short_list = list.slice(0,5)
            return(short_list)
        }
        },
        dictGet(key) {
        var result = this.typesAbb[key] || {'text':key, "hover":key}
        return(result)
        },
        build_pubs(item){
        var labels = []
        for (let i = 0; i < item.citations.length; i++) {
            const links = []
            for(var k = 0; k < this.linksURLs.length; k++){
            const idType = this.linksURLs[k]['id']
            if(item.citations[i][idType]!=undefined){
                links.push(this.linksURLs[k]['template']+item.citations[i][idType]) 
            }
            }
            var label
            if(item.citations[i]['year'] == undefined){
            if(item.citations[i]['title'] == undefined){
                label = 'link'
            }else{
                label = item.citations[i]['title']
            }
            }else{
            label = `<span>${item.citations[i]['title']}(${item.citations[i]['year']})</span>`
            }
            labels.push({'label':label, 
                        'color':this.plot_colors[i],
                        'year':item.citations[i]['year'],
                        'links':links})
        }
        for (let e = 0; e < item.citations_other.length; e++) {
            const links = []
            for(var j = 0; j < this.linksURLs.length; j++){
            const idType = this.linksURLs[j]['id']
            if(item.citations_other[e][idType]!=undefined){
                links.push(this.linksURLs[j]['template']+item.citations_other[e][idType]) 
            }
            }
            label = ''
            if(item.citations_other[e]['title'] != '' && item.citations_other[e]['title'] != undefined){
            labels.push({'label': item.citations_other[e]['title'],
                        'color': 'black',
                        'year': null,
                        'links': links})
            }
        }
        return(labels)
        },
        formats(formats){
        var string = ''
        for (let i = 0; i < formats.length; i++) {
            if(i>0){
            string= string + ', ' + formats[i]
            }else{
            string= string + ': ' + formats[i]
            }
        }
        return(string)
        },
        span(title, year){
        const span = `${title} (${year})`
        return(span)
        },
        descriptionSpan(description){
        const html = `<span>${description}</span>`
        return(html)
        },
        formatNumber (num) {
        return parseFloat(num).toFixed(2)
        }
    }
}
</script>

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

#url{
  width: 96%;
  text-align: left;
  margin-right: auto;
  margin-left: auto;
}
#url p{
  text-indent: .7rem;
}

.publications >>> .fas{
  padding-right: .15em;
  padding-left: .15em;
  padding-bottom: .4em;
}

</style>