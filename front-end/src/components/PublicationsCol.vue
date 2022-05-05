<template>
    <td>
        <ul>
            <div v-for="(pdata, idx) in build_pubs(item)" :key="idx" class='publications'>
                <v-icon class='fas fa-circle' :color = 'pdata.color' size="10"></v-icon> 
                <span v-html="pdata['label']" />
                <a v-for="(link, idx) in pdata['links']" :key="idx"  :href="link" target="_blank">  
                    <i class='fas fa-external-link-alt' size="3"></i>
                </a>
            </div>
        </ul>
    </td> 
</template>

<script>
export default {
    name: 'PublicationsCol',
    props: ['item', 'idx'],
    data() {
        return {
            linksURLs: [
                {id : 'doi',  template : 'https://doi.org/'},
                {id : 'pmcid', template : 'https://www.ncbi.nlm.nih.gov/pmc/articles/'},
                {id : 'pmid', template :'https://pubmed.ncbi.nlm.nih.gov/'},
                {id : 'url', template: ''}
                ],
                plot_colors: [
            '#1f77b4',
            '#ff7f0e',
            '#2ca02c',
            '#d62728',
            '#9467bd',
            '#8c564b',
            '#e377c2',
            '#7f7f7f',
            '#bcbd22',
            '#17becf' 
            ],
            labels:''
        }
    },
 
    methods: {
        build_pubs(item){
            var labels = []
            for (let i = 0; i < item.citations.length; i++) {
                var links = []
                var linkFound = 0
                for(var k = 0; k < this.linksURLs.length; k++){
                    while(linkFound < 1){
                        const idType = this.linksURLs[k]['id']
                        if(item.citations[i][idType]!=undefined){
                            links.push(this.linksURLs[k]['template']+item.citations[i][idType])
                            linkFound ++
                            console.log('hey')
                            console.log(i)
                            console.log(linkFound)
                            }
                    }
                }
                var label = ''
                if(item.citations[i]['year'] == undefined){
                    if(item.citations[i]['title'] == undefined){
                        label = 'link'
                    }else{
                        label = item.citations[i]['title']
                    }
                }else{
                    label = `<span>${item.citations[i]['title']}(${item.citations[i]['year']})</span>`
                }
                labels.push({'label':label, 
                            'color':this.plot_colors[i],
                            'year':item.citations[i]['year'],
                            'links':links})
            }
            for (let e = 0; e < item.citations_other.length; e++) {
                links = []
                linkFound = 0
                for(var j = 0; j < this.linksURLs.length; j++){
                    while(linkFound < 1){
                        const idType = this.linksURLs[j]['id']
                        if(item.citations_other[e][idType]!=undefined){
                            links.push(this.linksURLs[j]['template']+item.citations_other[e][idType])
                            linkFound ++
                        }
                    }
                }
                label = ''
                if(item.citations_other[e]['title'] != '' && item.citations_other[e]['title'] != undefined){
                    labels.push({'label': item.citations_other[e]['title'],
                                'color': 'black',
                                'year': null,
                                'links': links})
                }
            }
            console.log(labels)
            return(labels)
        }
    }
}
</script>

<style>
.publications >>> .fas{
  padding-right: .15em;
  padding-left: .15em;
  padding-bottom: .4em;
}
</style>