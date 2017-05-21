import scipy.io
import numpy as np
import random
import math
random.seed(123)
mat = scipy.io.loadmat('../POS.mat')

graph=mat['network']
edges=[]
cx = scipy.sparse.coo_matrix(graph)
for i,j,v in zip(cx.row, cx.col, cx.data):
  i=str(i)
  j=str(j)
  v=v
  edges.append([i,j,v])

random.shuffle(edges)

def getclass(num):
  return 1 + int(math.floor(num/10))

def write_to_file(file, start, end):
  w=open(file, 'w')
  i=start
  while i<=end:
    edg = edges[i]
    w.write(edg[0]+"\t"+edg[1]+"\t"+str(getclass(edg[2]))+"\n")
    i = i + 1
  w.close()

tr=int(len(edges)*0.7)
dev=int(len(edges)*0.1)
test=len(edges)-tr-dev

write_to_file('edgeWeight_train', 0, tr-1)
write_to_file('edgeWeight_dev', tr, tr+dev-1)
write_to_file('edgeWeight_test', tr+dev, tr+dev+test-1)
