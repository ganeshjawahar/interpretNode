import sys
import random
import itertools
import math
random.seed(123)

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

def get_authid_map():
  # get authid map
  authids = [line.rstrip('\n') for line in open('authids')]
  authid_map={}
  c=0
  for i in authids:
    authid_map[i]=c
    c=c+1
  return authid_map

authid_map = get_authid_map()
auth_degree = {}
train_from=1990
train_until=2009
tr = 0.7
dev = 0.1
def getclass(num):
  return 1 + int(math.floor(num/5))
author_2_author = {}

def process_paper(content):
  author_pairs = []
  year = None
  for line in content:
    line = line.lower()
    if line.startswith('#@'):
      auth = line[2:]
      if len(auth)>0:
        authors = auth.split(',')
        if len(authors)>1:
          author_pairs = list(itertools.combinations(authors, 2))
    elif line.startswith('#t'):
      year = line[2:]

  #feed a2a
  if year!=None and len(author_pairs) > 0 :
    year=int(year)
    for a2a in author_pairs:
      if a2a[0] not in author_2_author:
        author_2_author[a2a[0]] = {}
      if a2a[1] not in author_2_author[a2a[0]]:
        author_2_author[a2a[0]][a2a[1]] = 0
      author_2_author[a2a[0]][a2a[1]] = author_2_author[a2a[0]][a2a[1]] + 1
      if a2a[1] not in author_2_author:
        author_2_author[a2a[1]] = {}
      if a2a[0] not in author_2_author[a2a[1]]:
        author_2_author[a2a[1]][a2a[0]] = 0
      author_2_author[a2a[1]][a2a[0]] = author_2_author[a2a[1]][a2a[0]] + 1  

# parse the file
f = open('/home/ayushidalmia/interpretNode/graphs/dataset/CS_Citation_Network', 'r')
paper_content=[]
for line in f:
  line = line.strip()
  if len(line)==0:
    process_paper(paper_content)
    paper_content=[]
  else:
    paper_content.append(line)
process_paper(paper_content)
f.close()

auths = author_2_author.keys()
print(len(auths))

random.shuffle(auths)

train_size = int(tr * len(auths))
dev_size = int(dev * len(auths))
test_size = len(auths) - train_size - dev_size

mx=0
class_map = {}
for a in auths:
  if len(author_2_author[a])>mx:
    mx=len(author_2_author[a])
  cl = getclass(len(author_2_author[a]))
  if cl not in class_map:
    class_map[cl] = 0
  class_map[cl] = class_map[cl] + 1
#print(mx)
#print(class_map)
baseDir = "/home/ayushidalmia/interpretNode/graphs/features/graph1/"

def run_to_file():
  i=0
  end=len(auths)
  arr = []
  while i < end:
    arr.append(len(author_2_author[auths[i]]))
    i = i + 1
  return arr

arr = run_to_file()
bin_edges = create_quantiles(arr, 10)
print bin_edges

mp = {}
w = open(baseDir+'countDegree_train', 'w')
for i in xrange(train_size):
  assert(authid_map[auths[i]]!=None)
  cl = get_class(len(author_2_author[auths[i]]), bin_edges)
  w.write(str(authid_map[auths[i]])+"\t"+str(cl)+"\n")
  if cl not in mp:
    mp[cl] = 0
  mp[cl] = mp[cl] + 1
w.close()
print(mp)

w = open(baseDir+'countDegree_dev', 'w')
for i in xrange(dev_size):
  assert(authid_map[auths[train_size+i]]!=None)
  cl = get_class(len(author_2_author[auths[train_size+i]]), bin_edges)
  w.write(str(authid_map[auths[train_size+i]])+"\t"+str(cl)+"\n")
  if cl not in mp:
    mp[cl] = 0
  mp[cl] = mp[cl] + 1
w.close()
print(mp)

w = open(baseDir+'countDegree_test', 'w')
for i in xrange(test_size):
  assert(authid_map[auths[train_size+dev_size+i]]!=None)
  cl = get_class(len(author_2_author[auths[train_size++dev_size+i]]), bin_edges)
  w.write(str(authid_map[auths[train_size++dev_size+i]])+"\t"+str(cl)+"\n")
  if cl not in mp:
    mp[cl] = 0
  mp[cl] = mp[cl] + 1
w.close()
print(mp)
