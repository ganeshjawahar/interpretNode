import sys
import random
import itertools
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
num_per_node = 5

train_auth_2_auth = {}
dev_auth_2_auth = {}
test_auth_2_auth = {}
train_from=1990
train_until=2006
dev_year=2007
test_year=2008
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
    if train_from<=year and year<=train_until:
      for a2a in author_pairs:
        assert(authid_map[a2a[0]]!=None)
        assert(authid_map[a2a[1]]!=None)
        id1 = authid_map[a2a[0]]
        id2 = authid_map[a2a[1]]
        if id1 not in train_auth_2_auth:
          train_auth_2_auth[id1] = {}
        train_auth_2_auth[id1][id2] = 1
        if id2 not in train_auth_2_auth:
          train_auth_2_auth[id2] = {}
        train_auth_2_auth[id2][id1] = 1
    elif year==dev_year:
      for a2a in author_pairs:
        assert(authid_map[a2a[0]]!=None)
        assert(authid_map[a2a[1]]!=None)
        id1 = authid_map[a2a[0]]
        id2 = authid_map[a2a[1]]
        if id1 not in dev_auth_2_auth:
          dev_auth_2_auth[id1] = {}
        dev_auth_2_auth[id1][id2] = 1
        if id2 not in dev_auth_2_auth:
          dev_auth_2_auth[id2] = {}
        dev_auth_2_auth[id2][id1] = 1
    elif year>=test_year:
      for a2a in author_pairs:
        assert(authid_map[a2a[0]]!=None)
        assert(authid_map[a2a[1]]!=None)
        id1 = authid_map[a2a[0]]
        id2 = authid_map[a2a[1]]
        if id1 not in test_auth_2_auth:
          test_auth_2_auth[id1] = {}
        test_auth_2_auth[id1][id2] = 1
        if id2 not in test_auth_2_auth:
          test_auth_2_auth[id2] = {}
        test_auth_2_auth[id2][id1] = 1    

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

def write_set(file, mp):
  rand_a2a_list = {}
  rand_a2a_cur = {}
  for auth in mp.keys():
    rand_a2a_cur[auth]=0
    rand_a2a_list[auth]=mp[auth].keys()
    random.shuffle(rand_a2a_list[auth])

  w = open(file, 'w')
  succ=0
  d={}
  for key in mp:
    for a1 in mp[key]:
      if a1 in mp:
        cur_set = rand_a2a_list[a1]
        for i in xrange(min(num_per_node, len(cur_set))):
          cur_n = rand_a2a_list[a1][rand_a2a_cur[a1]]
          rand_a2a_cur[a1] = (rand_a2a_cur[a1]+1)%len(rand_a2a_list[a1])
          succ=succ+1
          w.write(str(key)+"\t"+str(cur_n)+"\t1\n")
          d[str(key)+"$$$"+str(cur_n)]=1
  authors = mp.keys()
  print(len(authors))
  for i in xrange(succ):
    print(file+"\t"+str(i))
    while True:
      p1=authors[random.randint(0, len(authors)-1)]
      p2=authors[random.randint(0, len(authors)-1)]
      if p1!=p2 and p1 in mp and p2 in mp and str(p1)+"$$$"+str(p2) not in d:
        w.write(str(p1)+"\t"+str(p2)+"\t0\n")
        break
  w.close()
baseDir = "/home/ayushidalmia/interpretNode/graphs/features/graph1/"
print('train set...')
write_set(baseDir+'is2ndDegree_train', train_auth_2_auth)

print('dev set...')
write_set(baseDir+'is2ndDegree_dev', dev_auth_2_auth)

print('test set...')
write_set(baseDir+'is2ndDegree_test', test_auth_2_auth)
