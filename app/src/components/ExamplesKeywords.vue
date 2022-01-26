<template>
<div class="container" id="examples-cont">
  <div class="row flex-container" id="row">
    <p><b>Example keyword lists</b></p>
    <div type="button" v-for="item in texts" :key="item.label" class="col-sm-2 flex-item card" @click="sampleInput(item)">
      {{ item.label }}
    </div>
  </div>
  <div class="btn-group-vertical">
      <button type="button" class="input-aid-btn" id="input_clear_button" @click="sampleInput('')">Clear</button>
  </div>
</div>
</template>
<style scoped>
#examples-cont{
  text-align: center;
  

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
.row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap:wrap;
  gap: 10px;
  border-style: solid;
  border-color:lightgrey;
  border-width: 1px;
  margin-top: 1em;
  padding: .5em;
  }

.row > p{
  margin-bottom: .5em;
}

.flex-item {
  flex-grow: 1;
  flex-shrink: 0;
  flex-basis: 45%;
  align-self: center;
  text-align: center;
  min-width: 45%;
  width: 45%;
}

.btn-group-vertical{
  margin-top: 2rem;
}

</style>

<script>
export default {
  name: 'SourceAvatar',
  props: [],
  data() {
    return {
      texts : [
        {'label':'Extract, Transform, Load', 
        'keywords':'Ontology annotation, 1\nsemantic annotation, 0.8\nText mining, 0.5'},
        {'label':'Ontology Annotation',
         'keywords':'Ontology annotation, 1\nsemantic annotation, 0.8\nText mining, 0.5\nText annotation, 0.5\nEntity, 1\nQuery expansion, 0.75'},
        {'label':'Identifier minting',
         'keywords':'k1, 1\nk2, 0.5'}
      ]
    }
  },
  methods: {
    sampleInput(n){
      this.$emit("click", n.keywords)
    }
  }
}
</script>
