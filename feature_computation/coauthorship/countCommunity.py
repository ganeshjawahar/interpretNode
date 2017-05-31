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
num_samples=5
tr = 0.7
dev = 0.1
author_2_category = {}
category_2_author = {}

def process_paper(content):
  authors = []
  year = None
  category = None
  for line in content:
    line = line.lower()
    if line.startswith('#@'):
      auth = line[2:]
      if len(auth)>0:
        authors = auth.split(',')
    elif line.startswith('#t'):
      year = line[2:]
    elif line.startswith('#f'):
      category = line[2:]

  #feed a2a
  if year!=None and category!=None and len(authors) > 0 :
    year=int(year)
    if train_from<=year and year<=train_until:
      for auth in authors:
        auth = authid_map[auth]
        assert(auth!=None)
        if auth not in author_2_category:
          author_2_category[auth]={}
        author_2_category[auth][category] = 1
        if category not in category_2_author:
          category_2_author[category] = {}
        category_2_author[category][auth] = 1
  

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

auths = author_2_category.keys()
print(len(auths))
random.shuffle(auths)

train_size = int(tr * len(auths))
dev_size = int(dev * len(auths))
test_size = len(auths) - train_size - dev_size

def run_to_file():
  i=0
  end=len(auths)
  arr = []
  while i < end:
    cur_auth=auths[i]
    cur_cats=author_2_category[cur_auth]
    arr.append(len(cur_cats))
    i = i + 1
  return arr

arr = run_to_file()
bin_edges = create_quantiles(arr, 10)
print bin_edges

def write_file(file, start, end):
  w = open(file, 'w')
  mp = {}
  while start <= end:
    cur_auth=auths[start]
    cur_cats=author_2_category[cur_auth]
    cl = get_class(len(cur_cats), bin_edges)
    w.write(str(cur_auth)+"\t"+str(cl)+"\n")
    start = start + 1
    if cl not in mp:
      mp[cl] = 0
    mp[cl] = mp[cl] + 1
  w.close()
  print(mp)

baseDir = "/home/ayushidalmia/interpretNode/graphs/features/graph1/"
write_file(baseDir+'countCommunity_train', 0, train_size-1)
write_file(baseDir+'countCommunity_dev', train_size, train_size+dev_size-1)
write_file(baseDir+'countCommunity_test', train_size+dev_size, train_size+dev_size+test_size-1)
