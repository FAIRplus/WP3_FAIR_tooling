import biotools_API_querying as bAq
import pandas as pd 

topics = ["ontology_annotation", "ontology_management","ontology_engineering","ontology_mapping"]

for topic in topics:
	print(topic+"/n/n")
	# parsing zooma results
	terms_file='keywords/'+topic+'_EDAM_curated.csv'
	ontology_edam_terms, terms_label_ontology, free_terms = bAq.parse_zooma_results(terms_file)

	# queries
	ontology_edam_results_general, ontology_edam_results_detailed  = bAq.query_for_terms(ontology_edam_terms, True)
	ontology_free_results_general, ontology_free_results_detailed  = bAq.query_for_terms(free_terms, False)


	# join results
	ontology_joint_results = bAq.join_results(ontology_edam_results_detailed, ontology_free_results_detailed)
	all_ontology_tools = bAq.merge_tools_lists([ontology_edam_results_general, ontology_free_results_general])

	# arrange by term
	tools_per_term_ontology = bAq.tools_per_term(ontology_edam_results_general)
	tools_per_term_ontology = {terms_label_ontology[term]:tools_per_term_ontology[term] for term in tools_per_term_ontology.keys()}
	tools_per_term_free_ontology = bAq.tools_per_term(ontology_free_results_general)
	tools_per_term_free_ontology = {term:tools_per_term_free_ontology[term] for term in tools_per_term_free_ontology.keys()}

	# ontology related annotations count. Free text and EDAM queries
	matches_tools_ontology = bAq.count_matches_edam_free(tools_per_term_ontology, tools_per_term_free_ontology, all_ontology_tools)
	ontology_annot_count_df = pd.DataFrame(list(matches_tools_ontology.items()), columns= ['tool',topic+'_count']).sort_values(topic+'_count', ascending=False)
	#ontology_annot_count_df.to_csv("outputs/20210122_ontology_ranked_by_counts.csv")

	# Rank tools using keywords and weight
	ontology_ranked = "keywords/"+topic+"_EDAM_ranked.csv"
	ranked_keys = bAq.read_ranking(ontology_ranked)

	max_matches = max(ontology_annot_count_df[topic+'_count'])
	df_ranked_tools = bAq.rank_tools(all_ontology_tools,ranked_keys, tools_per_term_ontology, tools_per_term_free_ontology, ontology_joint_results, max_matches)
	df_ranked_tools.to_csv('outputs/ontology/'+topic+'_ranked_tools.csv', index=False)
