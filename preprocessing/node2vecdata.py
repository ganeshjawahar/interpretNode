import itertools
import sys

# get authid map
authids = [line.rstrip('\n') for line in open('authids')]
authid_map={}
c=0
for i in authids:
  authid_map[i]=c
  c=c+1

edge_list = []
train_from=1990
train_until=2009
test=2010

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
  if year!=None:
    year=int(year)
    if train_from<=year and year<=train_until and len(author_pairs) > 0:
      for a2a in author_pairs:
        assert(authid_map[a2a[0]]!=None)
        assert(authid_map[a2a[1]]!=None)
        edge_list.append([authid_map[a2a[0]],authid_map[a2a[1]]])

# parse the file
f = open('CS_Citation_Network', 'r')
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

print('num. edges = '+str(len(edge_list)))

w=open('edgelist', 'w')
for edge in edge_list:
  w.write(str(edge[0])+" "+str(edge[1])+"\n")
w.close()
