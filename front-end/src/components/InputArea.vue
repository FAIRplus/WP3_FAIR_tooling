<template>
  <v-container fluid>
    <v-row>
      <v-row>
        <v-col cols="6">
          <v-autocomplete
            v-model="input"
            :items="EDAM_items"
            :search-input.sync="cachedterms"
            cache-items
            placeholder="Start typing to search EDAM terms"
            prepend-icon="mdi-magnify-expand"
            color="#300761"
            :loading="isLoading"
            label="Search terms"
            chips
            hide-no-data
            hide-selected
            item-text="PreferredLabel"
            small-chips
          >
          </v-autocomplete>
        </v-col>
        <v-col cols="2">
          <v-btn
              color="#300761"
              dark
              rounded
              @click="addItem"
            >
            <small> ADD TERM <br>TO SEARCH</small><v-icon>mdi-plus</v-icon>
          </v-btn>
        </v-col>
      </v-row>
    <v-row>
      <v-col cols="8">
        <v-card
          elevation="1">
          <v-card-text>
            <v-row v-for="(item) in terms" :key="item">
              <v-col cols="6">
                <v-text-field 
                    v-model="item['label']"
                    :disabled="!isEditing"
                    class="mt-0 pt-0"
                    single-line
                    color="purple darken-2"
                    background-color='white'
                    filled
                    hide-details="auto"
                    dense
                  >
                </v-text-field>
              </v-col>
              <v-col cols="2">
                <v-text-field 
                  v-model="item['weight']"
                  :disabled="!isEditing"
                  class="mt-0 pt-0"
                  single-line
                  align="right"
                  color="purple darken-2"
                  background-color='white'
                  filled
                  dense
                  hide-details="auto"
                >
                </v-text-field>
              </v-col>
              <v-col cols="2">
                <EditBtn :isEditing="isEditing" @click='edit' />
                <DeleteBtn @click="remove"/>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="1">
              </v-col>
              <v-col cols="2">
                <v-btn
                  color="success"
                  dark
                  id="launch-btn"
                  @click="runDiscoverer(terms)"
                >
                <small> RUN <br> SEARCH</small><v-icon>mdi-rocket-launch</v-icon>
                </v-btn>
                <div id='spacer'>
                  </div>
              </v-col>
            </v-row>       
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="4">
      <ExamplesKeywords @click='sampleInput'/>
      </v-col>
      </v-row>
    </v-row>
  </v-container>
</template>
<style scoped>
.v-card{
  margin-top: 0%;
  padding: auto;
  overflow: wrap;
}
.v-card >>> .v-text-field{
  font-size: .9rem;
}
.v-card >>> .v-row{
  margin-top: 0%;
  padding-top: 0%;
  margin-bottom: 0%;
  padding-bottom: 0%;
  font-size: small
}
.v-card >>> .v-col{
  margin-top: 0%;
  padding-top: 0%;
  margin-bottom: 0%;
  padding-bottom: 0%;
}
.v-autocomplete{
  padding-top: 0%;
  font-size: .9rem
}
.v-autocomplete >>> .v-icon{
  color:#300761;
}
.v-btn{
  padding-right: 0
}
.v-card >>> .v-icon{
  padding-left: .25em;
  padding-right: 0;
  margin-right: 0
}
#launch-btn{
  position: absolute;
  bottom:18%;
  left: 92%;
  width: 7em;
  transform: translateX(-50%); /* Move 50% of own width to the left*/
}

#spacer{
  width: 7em; 
  height: 4.2em; 
}
</style>

<script>
import EditBtn from './EditBtn.vue'
import DeleteBtn from './DeleteBtn.vue'
import EDAM from "../assets/EDAM_1.25.json";
import ExamplesKeywords from '../components/ExamplesKeywords.vue';

export default {
  name: 'InputArea',
  components: { 
    EditBtn,
    DeleteBtn,
    ExamplesKeywords
    },
  props: [],
  data () {
      return {
        terms:[],
        isEditing: false,
        hover:[],
        btns: {'edit':{'icon':'mdi-pencil', 'text':'Edit'},
               'delete':{'icon':'mdi-trash-can-outline', 'text':'Remove'}
              },
        EDAM_items: EDAM
      }
    },
  methods: {
    addItem(){
      console.log('here'+this.input)
      if(this.input==undefined){
        var item = {'label':this.cachedterms, 'weight':100}
      }else{
        item = {'label':this.input, 'weight':100}
      }
      this.terms.push(item)
      this.input = ''
      this.cachedterms = []
    },
    edit(){
      this.isEditing = !this.isEditing
    },
    remove(){
      this.terms.pop(this.item)
    },
    sampleInput (keywords) {
      this.terms = []
      for(let i=0; i<keywords.length;i++){
        this.terms.push({'label':keywords[i]['label'], 'weight':keywords[i]['weight']})
      }
      this.input = ''
      this.cachedterms = []
    },
    runDiscoverer(terms){
      this.$emit("click", terms)
    }
  }
}
</script>
