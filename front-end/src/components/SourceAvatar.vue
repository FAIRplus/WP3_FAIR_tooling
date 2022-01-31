<template>
    <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }" v-if="active"> 
          <a v-bind:href=link target='_blank'>     
          <v-avatar
            v-bind="attrs"
            v-on="on"
            v-bind:color="avatarProps.color"
            size="20"
            class="avatar-source"
            align="center"
            >
            <v-img :src="require(`@/assets/img/${avatarProps.src}`)"></v-img>
          </v-avatar>
          </a>
        </template>
        <span>{{ avatarProps.content }}</span>
      </v-tooltip>
</template>

<style scoped>
.avatar-source{
  margin-top: 0.4em;
  margin-right: 0.2em;
}
</style>

<script>
export default {
  name: 'SourceAvatar',
  props: ['avatarProps', 'sources_labels'],
  data() {
    return {
      hover: false,
      active: false,
      lab: [],
      link:false
    }
  },
  mounted() {
    this.active = this.active_avatar()
    this.link = this.build_link()
  },
  methods: {
    active_avatar(){
      if((this.avatarProps.label in this.sources_labels) === true){
        this.lab.push(this.avatarProps.label in this.sources_labels)
        return(true)
      }
    },
    build_link(){
      var source = this.avatarProps.label
      return(this.sources_labels[source])
    }
  }
}
</script>
