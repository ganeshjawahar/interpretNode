folder="data/ibm/it5/graph4/"
embeddings="eval/word/"
features=("average_neighbor_degree" "betweenness_centrality" "closeness_centrality" "clustering_coefficient" "count_community" "degree" "degree_centrality" "edge_weight" "is_1st_degree" "is_2nd_degree" "is_from_same_community" "load_centrality" "pagerank" "preferential_attachment" "shortest_path_length" "jaccard_coefficient_dict")
codes=("1" "1" "1" "1" "1" "1" "1" "2" "2" "2" "2" "1" "1" "2" "2" "2")
for i in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
do
  echo ${features[$i]}

  #deepwalk (1)
  th model${codes[$i]}.lua -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}wordembeddings

  #line (3)
  th model${codes[$i]}.lua -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}word_vec_1st.txt
  th model${codes[$i]}.lua -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}word_vec_2nd.txt
  th model${codes[$i]}.lua -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}word_vec_final.txt
  
  th model${codes[$i]}.lua  -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}n2v/word-1-0.5
  th model${codes[$i]}.lua  -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}n2v/word-1-2
done