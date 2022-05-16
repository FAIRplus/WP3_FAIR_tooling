<template>
  <v-container fluid>
    <v-row>
      <v-row>
        <v-col cols="6">
          <v-autocomplete
            v-model="input"
            :items="EDAM_items"
            :search-input.sync="cachedterms"
            :debounce-search="0"
            cache-items
            placeholder="Start typing to search EDAM terms"
            prepend-icon="mdi-magnify-expand"
            background-color="#f5f5f5"
            :loading="isLoading"
            label=""
            chips
            solo
            hide-no-data
            hide-selected
            :item-text="PreferredLabel"
            :item-value="PreferredLabel"
            small-chips
          >
             <template v-slot:selection="data">
                <v-chip
                      class="ma-2"
                      label
                      small
                      color="grey"
                      text-color="white"
                      >
                      {{ getLabel(data.item) }}
                    </v-chip>
                    {{data.item.PreferredLabel}}
                </template>
              <template v-slot:item="data">
                <template v-if="typeof data.item !== 'object'">
                  <v-list-item-content v-text="data.item"></v-list-item-content>
                </template>
                <template v-else>
                   <v-chip
                      class="ma-2"
                      label
                      small
                      color="grey"
                      text-color="white"
                      >
                      {{ getLabel(data.item) }}
                    </v-chip>
                  <v-list-item-content>
                    <v-list-item-title v-html="data.item.PreferredLabel"></v-list-item-title>
                  </v-list-item-content>
                </template>
              </template>
          </v-autocomplete>
        </v-col>
        <v-col cols="1">
          <v-btn
              color="#5750AA"
              dark
              id='add-btn'
              @click="addItem"
            >
            <small> ADD TERM <br>TO SEARCH</small><v-icon>mdi-plus</v-icon>
          </v-btn>
        </v-col>
      </v-row>
    <v-row>
      <v-col cols="8">
        <v-card
          elevation="1"
          id='terms-card'>
          <v-card-text>
            <v-row v-for="(item) in terms" :key="item">
              <v-col cols="6">
                <v-text-field 
                    v-model="item['label']"
                    :disabled="!item['isEditing']"
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
                  :disabled="!item['isEditing']"
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
                <EditBtn :isEditing="isEditing" @click='edit(item)' />
                <DeleteBtn @click="remove(item)"/>
              </v-col>
            </v-row>
            <v-row>
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
  font-size: .9rem;
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

.v-text-field >>> input{
  color: black   !important
}
#add-btn{
  width: 8em;
  padding-left:1.5em;
  padding-top: 8%;
  padding-bottom: 8%;
  height: 3em;
  margin-top: .2em;
}
#terms-card{
  border-color: #edebeb;
  border-style: solid;
  border-width: 1;
  min-height: 22em;
  min-width: 90%;
  margin-right: 5% 
}
#launch-btn{
  position: absolute;
  bottom:9%;
  left: 87%;
  width: 7em;
  transform: translateX(-50%); /* Move 50% of own width to the left*/
}
.disable-events {
  color: black
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
        cachedterms:"",
        termsNames:[],
        hover:[],
        btns: {'edit':{'icon':'mdi-pencil', 'text':'Edit'},
               'delete':{'icon':'mdi-trash-can-outline', 'text':'Remove'}
              },
        EDAM_items: EDAM,
        input: null
      }
    },
  methods: {
    addItem(){
      console.log('here'+this.input)
      if(this.input==undefined){
        console.log(this.termsNames.includes(this.cachedterms))
        var item = {
          'label':this.cachedterms, 
          'ClassId':null,
          'weight':'1.00', 
          'isEditing': false
          }
        this.cachedterms=null
      }else{
        item = {
          'label':this.input.PreferredLabel, 
          'ClassId':this.input.ClassId,
          'weight':'1.00', 
          'isEditing':false}
        this.input=null
      }
      this.terms.push(item)
          },
    edit(item){
      for(let i=0; i<this.terms.length;i++){
        if(this.terms[i]['label'] == item['label']){
          this.terms[i]['isEditing'] = !this.terms[i]['isEditing']
          }
      }
      this.isEditing = !this.isEditing
    },
    remove(item){
      console.log(item)
      for(let i=0; i<this.terms.length;i++){
        if(this.terms[i]['label'] == item['label']){
          this.terms.splice(i, 1)
          }
      }
    },
    sampleInput (keywords) {
      this.terms = []
      for(let i=0; i<keywords.length;i++){
        this.terms.push({
          'label':keywords[i]['label'], 
          'weight':keywords[i]['weight'],
          'ClassId':keywords[i]['ClassId'],
          'isEditing':false})
      }
    },
    runDiscoverer(terms){
      this.$emit("click", terms)
    },
    getLabel(item){
      if(item.ClassId.includes('operation')===true){
        return('Operation')
      }else if(item.ClassId.includes('format')===true){
        return('Data Type')
      }else if(item.ClassId.includes('topic')===true){
        return('Topic')
      }else{return('Other')}
    }
  },
  getColor(item){
      if(item.ClassId.includes('operation')===true){
        return('teal')
      }else if(item.ClassId.includes('format')===true){
        return('grey')
      }else if(item.ClassId.includes('topic')===true){
        return('blue')
      }else{return('grey')}
    }
  }
</script>
