#!/bin/sh

g++ -lm -pthread -Ofast -march=native -Wall -funroll-loops -ffast-math -Wno-unused-result line.cpp -o line -lgsl -lm -lgslcblas
g++ -lm -pthread -Ofast -march=native -Wall -funroll-loops -ffast-math -Wno-unused-result reconstruct.cpp -o reconstruct
g++ -lm -pthread -Ofast -march=native -Wall -funroll-loops -ffast-math -Wno-unused-result normalize.cpp -o normalize
g++ -lm -pthread -Ofast -march=native -Wall -funroll-loops -ffast-math -Wno-unused-result concatenate.cpp -o concatenate

./reconstruct -train ../../../graphs/edgelist/graph3 -output ../../../graphs/edgelist/graph3_net_dense.txt -depth 3 -k-max 10000
./line -train ../../../graphs/edgelist/graph3_net_dense.txt -output ../../../graphs/edgelist/graph3_vec_1st_wo_norm.txt -binary 1 -size 128 -order 1 -negative 5 -samples 10000 -threads 40
./line -train ../../../graphs/edgelist/graph3_net_dense.txt -output ../../../graphs/edgelist/graph3_vec_2nd_wo_norm.txt -binary 1 -size 128 -order 2 -negative 5 -samples 10000 -threads 40
./normalize -input ../../../graphs/edgelist/graph3_vec_1st_wo_norm.txt -output ../../../graphs/edgelist/graph3_1st.txt
./normalize -input ../../../graphs/edgelist/graph3_vec_2nd_wo_norm.txt -output ../../../graphs/edgelist/graph3_2nd.txt
python concatenate.py ../../../graphs/edgelist/graph3_1st.txt ../../../graphs/edgelist/graph3_2nd.txt ../../../graphs/edgelist/graph3_all.txt
