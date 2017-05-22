p=(0.25 0.5 1 2 4)
for i in "${p[@]}"
do
  for j in "${p[@]}"
  do
    ./node2vec -i:wa_edgelist -o:waemb/author-$i-$j -p:$i -q:$j -w -dr
  done
done
