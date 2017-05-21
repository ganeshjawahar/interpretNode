from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC, LinearSVC
from sklearn import metrics, cross_validation
from operator import itemgetter
from time import time
import numpy as np
import multiprocessing
import random
import os

CORES = multiprocessing.cpu_count()

# Load the full embedding file to a dict
def loadEmbeddings(path):
	f = open(path, 'r')
	first = f.readline()
	d = {}
	for line in f:
		arr = line.strip().split()
		key, val = long(arr[0]), arr[1:]
		d[key] = [float(i) for i in val]
	f.close()
	return d

def getEdgeVector(vec1, vec2):
	sub = np.abs(vec1 - vec2)
	mul = vec1 * vec2
	return np.concatenate((sub, mul), axis=0)

def prepareDataset(data_dict):
	f = open('binary_dataset.txt', 'r')
	data, labels = [], []
	for line in f:
		arr = line.strip().split()
		id1, id2, label = long(arr[0]), long(arr[1]), int(float(arr[2]))
		try:
			vec1, vec2 = np.array(data_dict[id1]), np.array(data_dict[id2])
			feature_vec = getEdgeVector(vec1, vec2)
			data.append(feature_vec)
			labels.append(label)
		except KeyError:
			print line
			pass
	f.close()
	return data, labels


def train(path):
	data_dict = loadEmbeddings(path)
	X, y = prepareDataset(data_dict)
	scaler = StandardScaler()
	X = scaler.fit_transform(X)
	#print X.shape

	clf = LogisticRegression(penalty='l2')
	#clf = SVC(kernel='rbf', C=1.5)
	#clf = LinearSVC(C=1.0)
	scores = cross_validation.cross_val_score(clf, X, y, cv=3, scoring='accuracy', n_jobs=CORES)
	print path, sum(scores) / len(scores) * 100

def main():
	print '======================================\n'
	path = './'
	all_files = os.listdir(path)
	for file in all_files:
		if '.emb' in file:
			train(path + file)


if __name__ == '__main__':
	main()