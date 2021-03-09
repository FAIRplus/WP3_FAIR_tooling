import biotools_API_querying as bAq
import pandas as pd 

# parsing zooma results
terms_file='keywords/ETL_EDAM_curated.csv'
ETL_edam_terms, terms_label_ETL, free_terms = bAq.parse_zooma_results(terms_file)

# queries
ETL_edam_results_general, ETL_edam_results_detailed  = bAq.query_for_terms(ETL_edam_terms, True)
ETL_free_results_general, ETL_free_results_detailed  = bAq.query_for_terms(free_terms, False)


# join results
ETL_joint_results = bAq.join_results(ETL_edam_results_detailed, ETL_free_results_detailed)
all_ETL_tools = bAq.merge_tools_lists([ETL_edam_results_general, ETL_free_results_general])

# arrange by term
tools_per_term_ETL = bAq.tools_per_term(ETL_edam_results_general)
tools_per_term_ETL = {terms_label_ETL[term]:tools_per_term_ETL[term] for term in tools_per_term_ETL.keys()}
tools_per_term_free_ETL = bAq.tools_per_term(ETL_free_results_general)
tools_per_term_free_ETL = {term:tools_per_term_free_ETL[term] for term in tools_per_term_free_ETL.keys()}

# ETL related annotations count. Free text and EDAM queries
matches_tools_ETL = bAq.count_matches_edam_free(tools_per_term_ETL, tools_per_term_free_ETL, all_ETL_tools)
ETL_annot_count_df = pd.DataFrame(list(matches_tools_ETL.items()), columns= ['tool','ETL annotations count']).sort_values('ETL annotations count', ascending=False)
#ETL_annot_count_df.to_csv("outputs/20210122_ETL_ranked_by_counts.csv")

# Rank tools using keywords and weight
ETL_ranked = "keywords/ETL_EDAM_ranked.csv"
ranked_keys = bAq.read_ranking(ETL_ranked)

max_matches = max(ETL_annot_count_df['ETL annotations count'])
df_ranked_tools = bAq.rank_tools(all_ETL_tools,ranked_keys, tools_per_term_ETL, tools_per_term_free_ETL, ETL_joint_results, max_matches)
df_ranked_tools.to_csv('outputs/ETL/ranked_tools.csv', index=False)
