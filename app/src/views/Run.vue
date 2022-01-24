<template>
  <div class="container run_main">
    <div class="row">
        <h4>Input</h4>
        <p>Enter keywords and their respective weights (optionally) to discover tools.</p>
        <div class="col-sm-8 d-flex">
            <form action="" method="post" id="input_text">
                <textarea v-model=inputTextarea name="input_data" class="form-control" id="input_textarea" aria-label=""></textarea>
                <!--div name="input_data" contenteditable="true" id="input_textarea"></div-->
                <small id="" class="form-text text-muted">For further axplanation on input format, see <a href="/help">here</a>.<br></small>
                <button type="button" name="run" value="Run" v-on:click=runDiscoverer class="input-run-btn" id="run_button">Run</button>
                <span v-if=formatErrorVisible id="errorFormat"><i class="fas fa-times"></i> Error: invalid format detected in line <span v-html="lineNum"></span></span>
            </form>
        </div>
        <div class="col-sm-4 d-flex">
          <ExamplesKeywords @click='sampleInput'/>
       </div>
    </div>
      <div>
        <div v-if=querying style="min-height: 4px;">
          <!-- query progress bar, see eaxample https://github.com/vuetifyjs/vuetify/blob/master/packages/docs/src/examples/v-progress-linear/prop-query.vue -->
          <v-progress-linear
            v-model="value"
            :active="show"
            :indeterminate="query"
            :query="true"
          ></v-progress-linear>
        </div>
        <Results v-if="resultsVisible" :tools="results.result" :inputParameters="results.input_parameters" />
        <div v-if="results_not_found" class='center_img'><img src="@/assets/img/not_found.png" width="50px"> No results found</div>
        <div v-if="error" class='center_img'><img src="@/assets/img/error.png" width="50px"> Something went wrong</div>
      </div>
</div>
</template>
<script>
import Results from '../components/Results.vue'
import ExamplesKeywords from '../components/ExamplesKeywords.vue'
import axios from 'axios'
export default {
  name: 'Run',
  components: {
    Results,
    ExamplesKeywords
  },
  data () {
    return {
      inputTextarea: '',
      formatErrorVisible: false,
      lineNum: 0,
      results: [],
      querying: false,
      resultsVisible: false,
      value: 0,
      query: false,
      show: true,
      interval: 0,
      results_not_found: false,
      error: false,
      inputParameters: [
        {
          keyword: 'ontology mapping',
          weight: '0.8'
        },
        {
          keyword: 'ontology crosswalk',
          weight: '0.9'
        }
      ]
    }
  },
  methods: {
    sampleInput (text) {
      this.inputTextarea = text
      this.resultsVisible = false
    },
    clearInput () {
      this.inputTextarea = ''
    },
    async runDiscoverer () {
      this.results = []
      var fCorrect = this.formatCorrect()
      if (fCorrect === true) {
        console.log('Correct format, RUN!')
        this.formatErrorVisible = false
        this.querying = true
        this.query = true
        this.results_not_found = false
        this.error = false
        this.ToolDiscovererCall()
        console.log('done')
      } else {
        this.lineNum = fCorrect
        this.formatErrorVisible = true
      }
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
    ToolDiscovererCall () {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:5000/',
        data: {
          textarea_content: this.inputTextarea
        },
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      })
        .then(
          (response) => {
            this.results = response.data.message
            this.querying = false
            if(response.data.code==='ERROR'){
              this.resultsVisible = false
              this.results_not_found = false
              this.error = true

              console.log('ERROR:')
              console.log(response.data.message)
            }
            else{
              console.log('NO ERROR HERE')
              this.resultsVisible = this.results.result_found
              this.results_not_found = !this.results.result_found
              this.error = false
              }
          })
    }
  }
}
</script>
<style>
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
  font-size: smaller;
  width: 100%;
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

</style>
