<template>
    <td>
        <i  v-if="down" class="fas fa-angle-down cell-arrow"></i>
        <i  v-if="up" class="fas fa-angle-up cell-arrow"></i>
    </td>
</template>

<script>
export default {
    name:'ArrowsCol',
    props: ['up', 'down']
}
</script>

<style>
.cell-arrow{
  color: darkgray;
}
</style>