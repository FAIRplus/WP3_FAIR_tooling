<template>
    <td>
        <ul>
            <li v-for="(item) in elementsList" :key="items.indexOf(item)">
            {{ item.label }}
            </li>
            <span v-if="dots">...</span>                      
        </ul>
    </td>
</template>

<script>
export default {
    name: 'EnumCol',
    props : ['items', 'arrowsUp', 'selected', 'idx'],
    data(){
        return {
        }
    },
    computed: {
        elementsList() {
            return this.trimListIfNotSelected(this.items, this.idx)
        },
        dots() {
            if(this.items.length > 5){
                if(this.arrowsUp == false){
                        return  true
                    }
                }
            return false   
        }
    },
    methods: {
        trimListIfNotSelected(list, idx){
            if(this.selected === idx){
                return(list)
            }else{
                var short_list = list.slice(0,5)
                return(short_list)
            }
        }
    }
}
</script>

<style>

</style>