library(reshape2)
library(ggplot2)
tools=read.csv('~/Downloads/Ontology Mapping - Aggregated Tool List.tsv',sep='\t')

#ggplot(tools,aes(Tools,Score,fill=Curation))+geom_bar(stat='identity')+facet_grid(~Category)+coord_flip()+scale_fill_manual(values = c("#7171C6", "#71C671"))
#ggplot(tools,aes(Tools,Score,fill=Curation,color=Licensing))+geom_bar(stat='identity',size=0.5,aes(linetype=Licensing))+facet_grid(~Category)+coord_flip()+scale_fill_manual(values = c("#7171C6", "#71C671"))+scale_color_manual(values = c("black","gray25") )

ggplot(tools,aes(Tools,Score,fill=Curation))+geom_bar(stat='identity',size=0.5)+facet_grid(Licensing~Category,scales="free")+coord_flip()+scale_fill_manual(values = c("#7171C6", "#71C671"))