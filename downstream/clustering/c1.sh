edgelist=../../graphs/labels/graph1_labels
base=../../graphs/embeddings/
outputfolder=../../graphs/downstream/clustering/graph1/

embeds=("author-1-0.25" "author-4-0.5" "author-4-2" "author-1-2" "author-2-2" "author-4-1" "graph5_1st.txt" "graph5_all.txt" "author-1-1" "author-2-0.5" "graph5_dw" "author-0.5-0.5" "author-1-0.5" "author-2-1" "author-4-0.25" "author-4-4" "author-1-4" "author-0.25-0.25" "author-0.25-1" "author-0.5-2" "author-0.25-2" "author-0.5-4" "author-2-0.25" "author-0.5-1" "author-0.25-4" "author-2-4" "author-0.5-0.25" "graph5_2nd.txt" "author-0.25-0.5")

for i in "${embeds[@]}"
do
  python cluster.py $edgelist ${base}$i $outputfolder
done

: '
edgelist=../../graphs/edgelist/graph1_labels
base=../../graphs/embeddings/
outputfolder=../../graphs/downstream/graph1/
embeds=("deepwalk_emb" "wa_vec_1st.txt" "wa_vec_2nd.txt" "wa_vec_final.txt" "n2v/author-1-0.5" "n2v/author-1-2")
for i in 0 1 2 3 4 5
do
  python cluster.py $edgelist ${base}${embeds[$i]} $outputfolder
done
' 
