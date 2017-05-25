import sys
import random
import itertools
import math
random.seed(123)

train_from=1990
train_until=2009
num_samples=5
tr = 0.7
dev = 0.1
num_samples = 5
paper_2_category = {}
category_2_paper = {}

def process_paper(content):
  authors = []
  year = None
  citations = []
  paperid = None
  for line in content:
    line = line.lower()
    if line.startswith('#@'):
      auth = line[2:]
      if len(auth)>0:
        authors = auth.split(',')
    elif line.startswith('#t'):
      year = line[2:]
    elif line.startswith('#index'):
      paperid=line[len('#index'):]
    elif line.startswith('#%'):
      citations.append(line[len('#%'):])
    elif line.startswith('#f'):
      category = line[2:]

  if len(authors) > 0 and year!=None and category!=None and paperid!=None:
    year=int(year)
    assert(paperid not in paper_2_category)
    paper_2_category[paperid]=category
    if category not in category_2_paper:
      category_2_paper[category] = {}
    category_2_paper[category][paperid]=1
  

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

papers = paper_2_category.keys()
print(len(papers))
rand_c2p_list = {}
rand_c2p_cur = {}
for cat in category_2_paper.keys():
  rand_c2p_cur[cat]=0
  rand_c2p_list[cat]=category_2_paper[cat].keys()
  random.shuffle(rand_c2p_list[cat])
random.shuffle(papers)

train_size = int(tr * len(papers))
dev_size = int(dev * len(papers))
test_size = len(papers) - train_size - dev_size

def write_file(file, start, end):
  w = open(file, 'w')
  succ=0
  while start <= end:
    cur_paper=papers[start]
    cur_cat=paper_2_category[cur_paper]
    for i in xrange(num_samples):
      n_paper = rand_c2p_list[cur_cat][rand_c2p_cur[cur_cat]]
      w.write(cur_paper+"\t"+n_paper+"\t1\n")
      rand_c2p_cur[cur_cat] = (rand_c2p_cur[cur_cat]+1)%len(rand_c2p_list[cur_cat])
      succ = succ + 1
    start = start + 1
  for i in xrange(succ):
    print(file+"\t"+str(i))
    while True:
      r_p1 = papers[random.randint(0, len(papers)-1)]
      r_p2 = papers[random.randint(0, len(papers)-1)]
      if r_p1!=r_p2 and r_p1 in paper_2_category and r_p2 in paper_2_category and paper_2_category[r_p1]!=paper_2_category[r_p2]:
        w.write(r_p1+"\t"+r_p2+"\t0\n")
        break
  w.close()
baseDir = "/home/ayushidalmia/interpretNode/graphs/features/graph3/"
write_file(baseDir+'sameCommunity_train', 0, train_size-1)
write_file(baseDir+'sameCommunity_dev', train_size, train_size+dev_size-1)
write_file(baseDir+'sameCommunity_test', train_size+dev_size, train_size+dev_size+test_size-1)
