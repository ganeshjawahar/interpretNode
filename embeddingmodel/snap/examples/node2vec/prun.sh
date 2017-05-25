: '
a1=(0.25 0.5 0.5 1 2 4 1 2 4 4)  
a2=(0.25 0.25 0.5 0.25 0.5 0.25 2 1 0.25 2)

for idx in "${!a1[@]}";
do
	i=${a1[$idx]} 
	j=${a2[$idx]} 
	./node2vec -i:/home/ayushidalmia/interpretNode/graphs/edgelist/graph3 -o:/home/ayushidalmia/interpretNode/graphs/embeddings/paper-$i-$j -p:$i -q:$j -dr	
done
'

p=(0.25 0.5 1 2 4)
for i in "${p[@]}"
do
  for j in "${p[@]}"
  do
    ./node2vec -i:/home/ayushidalmia/interpretNode/graphs/edgelist/graph3 -o:/home/ayushidalmia/interpretNode/graphs/embeddings/paper-$i-$j -p:$i -q:$j -dr
  done
done

