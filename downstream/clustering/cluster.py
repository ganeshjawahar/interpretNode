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
        dataset.append([np.array(dic[nid]), l_i[label],nid])
  r.close()
  random.shuffle(dataset)
  tr=int(len(dataset)*0.7)
  rem = len(dataset)-tr
  train=dataset[0:tr]
  train_feat, train_lab, train_id  = [], [], []
  for d in train:
    train_feat.append(d[0])
    train_lab.append(d[1])
    train_id.append(d[2])
  test=dataset[tr:]
  test_feat, test_lab, test_id  = [], [], []
  for d in test:
    test_feat.append(d[0])
    test_lab.append(d[1])
    test_id.append(d[2])
  return train_feat, train_lab, test_feat, test_lab, train_id, test_id

data_dict = loadEmbeddings(emb_f)
train_feat, train_lab, test_feat, test_lab, train_id, test_id = prepareDataset(lab_f, data_dict)
kmeans = KMeans(n_clusters=24, random_state=0).fit(train_feat)
lab=kmeans.predict(test_feat)

print(sys.argv[1]+"\t"+sys.argv[2]+"\t"+str(normalized_mutual_info_score(test_lab, lab)))

data = []
for i in range(len(lab)):
	arr = [str(j) for j in test_feat[i]]
        if lab[i] == test_lab[i]:
                data.append(str(test_id[i])+"\t"+str(1))
        else:
                data.append(str(test_id[i])+"\t"+str(0))


embeddingfile = sys.argv[2].strip().split("/")[-1]
graphfile = sys.argv[1].strip().split("/")[-1].split("_")[0]
outputfolder = sys.argv[3]

f=open(outputfolder+"/"+graphfile+"_"+embeddingfile+"clustering.txt","w")
f.write("\n".join(data))
f.close()
