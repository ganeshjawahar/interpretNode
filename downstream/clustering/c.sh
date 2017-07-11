edgelist=../../graphs/labels/graph3_labels
base=../../graphs/embeddings/
outputfolder=../../graphs/downstream/clustering/graph3/

embeds=("paper-4-0.25" "paper-4-4" "paper-0.5-2" "paper-0.5-0.5" "paper-2-1" "graph3_dw" "paper-0.25-4" "paper-4-0.5" "paper-0.5-1" "paper-2-2" "paper-0.25-2" "paper-0.25-1" "paper-2-4" "graph3_2nd.txt" "paper-0.25-0.25" "paper-1-1" "paper-4-2" "paper-2-0.25" "paper-0.5-0.25" "paper-1-0.5" "graph3_1st.txt" "paper-1-4" "paper-0.25-0.5" "graph3_all.txt" "paper-4-1" "paper-2-0.5" "paper-1-2" "paper-1-0.25" "paper-0.5-4")


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
