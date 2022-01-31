<template>
  <div>
    <img src='@/assets/img/error.png'>
    {{ error_text }}
  </div>
</template>

<style scoped>
div{
  width: 50%;
  margin-left: auto;
  margin-right: auto;
}

div img{
  width: 50px;
}
</style>

<script>
export default {
  name: 'Dummy',
  props: ['error_text']
}
</script>
