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

rand_c2p_list = {}
rand_c2p_cur = {}
for cat in category_2_author.keys():
  rand_c2p_cur[cat]=0
  rand_c2p_list[cat]=category_2_author[cat].keys()
  random.shuffle(rand_c2p_list[cat])

train_size = int(tr * len(auths))
dev_size = int(dev * len(auths))
test_size = len(auths) - train_size - dev_size

def write_file(file, start, end):
  w = open(file, 'w')
  succ=0
  while start <= end:
    cur_auth=auths[start]
    cur_cats=author_2_category[cur_auth]
    for cur_cat in cur_cats:
      for i in xrange(num_samples):
        n_auth = rand_c2p_list[cur_cat][rand_c2p_cur[cur_cat]]
        w.write(str(cur_auth)+"\t"+str(n_auth)+"\t1\n")
        rand_c2p_cur[cur_cat] = (rand_c2p_cur[cur_cat]+1)%len(rand_c2p_list[cur_cat])
        succ = succ + 1
    start = start + 1
  for i in xrange(succ):
    print(file+"\t"+str(i))
    while True:
      r_p1 = auths[random.randint(0, len(auths)-1)]
      r_p2 = auths[random.randint(0, len(auths)-1)]
      if r_p1!=r_p2 and r_p1 in author_2_category and r_p2 in author_2_category and author_2_category[r_p1]!=author_2_category[r_p2]:
        w.write(str(r_p1)+"\t"+str(r_p2)+"\t0\n")
        break
  w.close()
baseDir = "/home/ayushidalmia/interpretNode/graphs/features/graph1/"
write_file(baseDir+'sameCommunity_train', 0, train_size-1)
write_file(baseDir+'sameCommunity_dev', train_size, train_size+dev_size-1)
write_file(baseDir+'sameCommunity_test', train_size+dev_size, train_size+dev_size+test_size-1)
