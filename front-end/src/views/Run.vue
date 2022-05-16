<template>
  <div class="container run_main">
    <v-row class='first-parag'>
        <h4>Disover Tools</h4>
    </v-row >
    <p>Introduce search terms and respective weights (optionally).</p>
    <InputArea @click='runDiscoverer'/>
      <div class="main-results">
        <div v-if=querying style="min-height: 4px;">
          <!-- query progress bar, see eaxample https://github.com/vuetifyjs/vuetify/blob/master/packages/docs/src/examples/v-progress-linear/prop-query.vue -->
          <v-progress-linear
            v-model="value"
            :active="show"
            :indeterminate="query"
            :query="true"
          ></v-progress-linear>
        </div>
        <div v-if="results"><Results :tools="results.result" :inputParameters="results.input_parameters" :run_id="results.run_id" /></div>
        <div v-if="results_not_found" class='center_img' id="not_foundm"><img src="@/assets/img/not_found.svg" width="50px"> No tools found for those keywords</div>
        <div v-if="error" class='center_img' id="errorm"><img src="@/assets/img/error.svg" width="50px"> Something went wrong while fetching results</div>
      </div>
</div>
</template>
<script>
import Results from '../components/Results.vue'
import InputArea from '../components/InputArea.vue'
import axios from 'axios'
export default {
  name: 'Run',
  components: {
    Results,
    InputArea
  },
  created() {
    // watch the params of the route to fetch the data again
    this.$watch(
      () => this.$route.params,
      () => {
        this.fetchDataRes()
      },
      // fetch the data when the view is created and the data is
      // already being observed
      { immediate: true }
    )
  },
  data () {
    return {
      inputTextarea: '',
      formatErrorVisible: false,
      lineNum: 0,
      results: null,
      querying: false,
      value: 0,
      query: false,
      show: true,
      interval: 0,
      results_not_found: false,
      error: false,
      terms:[]
    }
  },
  methods: {
    fetchDataRes() {
      if(this.$route.params.run_id){
        this.query = true
        this.querying = true
        axios.get('https://fair-tool-discoverer.bsc.es/api/result/fetch', {
        params : {
          id : this.$route.params.run_id
        },
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then((response) => {
        console.log(response.data.message.results)
        this.results = response.data.message
        this.results_not_found = !this.results.result_found
        this.query = false
        this.querying = false
        this.error = false
      })
      .catch((error) => {
        console.log(error)
        this.query = false
        this.error = true
        this.querying = false
      });
      }else{
        this.results = null
      }
    },
    clearInput () {
      this.inputTextarea = ''
    },
    async runDiscoverer (terms) {
      this.results = null
      this.terms = terms
      console.log(this.terms)
      this.formatErrorVisible = false
      this.querying = true
      this.query = true
      this.results_not_found = false
      this.error = false
      this.ToolDiscovererCall(terms)
      console.log('done')
    },
    formatCorrect () {
      var lines = this.inputTextarea.split(/\r?\n/g)
      var csvLineRegex = /^([^\r\n;]*),([" *"]?\d+(\.\d+)?)$/
      for (var i = 0; i < lines.length; i++) {
        var lineValid = csvLineRegex.test(lines[i])
        if (lineValid === true) {
          continue
        } else {
          return i + 1
        }
      }
      return true
    },
    ToolDiscovererCall (terms) {
      axios({
        method: 'post',
        url: 'https://fair-tool-discoverer.bsc.es/api/',
        data: {
          textarea_content: terms
        },
        headers: {
          'Content-Type': 'application/json'
          }
      })
        .then(
          (response) => {
            this.results = response.data.message
            this.querying = false
            console.log('NO ERROR HERE')
            this.results_not_found = !this.results.result_found
            this.error = false
            })
        .catch((error) => {
          console.log(error)
          this.query = false
          this.querying = false
          this.error = true
          this.results = null
          })
    }
    }
  }
</script>
<style scoped>
#errorFormat{
  color: darkred;
  font-size: small;
}
.input-run-btn{
    width: 3em;
    border: 1px solid green;
    background-color: green;
    color: white;
    font-weight: bold;
    margin: 1em;
    margin-left: 0;
}
.input-aid-btn{
    border: 1px solid grey; 
    color: grey;
    background-color: white;
    padding: 2%;
    margin: 2px;
    width: 100%;
    margin-top: 1em;
}
.input_label{
    font-size: smaller;
    font-weight: bold;
}
.run_main{
  text-align: left;
  align-items: left;
  margin-bottom: 2em;
  font-size: .9rem;
  width: 100%;
  font-family: "Lexend";
}
.first-parag{
  margin-bottom: 2em
}
.center_img img{
  display: block;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 1em;
  margin-top: 1em;
}
.center_img{
  text-align: center;
}
#errorm{
  color: #900048
}
#not_foundm{
  color: #300761
}
#inputdiv{
  margin-top: 0%;
  padding-top: 0%
}
.main-results{
  margin-top: 3em
}
</style>
