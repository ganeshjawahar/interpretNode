folder="data/ibm/it4/directed_unweighted/"
embeddings="eval/paper/"
#feb23
#features=("indegree" "outdegree" "degree_centrality" "pagerank")
#codes=("1" "1" "1" "1")
#deb24
features=("direction")
codes=("2")
for i in 0
do
  echo ${features[$i]}

  #deepwalk (1)
  th model${codes[$i]}.lua -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}deepwalk_emb

  #line (3)
  th model${codes[$i]}.lua -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}p_vec_1st.txt
  th model${codes[$i]}.lua -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}p_vec_2nd.txt
  th model${codes[$i]}.lua -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}p_vec_final.txt

  #node2vec (25)
  grid=(0.25 0.5 1 2 4)
  #for p in "${grid[@]}"
  #do
  #  for q in "${grid[@]}"
  #  do
  #    th model${codes[$i]}.lua  -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}n2v/author-$p-$q
  #  done
  #done
  
  th model${codes[$i]}.lua  -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}n2v/paper-1-0.5
  th model${codes[$i]}.lua  -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}n2v/paper-1-2

done