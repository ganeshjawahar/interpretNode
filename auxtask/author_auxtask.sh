folder="data/ibm/it4/undirected_weighted/"
embeddings="eval/author_w/"
#feb23
#features=("clustering_coefficient" "degree" "degree_centrality" "pagerank")
#codes=("1" "1" "1" "1")
#feb24
features=("closeness_centrality" "shortest_path_length")
codes=("1" "2")
for i in 0 1
do
  echo ${features[$i]}

  #deepwalk (1)
  #th model${codes[$i]}.lua -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}deepwalk_emb

  #line (3)
  th model${codes[$i]}.lua -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}wa_vec_1st.txt
  th model${codes[$i]}.lua -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}wa_vec_2nd.txt
  th model${codes[$i]}.lua -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}wa_vec_final.txt

  #node2vec (25)
  grid=(0.25 0.5 1 2 4)
  #for p in "${grid[@]}"
  #do
  #  for q in "${grid[@]}"
  #  do
  #    th model${codes[$i]}.lua  -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}n2v/author-$p-$q
  #  done
  #done
  
  th model${codes[$i]}.lua  -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}n2v/author-1-0.5
  th model${codes[$i]}.lua  -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}n2v/author-1-2

done