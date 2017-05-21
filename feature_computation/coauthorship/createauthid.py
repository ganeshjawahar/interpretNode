import itertools
import sys

author_list = {}
def process_paper(content):
  authors = []
  for line in content:
    line = line.lower()
    if line.startswith('#@'):
      auth = line[2:]
      if len(auth)>0:
        authors = auth.split(',')
  if len(authors) > 0:
    for a in authors:
      if a not in author_list:
        author_list[a]=1

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

w=open('authids', 'w')
for k in author_list:
  w.write(k+'\n')
w.close()