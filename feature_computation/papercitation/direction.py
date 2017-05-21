import sys
import random
import itertools
random.seed(123)

train_edges  = []
dev_edges = []
test_edges = []
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
      for cite in citations:
        train_edges.append([paperid, cite])
    elif year==dev_year:
      for cite in citations:
        dev_edges.append([paperid, cite])
    elif year>=test_year:
      for cite in citations:
        test_edges.append([paperid, cite])

# parse the file
f = open('../CS_Citation_Network', 'r')
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

def write_set(file, edges):
  w = open(file, 'w')
  for edge in edges:
    w.write(edge[0]+"\t"+edge[1]+"\t1\n")
    w.write(edge[1]+"\t"+edge[0]+"\t0\n")
  w.close()

print('train set...')
write_set('direction_train', train_edges)

print('dev set...')
write_set('direction_dev', dev_edges)

print('test set...')
write_set('direction_test', test_edges)

