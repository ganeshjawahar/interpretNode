import scipy.io
import numpy as np
import random
import math
from scipy import stats
import matplotlib.pyplot as plt
random.seed(123)
mat = scipy.io.loadmat('/home/ayushidalmia/interpretNode/graphs/dataset/POS.mat')

def create_quantiles(arr, num_bins):
  sorted(arr)
  probs = [ (i/num_bins) for i in range(1, num_bins+1)]
  bin_edges = stats.mstats.mquantiles(values, probs)
  return bin_edges

def get_class(num, bin_edges):
  i = 0
  for be in bin_edges[1:]:
    if num <= be:
      return i
    i = i + 1
  return None

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

def run_to_file():
  i=0
  end=len(keys)
  arr = []
  while i<=end:
    node = keys[i]
    arr.append(len(nodes_2_c[node]))
    i = i + 1
  return arr
arr = run_to_file()
bin_edges = create_quantiles(arr, 10)

def write_to_file(file, start, end):
  w=open(file, 'w')
  i=start
  while i<=end:
    node = keys[i]
    cl = get_class(len(nodes_2_c[node]), bin_edges)
    w.write(node+"\t"+str(cl)+"\n")
    i = i + 1
  w.close()

tr=int(len(keys)*0.7)
dev=int(len(keys)*0.1)
test=len(keys)-tr-dev
baseDir = "/home/ayushidalmia/interpretNode/graphs/features/graph4/"
write_to_file(baseDir+'countCommunity_train', 0, tr-1)
write_to_file(baseDir+'countCommunity_dev', tr, tr+dev-1)
write_to_file(baseDir+'countCommunity_test', tr+dev, tr+dev+test-1)
