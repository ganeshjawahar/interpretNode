import random

baseDir="/home/ayushidalmia/interpretNode/graphs/features/graph3/"
features=["average_neighbor_degree","closeness_centrality","degree_centrality","degree","direction","indegree","is1stDegree","is2ndDegree","sameCommunity","outdegree","pagerank"]
#features=["average_neighbor_degree","clustering_coefficient","countCommunity","degree_centrality","degree","edgeWeight","is1stDegree","is2ndDegree","sameCommunity","pagerank"]


for feature in features:
	filenames = "test_"+feature+".txt"
	f=open(baseDir+filenames)
	lines = []
	for line  in f:
		lines.append(line.strip())
	f.close()

	random.shuffle(lines)
	number_of_samples = min(len(lines),10000)
	new_lines = lines[:number_of_samples]
	
	filenames = "test_"+feature+"_small.txt"
	f=open(baseDir+filenames,"w")
	f.write("\n".join(new_lines))
	f.close()		
	
	
	filenames = "dev_"+feature+".txt"
        f=open(baseDir+filenames)
        lines = []
        for line  in f:
                lines.append(line.strip())

	f.close()

        random.shuffle(lines)
        number_of_samples = min(len(lines),20000)
        new_lines = lines[:number_of_samples]

        filenames = "dev_"+feature+"_small.txt"
        f=open(baseDir+filenames,"w")
        f.write("\n".join(new_lines))
        f.close()

        filenames = "train_"+feature+".txt"
        f=open(baseDir+filenames)
        lines = []
        for line  in f:
                lines.append(line.strip())        

	f.close()

        random.shuffle(lines)
        number_of_samples = min(len(lines),70000)
        new_lines = lines[:number_of_samples]

        filenames = "train_"+feature+"_small.txt"
        f=open(baseDir+filenames,"w")
        f.write("\n".join(new_lines))
        f.close()
