p=(0.25 0.5 1 2 4)
for i in "${p[@]}"
do
  for j in "${p[@]}"
  do
    python src/main.py --input edgelist --output emb/author-$i-$j
  done
done