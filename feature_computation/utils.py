import random
random.seed(123)

def normalise(input_dictionary):

	'''
	import math
	max_value = max(input_dictionary.values())
 	min_value = min(input_dictionary.values())
 	for key in input_dictionary:
 		temp = float(input_dictionary[key] - min_value)/(max_value - min_value)
 		input_dictionary[key] = int(math.ceil(temp*10))
	'''
	from scipy import stats
	
	bin_edges = stats.mstats.mquantiles(sorted(input_dictionary.values()),prob = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,1.0])
	for key in input_dictionary:
		for i in range(len(bin_edges)):
			if input_dictionary[key] <= bin_edges[i]:
				input_dictionary[key]=i
				break
		    
 	return input_dictionary

def create_train_test_dev_split(keys):

	random.shuffle(keys)
	number_of_entries = len(keys)
	train = int(round(number_of_entries*0.7))
	dev = int(round(number_of_entries*0.9))
	train_keys = keys[:train]
	dev_keys = keys[train:dev]
	test_keys = keys[dev:]
	return train_keys, dev_keys, test_keys

def write_train_test_dev(input_dictionary,train_keys,dev_keys,test_keys):

	train_data=[]
	for key in train_keys:
		train_data.append(str(key)+"\t"+str(input_dictionary[key]))

	dev_data=[]
	for key in dev_keys:
		dev_data.append(str(key)+"\t"+str(input_dictionary[key]))

	test_data=[]
	for key in test_keys:
		test_data.append(str(key)+"\t"+str(input_dictionary[key]))

	return train_data, dev_data, test_data

def write_to_file(data,filename):
	f=open(filename,"w")
	f.write("\n".join(data))
	f.close()
