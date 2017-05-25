p=(0.25 0.5 1 2 4)
for i in "${p[@]}"
do
  for j in "${p[@]}"
  do
    ./node2vec -i:/home/ayushidalmia/interpretNode/graphs/edgelist/graph4 -o:/home/ayushidalmia/interpretNode/graphs/embeddings/word-$i-$j -p:$i -q:$j 
  done
done
