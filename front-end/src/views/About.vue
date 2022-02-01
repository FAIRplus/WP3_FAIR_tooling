<template>
  <div class="v-container" id="index-main">
    <v-row>
      <h6><span class="question-icon"><i class="far fa-comment-dots"></i></span>
      Get in touch</h6>
      <v-col cols="12" class="column">
        Please get in touch with us by creating a ticket in the <a href="https://github.com/FAIRplus/WP3_FAIR_tooling/tree/app" target="_blank">GitHub repository<sup class="link-icon"><i class="fas fa-external-link-alt"></i></sup></a>. 
        We welcome feedback regarding:
        <ul>
          <li>Errors in the outcome</li>
          <li>Recommending tools or implementation examples.</li>
          <li>FAIRification use cases</li>
          <li>Others</li>
        </ul>
      </v-col>
    </v-row>
    <v-row>
      <h6><span class="question-icon"><i class="fas fa-users"></i></span>
      Acknowledgements
      </h6>
      <v-col  cols="12" class="column">
        This software is developed by 
        <a href="https://bsc.es" target="_blank">BSC-CNS<sup class="link-icon"><i class="fas fa-external-link-alt"></i></sup></a>
        and
        <a href="https://ebi.ac.uk" target="_blank">EMBL-EBI<sup class="link-icon"><i class="fas fa-external-link-alt"></i></sup></a>
        , and funded by the 
         <a href="https://fairplus-project.eu/" target="_blank">IMI FAIRplus project<sup class="link-icon"><i class="fas fa-external-link-alt"></i></sup></a>.
      </v-col>
    </v-row>
    <v-row>
      <h6><span class="question-icon"><i class="fas fa-info-circle"></i></span>
      Licensing
      </h6>
      <v-col  cols="12" class="column">
        The software is deployed under the <b><a href="https://github.com/FAIRplus/WP3_FAIR_tooling/blob/main/LICENSE" target="_blanck">Apache 2.0 license</a></b>.
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

.far{
  margin-left: 1em;
  margin-right: 1em;
  margin-top: .9em;
  margin-bottom: .1em;
}

.question-icon{
  color:#300761;
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
  name: 'About'
}
</script>
