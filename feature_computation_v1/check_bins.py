graph_file = "graph4"

baseDir="/home/ayushidalmia/interpretNode/graphs/features/"+graph_file+"/"
outDir = "/home/ayushidalmia/interpretNode/logs/binning/"
from collections import defaultdict

features = ["isFromSameCommunity","is1stDegree","is2ndDegree","countCommunity","edgeWeight"]
for feature in features:
	input_files = []
	input_files.append(feature+"_dev")
	input_files.append(feature+"_train")
	input_files.append(feature+"_test")

	dict_class = defaultdict(int)
	for files in input_files:
		f=open(baseDir+files)
		for line in f:
			temp = line.strip().split("\t")
			if len(temp)==2:
				dict_class[int(temp[1])]+=1
			elif len(temp)==3:
				dict_class[int(temp[2])]+=1
		f.close()

	f=open(outDir+graph_file+"_"+feature,"w")
	for keys in sorted(dict_class.keys()):
		f.write(str(keys)+"\t"+str(dict_class[keys])+"\n")
	f.close()



features = ["clustering_coefficient.txt","load_centrality.txt","shortest_path_length.txt","average_neighbor_degree.txt","betweenness_centrality.txt","closeness_centrality.txt","degree_centrality.txt"]
for feature in features:
        input_files = ["train_"+feature,"test_"+feature, "dev_"+feature]

        dict_class = defaultdict(int)
        for files in input_files:
                f=open(baseDir+files)
                for line in f:
                        temp = line.strip().split("\t")
                        if len(temp)==2:
                                dict_class[int(temp[1])]+=1
                        elif len(temp)==3:
                                dict_class[int(temp[2])]+=1
                f.close()

        f=open(outDir+graph_file+"_"+feature,"w")
        for keys in sorted(dict_class.keys()):
                f.write(str(keys)+"\t"+str(dict_class[keys])+"\n")
        f.close()


