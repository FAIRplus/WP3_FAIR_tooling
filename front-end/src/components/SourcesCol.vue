<template>
    <td>
        <SourceAvatar 
            v-for="source in avatars"
            :key="source.content" 
            :avatarProps="source"
            :sources_labels="itemSources" />
    </td>
</template>

<script>
import SourceAvatar from './SourceAvatar.vue'

export default {
    name: 'SourcesCol',
    props: ['itemSources'],
    components : {
        SourceAvatar
    },
    data(){
        return {
            avatars: {
                biotools: {
                    src:'elixir-logo.svg',
                    color:'orange',
                    content:'bio.tools',
                    url:'bio.tools',
                    label: 'biotools',
                },
                bioconda: {
                    src:'bioconda-logo.svg',
                    color:'#005500',
                    content:'bioconda',
                    url:'',
                    label:'bioconda'
                },
                github: {
                    src:'github-logo.svg',
                    color:'black',
                    content:'GitHub',
                    url:'github.org',
                    label:'github'
                },
                bioconductor: {
                    src:'bioconductor-logo.svg',
                    color:'#2f93ba',
                    content:'Bioconductor',
                    url:'',
                    label:'bioconductor'
                },
                galaxy: {
                    src: 'galaxy-logo.svg',
                    color: '#134798',
                    content: 'Galaxy Eu',
                    url:'',
                    label: 'galaxy'
                },
                sourceforge: {
                    src: 'sourceforge-logo.svg',
                    color: '#ff6602',
                    content: 'SourceForge',
                    url:'',
                    label: 'sourceforge'
                },
                bitbucket: {
                    src: 'bitbucket-logo.svg',
                    color: '#005ed9',
                    content: 'Bitbucket',
                    url:'',
                    label: 'bitbucket'
                },
                other: {
                    src: 'other.svg',
                    color: '#535682',
                    content: 'Homepage',
                    url:'',
                    label: 'other'
                }
            }
        }
    }
}
</script>

<style>

</style>