import scipy.io
import numpy as np
import random
import math
random.seed(123)
mat = scipy.io.loadmat('/home/ayushidalmia/interpretNode/graphs/dataset/POS.mat')

from scipy import stats
def create_quantiles(arr, num_bins):
  probs = [ (float(i)/num_bins) for i in range(1, num_bins+1)]
  bin_edges = stats.mstats.mquantiles(sorted(arr), probs)
  return bin_edges

def get_class(num, bin_edges):
  i = 0
  for be in bin_edges[1:]:
    if num <= be:
      return i
    i = i + 1
  return None

graph=mat['network']
edges=[]
cx = scipy.sparse.coo_matrix(graph)
for i,j,v in zip(cx.row, cx.col, cx.data):
  i=str(i)
  j=str(j)
  v=v
  edges.append([i,j,v])

random.shuffle(edges)

def run_to_file():
  i=0
  end=len(edges)
  arr = []
  while i < end:
    edg = edges[i]
    arr.append(edg[2])
    i = i + 1
  return arr

arr = run_to_file()
bin_edges = create_quantiles(arr, 10)
print bin_edges

def write_to_file(file, start, end):
  w=open(file, 'w')
  i=start
  mp = {}
  while i<=end:
    edg = edges[i]
    cl = get_class(edg[2], bin_edges)
    w.write(edg[0]+"\t"+edg[1]+"\t"+str(cl)+"\n")
    i = i + 1
  w.close()

tr=int(len(edges)*0.7)
dev=int(len(edges)*0.1)
test=len(edges)-tr-dev

baseDir = "/home/ayushidalmia/interpretNode/graphs/features/graph4/"
write_to_file(baseDir+'edgeWeight_train', 0, tr-1)
write_to_file(baseDir+'edgeWeight_dev', tr, tr+dev-1)
write_to_file(baseDir+'edgeWeight_test', tr+dev, tr+dev+test-1)
