#!/bin/sh

g++ -lm -pthread -Ofast -march=native -Wall -funroll-loops -ffast-math -Wno-unused-result line.cpp -o line -lgsl -lm -lgslcblas
g++ -lm -pthread -Ofast -march=native -Wall -funroll-loops -ffast-math -Wno-unused-result reconstruct.cpp -o reconstruct
g++ -lm -pthread -Ofast -march=native -Wall -funroll-loops -ffast-math -Wno-unused-result normalize.cpp -o normalize
g++ -lm -pthread -Ofast -march=native -Wall -funroll-loops -ffast-math -Wno-unused-result concatenate.cpp -o concatenate

./reconstruct -train ../../../graphs/edgelist/graph2 -output net_dense.txt -depth 2 -k-max 1000
./line -train net_dense.txt -output vec_1st_wo_norm.txt -binary 1 -size 128 -order 1 -negative 5 -threads 40
./line -train net_dense.txt -output vec_2nd_wo_norm.txt -binary 1 -size 128 -order 2 -negative 5 -threads 40
./normalize -input vec_1st_wo_norm.txt -output ../../../graphs/embeddings/graph2_line_1st.txt -binary 1
./normalize -input vec_2nd_wo_norm.txt -output ../../../graphs/embeddings/graph2_line_2nd.txt -binary 1
./concatenate -input1 ../../../graphs/embeddings/graph2_line_1st.txt -input2 ../../../graphs/embeddings/graph2_line_2nd.txt -output ../../../graphs/embeddings/graph2_line_all.txt -binary 1

