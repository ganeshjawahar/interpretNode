import scipy.io
import numpy as np
import random
import math
random.seed(123)
mat = scipy.io.loadmat('../POS.mat')

graph=mat['group']
nodes_2_c={}
cx = scipy.sparse.coo_matrix(graph)
for i,j,v in zip(cx.row, cx.col, cx.data):
  i=str(i)
  j=str(j)
  if i not in nodes_2_c:
    nodes_2_c[i]=[]
  nodes_2_c[i].append(j)
keys=nodes_2_c.keys()
random.shuffle(keys)

def write_to_file(file, start, end):
  w=open(file, 'w')
  i=start
  while i<=end:
    node = keys[i]
    w.write(node+"\t"+str(len(nodes_2_c[node]))+"\n")
    i = i + 1
  w.close()

tr=int(len(keys)*0.7)
dev=int(len(keys)*0.1)
test=len(keys)-tr-dev

write_to_file('countCommunity_train', 0, tr-1)
write_to_file('countCommunity_dev', tr, tr+dev-1)
write_to_file('countCommunity_test', tr+dev, tr+dev+test-1)
