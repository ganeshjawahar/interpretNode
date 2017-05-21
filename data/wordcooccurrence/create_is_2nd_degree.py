import scipy.io
import numpy as np
import random
random.seed(123)
mat = scipy.io.loadmat('../POS.mat')

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
  succ=0
  d={}
  while i<=end:
    edg = edges[i]
    count=0
    for n2 in g[edg[0]]:
      for n3 in g[n2]:
        key=edg[0]+":"+n3
        if key not in d:
          w.write(edg[0]+"\t"+n3+"\t1\n")
          d[key]=1
          count=count+1
        if count>2:
          break
      if count>2:
        break
    succ = succ + count
    i = i + 1
  i=0
  while i<succ:
    while True:
      p1=keys[random.randint(0, len(keys)-1)]
      p2=keys[random.randint(0, len(keys)-1)]
      if p1!=p2 and p1+":"+p2 not in g:
        w.write(p1+"\t"+p2+"\t0\n")
        break
    i=i+1
  w.close()

tr=int(len(edges)*0.7)
dev=int(len(edges)*0.1)
test=len(edges)-tr-dev

write_to_file('is2ndDegree_train', 0, tr-1)
write_to_file('is2ndDegree_dev', tr, tr+dev-1)
write_to_file('is2ndDegree_test', tr+dev, tr+dev+test-1)
