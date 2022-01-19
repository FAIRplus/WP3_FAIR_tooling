<template>
<v-tooltip bottom>
      <template v-slot:activator="{ on, attrs }">
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
  props: ['avatarProps'],
  data() {
    return {
      hover: false
    }
  }
}
</script>
