import sys
import random
import itertools
import math
random.seed(123)

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

mx=0
for a in auths:
  for b in author_2_author[a]:
    if author_2_author[a][b]>mx:
      mx=author_2_author[a][b]
print(mx)

baseDir = "/home/ayushidalmia/interpretNode/graphs/features/graph1/"
w1 = open(baseDir+'edgeWeight_train', 'w')
w2 = open(baseDir+'edgeWeight_dev', 'w')
w3 = open(baseDir+'edgeWeight_test', 'w')
class_map = {}
for i in xrange(len(auths)):
  cur_auths = author_2_author[auths[i]].keys()
  random.shuffle(cur_auths)
  train_size = int(tr * len(cur_auths))
  dev_size = int(dev * len(cur_auths))
  test_size = len(cur_auths) - train_size - dev_size
  j = 0
  for auth in cur_auths:
    assert(authid_map[auths[i]]!=None)
    assert(authid_map[auth]!=None)
    st = str(authid_map[auths[i]])+"\t"+str(authid_map[auth])+"\t"+str(getclass(author_2_author[auths[i]][auth]))+"\n"
    if j < train_size:
      w1.write(st)
    elif j < train_size + dev_size:
      w2.write(st)
    else:
      w3.write(st)
    j = j + 1    
    cl = getclass(author_2_author[auths[i]][auth])
    if cl not in class_map:
      class_map[cl] = 0
    class_map[cl] = class_map[cl] + 1
w1.close()
w2.close()
w3.close()
#print(class_map)
