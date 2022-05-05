<template>
    <td>
        <div v-if="pubPlotProps.citations.length!=0">
            <div :id="pubPlotProps._id" class="plot"></div>
        </div>
    </td>
</template>

<script>
import Plotly from 'plotly.js-dist-min'

var layout = {title:false,
              showlegend: false,
              hoverlabel: { bgcolor: "#FFF" },
              margin: { l:0, t:0, b:0, r:0},
              font: {size: 9},
              width: 200,
              height: 100,
              yaxis: {
                title: {
                  text: 'count',
                  standoff: 8,
                  font: {
                    size: 8
                  }},
              tickformat: 'd',
              automargin: true
              },
              xaxis : {
                title: {
                  text: 'year',
                  standoff: 5,
                  font: {
                    size: 8
                  }
                },
                tickangle: 30,
                tickformat: 'd',
                automargin: true
                }};

export default {
    name: 'CitationsCol',
    props: ['pubPlotProps'],
    data() {
        return {
        labels : [],
        plot:true
        }
    },
    mounted() {
        if(this.pubPlotProps.citations.length === 0){
            this.plot = false
        }
        else{
            this.plot = true
            Plotly.newPlot(this.pubPlotProps._id, /* JSON object */ {
            "data": this.build_traces(),
            "config": { "displayModeBar": false  },
            "layout": layout
            }
        )}
    },
    methods: {
        build_traces(){
            var traces = []
            for (let i = 0; i < this.pubPlotProps.citations.length; i++) {
                var pub = this.pubPlotProps.citations[i]
                var new_data = {x : pub['trace']['x'], 
                                y : pub['trace']['y'],
                                name: pub['title'],
                                type: 'scatter',
                                text: Array(pub['trace']['x'].length).fill(pub['title']),
                                hovertemplate: 
                                    "year: %{x:d} </br></br>" + 
                                    "count: %{y:d}" +
                                    "<extra></extra>",
                                mode: 'lines+markers',
                                line: {
                                    width: 1
                                    },
                                marker:{
                                    size: 4
                                    }
                                }
                this.labels.push(pub['title'])
                traces.push(new_data)
                }
            return(traces)
        }
    }
}

</script>

<style scoped>
#plot{
  padding: 0%;
  margin: 0%
}
#plot .modebar{
    display: none !important;
}
</style>