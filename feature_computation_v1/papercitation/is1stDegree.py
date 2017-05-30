import sys
import random
import itertools
random.seed(123)

train_paper_2_paper  = {}
dev_paper_2_paper = {}
test_paper_2_paper = {}
train_from=1990
train_until=2006
dev_year=2007
test_year=2008
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

  if len(authors) > 0 and year!=None:
    year=int(year)
    if train_from<=year and year<=train_until:
      train_paper_2_paper[paperid] = {}
      for cite in citations:
        train_paper_2_paper[paperid][cite]=1
    elif year==dev_year:
      dev_paper_2_paper[paperid] = {}
      for cite in citations:
        dev_paper_2_paper[paperid][cite]=1
    elif year>=test_year:
      test_paper_2_paper[paperid] = {}
      for cite in citations:
        test_paper_2_paper[paperid][cite]=1 

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
  w = open(file, 'w')
  succ=0
  for key in mp :
    for a1 in mp[key]:
      succ=succ+1
      w.write(key+"\t"+a1+"\t1\n")
  papers = mp.keys()
  print(len(papers))
  for i in xrange(succ):
    print(file+"\t"+str(i))
    while True:
      p1=papers[random.randint(0, len(papers)-1)]
      p2=papers[random.randint(0, len(papers)-1)]
      if p1!=p2 and p1 in mp and p2 not in mp[p1]:
        w.write(p1+"\t"+p2+"\t0\n")
        break
  w.close()
baseDir = "/home/ayushidalmia/interpretNode/graphs/features/graph3/"

print('train set...')
write_set(baseDir+'is1stDegree_train', train_paper_2_paper)

print('dev set...')
write_set(baseDir+'is1stDegree_dev', dev_paper_2_paper)

print('test set...')
write_set(baseDir+'is1stDegree_test', test_paper_2_paper)

print(len(train_paper_2_paper ))
print(len(dev_paper_2_paper))
print(len(test_paper_2_paper))

