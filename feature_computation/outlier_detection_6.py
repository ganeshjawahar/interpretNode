k=10

baseDir = "/home/ayushidalmia/interpretNode/graphs/" 
wordembeddingsfolder = "embeddings/"
graph = "edgelist/graph4"
outputfilefolder = "outlierscore/graph4/"

from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import euclidean_distances
import os
import numpy
import networkx as nx

neigh = NearestNeighbors(n_neighbors=k)
id_to_embedding = {}
embedding_to_id = {}

def k_distance(n):
	neighbors = neigh.kneighbors(X=id_to_embedding[n].reshape(1,-1), n_neighbors=k, return_distance=True)
	return neighbors[0][0][-1]

def reachability_distance(a,b):
	distance  = euclidean_distances(id_to_embedding[a].reshape(1,-1),id_to_embedding[b].reshape(1,-1))[0][0]
	return max(k_distance(b),distance)

def compute_local_reachibility_distance(n,neighbors):
	local_reachibility_distance = 0
	for i in neighbors:
		local_reachibility_distance += reachability_distance(n,i)
	local_reachibility_distance = float(len(neighbors))/local_reachibility_distance
	return local_reachibility_distance


def main():
	filenames = ["graph6_1st.txt","graph6_2nd.txt","graph6_all.txt"]
	p=[0.25,0.5,1,2,4]
	for i in p:
		for j in p:
			filenames.append("word-"+str(i)+"-"+str(j))
	print filenames

	for filename in filenames:
		print filename
		X = []
		f = open(os.path.join(baseDir,wordembeddingsfolder,filename))
		f.readline()
		for line in f:
			temp = line.strip().split(" ")
			embedding_to_id[" ".join(temp[1:])] = temp[0]
			id_to_embedding[temp[0]] = numpy.array(temp[1:])
			X.append(temp[1:])
		X = numpy.array(X)
		neigh.fit(X)

		count = 0
		G = nx.read_weighted_edgelist(os.path.join(baseDir,graph))
		nodes = G.nodes()
		local_reachibility_distance = {}
		for n in nodes:
			count+=1
			neighbors = G.neighbors(n)
			local_reachibility_distance[n] = compute_local_reachibility_distance(n,neighbors)
		

		print "local_reachibility_distance computed. computing LOF..."
		count = 0
		local_outlier_factor = {}
		for n in local_reachibility_distance:
			count+=1
			neighbors = G.neighbors(n)
			sum_of_lrd = 0
			for i in neighbors:
				sum_of_lrd += local_reachibility_distance[i]
			sum_of_lrd = sum_of_lrd/float(len(neighbors))
			local_outlier_factor[n] = sum_of_lrd/local_reachibility_distance[n]
		
		import operator
		sorted_local_outlier_factor = sorted(local_outlier_factor.items(), key=operator.itemgetter(1), reverse=True)
		outputfilename = filename+"_outlier.txt"
		f=open(os.path.join(baseDir,outputfilefolder,outputfilename),"w")
		for key in sorted_local_outlier_factor:
			f.write(str(key[0])+'\t'+str(key[1])+"\n")
		f.close()

if __name__ == '__main__':
	main()
