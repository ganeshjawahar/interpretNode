p=(0.25 0.5 1 2 4)
for i in "${p[@]}"
do
  for j in "${p[@]}"
  do
    ./node2vec -i:pedgelist -o:pemb/paper-$i-$j -p:$i -q:$j -dr
  done
done
