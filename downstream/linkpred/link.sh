#edgelist=../../input/graph4
#base=../../eval/word/
#embeds=("wordembeddings" "word_vec_1st.txt" "word_vec_2nd.txt" "word_vec_final.txt" "n2v/word-1-0.5" "n2v/word-1-2")
#for i in 0 1 2 3 4 5
#do
# python linkpred.py $edgelist ${base}${embeds[$i]}
#done 

edgelist=../../input/graph3
base=../../eval/paper/
embeds=("deepwalk_emb" "p_vec_1st.txt" "p_vec_2nd.txt" "p_vec_final.txt" "n2v/paper-1-0.5" "n2v/paper-1-2")
for i in 0 1 2 3 4 5
do
  python linkpred.py $edgelist ${base}${embeds[$i]}
done

#edgelist=../../input/graph1
#base=../../eval/author_w/
#embeds=("deepwalk_emb" "wa_vec_1st.txt" "wa_vec_2nd.txt" "wa_vec_final.txt" "n2v/author-1-0.5" "n2v/author-1-2")
#for i in 0 1 2 3 4 5
#do
#  python linkpred.py $edgelist ${base}${embeds[$i]}
#done 