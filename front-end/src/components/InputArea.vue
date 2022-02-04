<template>
  <v-container fluid>
    <v-row>
      <v-col cols="7">
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
          item-text="label"
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
          <v-col cols="10">
          </v-col>
          <v-col cols="2">
            <v-btn
              color="success"
              dark
            >
            <small> RUN <br> SEARCH</small><v-icon>mdi-rocket-launch</v-icon>
            </v-btn>
          </v-col>
        </v-row>       
        </v-card-text>
      </v-card>
    </v-row>
  </v-container>
</template>
<style scoped>
.v-card{
  margin-top: 0%;
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

</style>

<script>
import EditBtn from './EditBtn.vue'
import DeleteBtn from './DeleteBtn.vue'
export default {
  name: 'InputArea',
  components: { 
    EditBtn,
    DeleteBtn
    },
  props: [],
  data () {
      return {
        terms: [],
        isEditing: false,
        hover:[],
        btns: {'edit':{'icon':'mdi-pencil', 'text':'Edit'},
               'delete':{'icon':'mdi-trash-can-outline', 'text':'Remove'}
              },
        EDAM_items:[
          {
            'uri':'http://edamontology.org/topic_0150',
            'label':'Protein design',
            'type':'topic'
          },
          {
            'uri':'http://edamontology.org/operation_3960', 
            'label':'Principal Component Analysis',
            'type':'operation'},
          {
            'uri':'http://edamontology.org/operation_3962', 
            'label':'Deletion detection',
            'type':'operation'},
          {
            'uri':'http://edamontology.org/topic_011',
            'label':'Gen Structure',
            'type':'topic'}]
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
    },
    edit(){
      this.isEditing = !this.isEditing
    },
    remove(){
      this.terms.pop(this.item)
    }
  }
}
</script>
