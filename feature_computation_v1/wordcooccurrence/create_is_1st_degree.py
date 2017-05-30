import scipy.io
import numpy as np
import random
random.seed(123)
mat = scipy.io.loadmat('/home/ayushidalmia/interpretNode/graphs/dataset/POS.mat')

graph=mat['network']
edges=[]
g={}
cx = scipy.sparse.coo_matrix(graph)
for i,j,v in zip(cx.row, cx.col, cx.data):
  i=str(i)
  j=str(j)
  edges.append([i, j])
  if i not in g:
    g[i]={}
  if j not in g:
    g[j]={}
  g[i][j]=1
  g[j][i]=1

keys=g.keys()
random.shuffle(edges)

def write_to_file(file, start, end):
  w=open(file, 'w')
  i=start
  while i<=end:
    edg = edges[i]
    w.write(edg[0]+"\t"+edg[1]+"\t1\n")
    i = i + 1
  i=start
  while i<=end:
    while True:
      p1=keys[random.randint(0, len(keys)-1)]
      p2=keys[random.randint(0, len(keys)-1)]
      if p1!=p2 and p2 not in g[p1]:
        w.write(p1+"\t"+p2+"\t0\n")
        break
    i=i+1
  w.close()

tr=int(len(edges)*0.7)
dev=int(len(edges)*0.1)
test=len(edges)-tr-dev

baseDir = "/home/ayushidalmia/interpretNode/graphs/features/graph4/"
write_to_file(baseDir+'is1stDegree_train', 0, tr-1)
write_to_file(baseDir+'is1stDegree_dev', tr, tr+dev-1)
write_to_file(baseDir+'is1stDegree_test', tr+dev, tr+dev+test-1)
