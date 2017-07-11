folder="/home/ayushidalmia/interpretNode/graphs/features/graph4/"
embeddings="/home/ayushidalmia/interpretNode/graphs/embeddings/"

features=("countCommunity" "degree_centrality" "degree")
codes=("1" "1" "1")

for i in 0 1 2
do
  echo ${features[$i]}

  #deepwalk (1)
  th model${codes[$i]}.lua -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}graph6_dw
  #line (3)
  th model${codes[$i]}.lua -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}graph6_1st.txt
  th model${codes[$i]}.lua -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}graph6_2nd.txt
  th model${codes[$i]}.lua -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}graph6_all.txt
  p=(0.25 0.5 1 2 4)
  for j in "${p[@]}"
  do
   for k in "${p[@]}"
    do  
      th model${codes[$i]}.lua  -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}word-$j-$k
    done

   done

      #th model${codes[$i]}.lua  -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}word-1-2
done
