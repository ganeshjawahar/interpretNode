import sys
import random
import itertools
import math
random.seed(123)

paper_degree = {}
train_from=1990
train_until=2009
tr = 0.7
dev = 0.1
def getclass(num):
  return 1 + int(math.floor(num/10))

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

  if len(authors) > 0 and year!=None and train_from<=int(year) and int(year)<=train_until:
    #add paper
    paper_degree[paperid]=len(citations)
   
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

papers = paper_degree.keys()
print(len(papers))

random.shuffle(papers)

train_size = int(tr * len(papers))
dev_size = int(dev * len(papers))
test_size = len(papers) - train_size - dev_size

mx=0
for p in papers:
  if paper_degree[p]>mx:
    mx=paper_degree[p]
print(mx)
baseDir = "/home/ayushidalmia/interpretNode/graphs/features/graph3/"
w = open(baseDir+'countDegree_train', 'w')
for i in xrange(train_size):
  w.write(papers[i]+"\t"+str(getclass(paper_degree[papers[i]]))+"\n")
w.close()

w = open(baseDir+'countDegree_dev', 'w')
for i in xrange(dev_size):
  w.write(papers[train_size+i]+"\t"+str(getclass(paper_degree[papers[train_size+i]]))+"\n")
w.close()

w = open(baseDir+'countDegree_test', 'w')
for i in xrange(test_size):
  w.write(papers[train_size+dev_size+i]+"\t"+str(getclass(paper_degree[papers[train_size+dev_size+i]]))+"\n")
w.close()
