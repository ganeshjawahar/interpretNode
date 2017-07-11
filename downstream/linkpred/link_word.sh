edgelist=../../graphs/edgelist/graph4
base=../../graphs/embeddings/
outputfolder=../../graphs/downstream/linkpred/graph4/


embeds=("word-4-4" "word-4-0.25" "word-2-0.25" "word-4-0.5" "word-1-1" "word-0.25-4" "word-0.5-1" "word-2-0.5" "graph6_2nd.txt" "graph6_all.txt" "word-4-2" "word-4-1" "word-2-4" "word-2-2" "word-0.25-2" "graph6_1st.txt" "word-0.5-0.25" "word-0.25-1" "word-0.5-4" "word-0.5-2" "graph6_dw" "word-1-4" "word-2-1" "word-1-0.25" "word-1-2" "word-0.5-0.5" "word-0.25-0.25" "word-1-0.5" "word-0.25-0.5" )

for i in "${embeds[@]}"
do
  echo $i
  timeout 1200s python linkpred.py $edgelist ${base}$i $outputfolder
done
