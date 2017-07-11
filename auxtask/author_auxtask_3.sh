folder="/home/ayushidalmia/interpretNode/graphs/features/graph1/"
embeddings="/home/ayushidalmia/interpretNode/graphs/embeddings/"

features=("edgeWeight_small" "is1stDegree_small" "is2ndDegree_small")
codes=("2" "2" "2")

for i in 0 1 2
do
  echo ${features[$i]}

  #deepwalk (1)
  th model${codes[$i]}.lua -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}graph5_dw
  #line (3)
  th model${codes[$i]}.lua -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}graph5_1st.txt
  th model${codes[$i]}.lua -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}graph5_2nd.txt
  th model${codes[$i]}.lua -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}graph5_all.txt
  p=(0.25 0.5 1 2 4)
  for j in "${p[@]}"
  do
   for k in "${p[@]}"
    do  
      th model${codes[$i]}.lua  -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}author-$j-$k
    done

   done

      #th model${codes[$i]}.lua  -train ${folder}train_${features[$i]}.txt -dev ${folder}dev_${features[$i]}.txt -test ${folder}test_${features[$i]}.txt -rep ${embeddings}word-1-2
done
