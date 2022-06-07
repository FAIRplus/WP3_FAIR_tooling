<template>
  <div class="v-container" id="index-main">
    <v-row>
      <h6><span class="question-icon"><i class="fas fa-question-circle"></i></span>
      How does the FAIRification Tool Discoverer work?</h6>
      <v-col cols="12" class="column">
        The <b>FAIRification Tool Discoverer</b> identifies tools from public archives for given 
        FAIRification capacities. 
        The tools are collected from 
        <a href="https://bio.tools/" target="_blank">Elixir Bio.tools<sup class="link-icon"><i class="fas fa-external-link-alt"></i></sup></a>, 
        <a href="https://openebench.bsc.es/" target="_blank">OpenEBench<sup class="link-icon"><i class="fas fa-external-link-alt"></i></sup></a>, 
        <a href="https://www.bioconductor.org/" target="_blank">Bioconductor<sup class="link-icon"><i class="fas fa-external-link-alt"></i></sup></a>, 
        <a href="https://usegalaxy.eu/" target="_blank">Galaxy EU<sup class="link-icon"><i class="fas fa-external-link-alt"></i></sup></a>,
        <a href="galaxy toolshed" target="_blank">Galaxy Toolshed<sup class="link-icon"><i class="fas fa-external-link-alt"></i></sup></a>, 
        <a href="https://github.com/" target="_blank">Github<sup class="link-icon"><i class="fas fa-external-link-alt"></i></sup></a>, 
        <a href="https://bitbucket.org/" target="_blank">Bitbucket<sup class="link-icon"><i class="fas fa-external-link-alt"></i></sup></a>
         and <a href="https://sourceforge.net/" target="_blank">Sourceforge<sup class="link-icon"><i class="fas fa-external-link-alt"></i></sup></a>. 
        <br>
        The FAIRification capacities are selected from <a href="https://fairplus-project.eu/" target="_blank">FAIRplus<sup class="link-icon"><i class="fas fa-external-link-alt"></i></sup></a>
        FAIRification experience and annotated using the <a href="https://edamontology.org/page" target="_blank">EDAM</a> ontology. 
        The tool list is ranked by confidence and relevance.
      </v-col>
    </v-row>
    <v-row>
      <h6><span class="question-icon"><i class="fas fa-question-circle"></i></span>
        Input format</h6>   
      <v-col cols="12" class="column">
        Introduce a term in the input bar and click "Add term to search" to include it into the kywords list to search. While typing, similar EDAM terms will be dispalyed as a dropdown. 
        The list of keywords to search is displayed under the input bar as the terms are added to it.
        The grey label on the right indicates the type os EDAM term, either 'operation' or 'topic'. Once a term is added to the list, you can modify its weight by clicking the 'Edit' bottom on the right.
        <v-card
        elevation=0>
        <div class="text-center">
          <v-img  src="@/assets/img/help_screenshot.png" max-width=600 style="margin:auto"></v-img>
        </div>
          <br><br><small style="align-text:center">See example keyword lists next to input box.</small>
          <br><br>
          </v-card>
        Weights are recommended to be in the range (0,1).
      </v-col>
    </v-row>
    <v-row>
      <h6><span class="question-icon"><i class="fas fa-question-circle"></i></span>
      Troubleshooting
      </h6>
      <v-col  cols="12" class="column">
        Empty lines and extra spaces are the main cause of input parsing errors. 
        If no tools match the query, a specific message will be displayed.
      </v-col>
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
.fas{
  margin-left: 1em;
  margin-right: 1em;
  margin-top: .9em;
  margin-bottom: .1em;
}
.question-icon{
  color:#900048;
  font-size: 1em
}
.link-icon{
  color:#300761;
  font-size: .5em;
  margin: 0%;
  padding: 0%;
}
.link-icon >>> i{
  margin-left: 0.25em;
  margin-right: 0.25em
}
.v-container >>> a{
  color:#300761 !important;
  text-decoration: none
}
.column{
  margin-left: 2em;
  margin-top: 0
}
</style>
<script>
export default {
  name: 'Help'
}
</script>
