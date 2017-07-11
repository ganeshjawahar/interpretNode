edgelist=../../graphs/edgelist/graph3
base=../../graphs/embeddings/
outputfolder=../../graphs/downstream/linkpred/graph3/

embeds=("paper-4-0.25" "paper-4-4" "paper-0.5-2" "paper-0.5-0.5" "paper-2-1" "graph3_dw" "paper-0.25-4" "paper-4-0.5" "paper-0.5-1" "paper-2-2" "paper-0.25-2" "paper-0.25-1" "paper-2-4" "graph3_2nd.txt" "paper-0.25-0.25" "paper-1-1" "paper-4-2" "paper-2-0.25" "paper-0.5-0.25" "paper-1-0.5" "graph3_1st.txt" "paper-1-4" "paper-0.25-0.5" "graph3_all.txt" "paper-4-1" "paper-2-0.5" "paper-1-2" "paper-1-0.25" "paper-0.5-4")

for i in "${embeds[@]}"
do
  echo $i
  timeout 1200s python linkpred.py $edgelist ${base}$i $outputfolder
done
