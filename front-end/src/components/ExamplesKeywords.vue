<template>
<div>
  <v-row>
  <v-col cols="14" id='main-col'>
    <v-card elevation="0" id="examples-cont">
      <p><b>Example keyword lists</b></p>
      <v-btn 
      v-for="item in texts" 
      :key="item.PreferredLabel"
      dark
      outlined
      max-width="13.5em"
      min-width="4em"
      min-height="4.5em"
      small
      :color="item.color"
      @click="sampleInput(item.keywords)">
        {{ item.label }}
      </v-btn>
    </v-card>
  </v-col>
  </v-row>
</div>
</template>
<style scoped>
#examples-cont{
  text-align: center;
  margin-top: 0;
  margin-left: 4%;
  margin-right: 1%;
  border-width: 1px;
}

#main-col{
  padding: 0;
}

.v-btn{
  text-transform: unset !important;
  margin: .4em;
  font-size: .7rem;
  white-space: normal;
  display: inline-block;
}


.text {
  color: black;
}
.card{
  margin: .3rem;
  font-size: 0.8em;
  padding-top: 0.2rem;
  padding-bottom: 0.2rem;
  padding-right: 0%;
  padding-left: 0%;
  text-align: center;
}
.v-card > p{
  font-size: 1.1rem;
  color: #454545;
  font-family: 'Lexend Deca'
}

.row > p{
  margin-bottom: .5em;
}

</style>

<script>
import IDminting from '../assets/IDminting.json'
import OntoAnno from '../assets/OntoAnno.json'
import OntoEng from '../assets/OntoEng.json'
import OntoMag from '../assets/OntoMag.json'
import IdMap from '../assets/IdMap.json'
import ETL from '../assets/ETL.json'


export default {
  name: 'ExamplesKeywords',
  props: [],
  data() {
    return {
      texts: [{'label':'Ontology Annotation','color': '#ad6911', 'keywords': OntoAnno},
      {'label':'Ontology Management','color': '#ad6911', 'keywords': OntoMag},
      {'label':'Ontology Engineering', 'color': '#ad6911', 'keywords': OntoEng},
      {'label':'Identifier Minting', 'color': '#8A2549', 'keywords': IDminting},
      {'label':'Identifier Mapping', 'color': '#8A2549', 'keywords': IdMap},
      {'label':'Extract, Transform, Load', 'color': '#484848','keywords': ETL}],
    }
  },
  methods: {
    sampleInput(item){
      this.$emit("click", item)
    }
  }
}
</script>
