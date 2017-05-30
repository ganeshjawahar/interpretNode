import networkx as nx
from utils import *
import sys

def function(input):
	'''
	clustering_coefficient = nx.clustering(G)
	clustering_coefficient = normalise(clustering_coefficient)
	train_keys, dev_keys, test_keys = create_train_test_dev_split(clustering_coefficient.keys())
	train_data, dev_data, test_data = write_train_test_dev(clustering_coefficient,train_keys,dev_keys,test_keys)
	write_to_file(train_data,baseDir+"train_clustering_coefficient.txt")
	write_to_file(dev_data,baseDir+"dev_clustering_coefficient.txt")
	write_to_file(test_data,baseDir+"test_clustering_coefficient.txt")
	'''
	if input==2:
		betweenness_centrality = nx.betweenness_centrality(G,normalized=True)
		betweenness_centrality = normalise(betweenness_centrality)
		train_keys, dev_keys, test_keys = create_train_test_dev_split(betweenness_centrality.keys())
		train_data, dev_data, test_data = write_train_test_dev(betweenness_centrality,train_keys,dev_keys,test_keys)
		write_to_file(train_data,baseDir+"train_betweenness_centrality.txt")
		write_to_file(dev_data,baseDir+"dev_betweenness_centrality.txt")
		write_to_file(test_data,baseDir+"test_betweenness_centrality.txt")

	if input==3:
		closeness_centrality = nx.closeness_centrality(G,normalized=True)
		closeness_centrality = normalise(closeness_centrality)
		train_keys, dev_keys, test_keys = create_train_test_dev_split(closeness_centrality.keys())
		train_data, dev_data, test_data = write_train_test_dev(closeness_centrality,train_keys,dev_keys,test_keys)
		write_to_file(train_data,baseDir+"train_closeness_centrality.txt")
		write_to_file(dev_data,baseDir+"dev_closeness_centrality.txt")
		write_to_file(test_data,baseDir+"test_closeness_centrality.txt")

	if input==4:
		average_neighbor_degree = nx.average_neighbor_degree(G)
		average_neighbor_degree = normalise(average_neighbor_degree)
		train_keys, dev_keys, test_keys = create_train_test_dev_split(average_neighbor_degree.keys())
		train_data, dev_data, test_data = write_train_test_dev(average_neighbor_degree,train_keys,dev_keys,test_keys)
		write_to_file(train_data,baseDir+"train_average_neighbor_degree.txt")
		write_to_file(dev_data,baseDir+"dev_average_neighbor_degree.txt")
		write_to_file(test_data,baseDir+"test_average_neighbor_degree.txt")

	if input==5:
		degree_centrality = nx.degree_centrality(G)
		degree_centrality = normalise(degree_centrality)
		train_keys, dev_keys, test_keys = create_train_test_dev_split(degree_centrality.keys())
		train_data, dev_data, test_data = write_train_test_dev(degree_centrality,train_keys,dev_keys,test_keys)
		write_to_file(train_data,baseDir+"train_degree_centrality.txt")
		write_to_file(dev_data,baseDir+"dev_degree_centrality.txt")
		write_to_file(test_data,baseDir+"test_degree_centrality.txt")

	if input==6:
		load_centrality = nx.load_centrality(G,normalized=True)
		load_centrality = normalise(load_centrality)
		train_keys, dev_keys, test_keys = create_train_test_dev_split(load_centrality.keys())
		train_data, dev_data, test_data = write_train_test_dev(load_centrality,train_keys,dev_keys,test_keys)
		write_to_file(train_data,baseDir+"train_load_centrality.txt")
		write_to_file(dev_data,baseDir+"dev_load_centrality.txt")
		write_to_file(test_data,baseDir+"test_load_centrality.txt")

	if input==7:
		shortest_path_length_dict = nx.shortest_path_length(G)
		shortest_path_length = {}
		for key_1 in shortest_path_length_dict:
			for key_2 in shortest_path_length_dict[key_1]:
				shortest_path_length[str(key_1)+"\t"+str(key_2)] = shortest_path_length_dict[key_1][key_2]
		shortest_patth_length = normalise(shortest_path_length)
		train_keys, dev_keys, test_keys = create_train_test_dev_split(shortest_path_length.keys())
		train_data, dev_data, test_data = write_train_test_dev(shortest_path_length,train_keys,dev_keys,test_keys)
		write_to_file(train_data,baseDir+"train_shortest_path_length.txt")
		write_to_file(dev_data,baseDir+"dev_shortest_path_length.txt")
		write_to_file(test_data,baseDir+"test_shortest_path_length.txt")

		'''
		jaccard_coefficient = nx.jaccard_coefficient(G)
		jaccard_coefficient_dict = {}
		for u,v,p in jaccard_coefficient:
			jaccard_coefficient_dict[str(u)+"\t"+str(v)] = p
		jaccard_coefficient_dict = normalise(jaccard_coefficient_dict)
		train_keys, dev_keys, test_keys = create_train_test_dev_split(jaccard_coefficient_dict.keys())
		train_data, dev_data, test_data = write_train_test_dev(jaccard_coefficient_dict,train_keys,dev_keys,test_keys)
		write_to_file(train_data,baseDir+"train_jaccard_coefficient_dict.txt")
		write_to_file(dev_data,baseDir+"dev_jaccard_coefficient_dict.txt")
		write_to_file(test_data,baseDir+"test_jaccard_coefficient_dict.txt")
		'''

	if input==9:
		katz_centrality = nx.katz_centrality(G)
		katz_centrality = normalise(katz_centrality)
		train_keys, dev_keys, test_keys = create_train_test_dev_split(katz_centrality.keys())
		train_data, dev_data, test_data = write_train_test_dev(katz_centrality,train_keys,dev_keys,test_keys)
		write_to_file(train_data,baseDir+"train_katz_centrality.txt")
		write_to_file(dev_data,baseDir+"dev_katz_centrality.txt")
		write_to_file(test_data,baseDir+"test_katz_centrality.txt")

	if input==10:
		pagerank = nx.pagerank(G)
		pagerank = normalise(pagerank)
		train_keys, dev_keys, test_keys = create_train_test_dev_split(pagerank.keys())
		train_data, dev_data, test_data = write_train_test_dev(pagerank,train_keys,dev_keys,test_keys)
		write_to_file(train_data,baseDir+"train_pagerank.txt")
		write_to_file(dev_data,baseDir+"dev_pagerank.txt")
		write_to_file(test_data,baseDir+"test_pagerank.txt")

		'''
		communicability = nx.communicability(G)
		communicability = normalise(pagerank)
		train_keys, dev_keys, test_keys = create_train_test_dev_split(communicability.keys())
		train_data, dev_data, test_data = write_train_test_dev(communicability,train_keys,dev_keys,test_keys)
		write_to_file(train_data,baseDir+"train_communicability.txt")
		write_to_file(dev_data,baseDir+"dev_communicability.txt")
		write_to_file(test_data,baseDir+"test_communicability.txt")
		'''

	if input==121:
		indegree = G.in_degree()
		indegree = normalise(indegree)
		train_keys, dev_keys, test_keys = create_train_test_dev_split(indegree.keys())
		train_data, dev_data, test_data = write_train_test_dev(indegree,train_keys,dev_keys,test_keys)
		write_to_file(train_data,baseDir+"train_indegree.txt")
		write_to_file(dev_data,baseDir+"dev_indegree.txt")
		write_to_file(test_data,baseDir+"test_indegree.txt")

	if input==122:	
		outdegree = G.out_degree()
		outdegree = normalise(outdegree)
		train_keys, dev_keys, test_keys = create_train_test_dev_split(outdegree.keys())
		train_data, dev_data, test_data = write_train_test_dev(outdegree,train_keys,dev_keys,test_keys)
		write_to_file(train_data,baseDir+"train_outdegree.txt")
		write_to_file(dev_data,baseDir+"dev_outdegree.txt")
		write_to_file(test_data,baseDir+"test_outdegree.txt")


##Throws error
#subgraph_centrality = nx.subgraph_centrality(G)
#print subgraph_centrality

#generalized_degree = nx.generalized_degree(G)
#print generalized_degree

#eigen_centrality = nx.eigenvector_centrality(G)
#print type(eigen_centrality)

#current_flow_closeness_centrality = nx.current_flow_closeness_centrality(G)
#print current_flow_closeness_centrality

baseDir="/home/ayushidalmia/interpretNode/graphs/features/graph3/"
baseInputDir = "/home/ayushidalmia/interpretNode/graphs/edgelist/"
inputfilename = "graph3"

#For undirected graph
f=open(baseInputDir+inputfilename, 'r')
G=nx.read_edgelist(f,create_using=nx.DiGraph()) 
f.close()

list_1=[2,3,4,5,6,7,9,10,121,122]
for l in list_1:
	function(l)	
#argument = int(sys.argv[1])
#function(argument)
