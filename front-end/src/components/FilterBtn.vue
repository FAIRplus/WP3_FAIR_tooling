<template>
<v-btn> 
    <span class="filter">{{ label }}</span>
        <v-img
            v-if="icon"
            :src="require(`@/assets/img/${label}-logo-black.svg`)"
            max-width='30'
        ></v-img>
    </v-btn>
</template>
<script>

export default {
    name: 'FilterBtn',
    props: {
        label: String,
        icon: Boolean
        }
    }

</script>

<style>
.filter {
    font-size: .7rem;
}
</style>