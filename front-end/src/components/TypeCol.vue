<template>
  <td>
      {{ dictGet(type).hover }}
  </td>
</template>

<script>
export default {
    name: 'TypeCol',
    props: ['type'],
    data() {
        return {
            typesAbb: {
                'cmd' : {
                'text': 'CMD',
                'hover': 'Command-line Tool'
                },
                'web': {
                'text': 'Web',
                'hover': 'Web Application'
                },
                'db' : {
                'text': 'DB',
                'hover': 'Database'
                },
                'lib' : {
                'text': 'Lib',
                'hover': 'Library'
                },
                'unknown': {
                'text': 'Unknown',
                'hover': 'Unknown'
                }
            }
        }
    },
    methods: {
        dictGet(key) {
            var result = this.typesAbb[key] || {'text':key, "hover":key}
            return(result)
        },
    }
}
</script>

<style>

</style>