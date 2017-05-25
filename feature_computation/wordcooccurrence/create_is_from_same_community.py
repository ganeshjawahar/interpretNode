import scipy.io
import numpy as np
import random
random.seed(123)
mat = scipy.io.loadmat('/home/ayushidalmia/interpretNode/graphs/dataset/POS.mat')

labels=mat['group']
cx = scipy.sparse.coo_matrix(labels)
nm_2_c = {}
cm_2_n = {}
na_2_c = {}
ca_2_n = {}
for i,j,v in zip(cx.row, cx.col, cx.data):
  i=str(i)
  j=str(j)
  if i not in na_2_c:
    na_2_c[i]=[]
  if j not in ca_2_n:
    ca_2_n[j]=[]
  na_2_c[i].append(j)
  ca_2_n[j].append(i)
  if i not in nm_2_c:
    nm_2_c[i]={}
  if j not in cm_2_n:
    cm_2_n[j]={}
  nm_2_c[i][j]=1
  cm_2_n[j][i]=1

keys = nm_2_c.keys()
random.shuffle(keys)
categories = cm_2_n.keys()
'''
cats={}
for cat in c_2_n:
  cats[cat]=c_2_n[cat].keys()
  random.shuffle(cats[cat])
'''
def get_rand_cat(c):
  while True:
    rc = categories[random.randint(0, len(categories)-1)]
    if rc not in c:
      return rc
  print('error')
  return categories[0]

def write_to_file(file, start, end):
  w=open(file, 'w')
  i=start
  while i<=end:
    node = keys[i]

    cats = na_2_c[node]
    same_cat = cats[random.randint(0, len(cats)-1)]
    same_cat_nodes = ca_2_n[same_cat]
    same_cat_node = same_cat_nodes[random.randint(0, len(same_cat_nodes)-1)]

    rand_cat = get_rand_cat(nm_2_c[node])
    rand_cat_nodes = ca_2_n[rand_cat]
    rand_cat_node = rand_cat_nodes[random.randint(0, len(rand_cat_nodes)-1)]
    w.write(node+"\t"+same_cat_node+"\t1\n")
    w.write(node+"\t"+rand_cat_node+"\t0\n")
    i = i + 1
  w.close()

tr=int(len(keys)*0.7)
dev=int(len(keys)*0.1)
test=len(keys)-tr-dev
baseDir = "/home/ayushidalmia/interpretNode/graphs/features/graph4/"
write_to_file(baseDir+'isFromSameCommunity_train', 0, tr-1)
write_to_file(baseDir+'isFromSameCommunity_dev', tr, tr+dev-1)
write_to_file(baseDir+'isFromSameCommunity_test', tr+dev, tr+dev+test-1)
