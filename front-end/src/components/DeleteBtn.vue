<template>
  <v-badge
  :value="hover"
  color="grey lighten-1"
  content="Delete"
  left
  bottom
  transition="slide-x-transition"
>
  <v-hover v-model="hover">
  <v-btn
      icon
      small
      v-model="id"
      @click="remove(id)"
      class="terms-row-btn"
      >
      <v-icon size="18">mdi-trash-can-outline</v-icon>
    </v-btn>
  </v-hover>
  </v-badge>
</template>

<style scoped>
.terms-row-btn{
  margin-top: 1.5em;
  padding: 0
  }
.terms-row-btn .v-icon{
  margin: 0%;
  padding: 0%
}
</style>

<script>
export default {
  name: 'DeleteBtn',
  props: [],
  data () {
    return{
      hover: false,
    }
  },
  methods:{
    remove(){
      this.$emit("click")
    }
  }
}
</script>
