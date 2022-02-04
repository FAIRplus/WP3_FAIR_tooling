<template>
  <v-badge
  :value="hover"
  color="grey lighten-1"
  content='Edit'
  left
  bottom
  transition="slide-x-transition"
>
  <v-hover v-model="hover">
  <v-btn
      icon
      small
      class="terms-row-btn"
      @click='edit'
      >
      <v-icon size="18">mdi-pencil</v-icon>
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
  name: 'EditBtn',
  props: ['isEditing'],
  data () {
    return{
      hover: false,
    }
  },
  methods:{
    edit(){
      this.$emit("click", !this.isEditing)
    }
  }
}
</script>
