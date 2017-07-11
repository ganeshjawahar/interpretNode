edgelist=../../graphs/labels/graph3_labels
base=../../graphs/embeddings/
outputfolder=../../graphs/downstream/classification/graph3/

embeds=("paper-4-0.25" "paper-4-4" "paper-0.5-2" "paper-0.5-0.5" "paper-2-1" "graph3_dw" "paper-0.25-4" "paper-4-0.5" "paper-0.5-1" "paper-2-2" "paper-0.25-2" "paper-0.25-1" "paper-2-4" "graph3_2nd.txt" "paper-0.25-0.25" "paper-1-1" "paper-4-2" "paper-2-0.25" "paper-0.5-0.25" "paper-1-0.5" "graph3_1st.txt" "paper-1-4" "paper-0.25-0.5" "graph3_all.txt" "paper-4-1" "paper-2-0.5" "paper-1-2" "paper-1-0.25" "paper-0.5-4")
#embeds=("author-4-0.25" "author-4-4" "author-0.5-2" "author-0.5-0.5" "author-2-1" "graph5_dw" "author-0.25-4" "author-4-0.5" "author-0.5-1" "author-2-2" "author-0.25-2" "author-0.25-1" "author-2-4" "graph5_2nd.txt" "author-0.25-0.25" "author-1-1" "author-4-2" "author-2-0.25" "author-0.5-0.25" "author-1-0.5" "graph5_1st.txt" "author-1-4" "author-0.25-0.5" "graph5_all.txt" "author-4-1" "author-2-0.5" "author-1-2" "author-1-0.25" "author-0.5-4")
#embeds=("word-4-0.25" "word-4-4" "word-0.5-2" "word-0.5-0.6" "word-2-1" "graph6_dw" "word-0.25-4" "word-4-0.5" "word-0.5-1" "word-2-2" "word-0.25-2" "word-0.25-1" "word-2-4" "graph6_2nd.txt" "word-0.25-0.25" "word-1-1" "word-4-2" "word-2-0.25" "word-0.5-0.25" "word-1-0.5" "graph6_1st.txt" "word-1-4" "word-0.25-0.5" "graph6_all.txt" "word-4-1" "word-2-0.5" "word-1-2" "word-1-0.25" "word-0.5-4")

#embeds=("graph3_1st.txt")
for i in "${embeds[@]}"
do
 echo $i
 timeout 1500s python classify.py $edgelist ${base}$i $outputfolder
done 

#edgelist=../../input/graph3_labels
#base=../../eval/paper/
#embeds=("deepwalk_emb" "p_vec_1st.txt" "p_vec_2nd.txt" "p_vec_final.txt" "n2v/paper-1-0.5" "n2v/paper-1-2")
#for i in 0 1 2 3 4 5
#do
 # python scoring.py $edgelist ${base}${embeds[$i]}
#done

#edgelist=../../input/graph1_labels
#base=../../eval/author_w/
#embeds=("deepwalk_emb" "wa_vec_1st.txt" "wa_vec_2nd.txt" "wa_vec_final.txt" "n2v/author-1-0.5" "n2v/author-1-2")
#for i in 0 1 2 3 4 5
#do
#  python scoring.py $edgelist ${base}${embeds[$i]}
#done 
