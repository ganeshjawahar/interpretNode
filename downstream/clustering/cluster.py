import sys
from sklearn.cluster import KMeans
import random
import os
random.seed(123)
from sklearn.metrics.cluster import normalized_mutual_info_score
import numpy as np

lab_f = sys.argv[1]
emb_f = sys.argv[2]

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

def prepareDataset(file, dic):
  r=open(file,'r')
  dataset=[]
  l_i = {}
  for line in r:
    content=line.strip().split()
    nid=long(content[0])
    if nid in dic:
      lab = content[1].split(',')
      if len(lab)==1:
        #data.append(np.array(dic[nid]))
        label=content[1]
        if label not in l_i:
          l_i[label]=len(l_i)+1
        dataset.append([np.array(dic[nid]), l_i[label]])
  r.close()
  random.shuffle(dataset)
  tr=int(len(dataset)*0.7)
  rem = len(dataset)-tr
  train=dataset[0:tr]
  train_feat, train_lab = [], []
  for d in train:
    train_feat.append(d[0])
    train_lab.append(d[1])
  test=dataset[tr:]
  test_feat, test_lab = [], []
  for d in test:
    test_feat.append(d[0])
    test_lab.append(d[1])
  return train_feat, train_lab, test_feat, test_lab

data_dict = loadEmbeddings(emb_f)
train_feat, train_lab, test_feat, test_lab= prepareDataset(lab_f, data_dict)
kmeans = KMeans(n_clusters=24, random_state=0).fit(train_feat)
lab=kmeans.predict(test_feat)
print(sys.argv[1]+"\t"+sys.argv[2]+"\t"+str(normalized_mutual_info_score(test_lab, lab)))
