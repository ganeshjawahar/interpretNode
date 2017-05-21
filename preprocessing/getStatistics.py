import itertools
import sys

author_2_author = {}
author_2_paper = {}
papers = [] #titile, abstract, category, year
invalid_papers = []
train_from=1990
train_until=2009
test=2010

def process_paper(content):
  authors = []
  author_pairs = []
  abstract = None
  title = None
  category = None
  year = None
  for line in content:
    line = line.lower()
    if line.startswith('#@'):
      auth = line[2:]
      if len(auth)>0:
        authors = auth.split(',')
        if len(authors)>1:
          author_pairs = list(itertools.combinations(authors, 2))
    elif line.startswith('#*'):
      title = line[2:]
    elif line.startswith('#!'):
      abstract = line[2:]
    elif line.startswith('#f'):
      category = line[2:]
    elif line.startswith('#t'):
      year = line[2:]

  #feed a2a
  if len(author_pairs) > 0:
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
  
  if len(authors) > 0:
    #add paper
    papers.append([title, abstract, category, year])
    #feed a2p
    for author in authors:
      if author not in author_2_paper:
        author_2_paper[author] = []
      author_2_paper[author].append(len(papers))      
  else:
    invalid_papers.append(content)

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

print('num. authors with atleast 1 co-authorship = '+str(len(author_2_author)))
print('num. authors = '+str(len(author_2_paper)))
print('num. valid. papers = '+str(len(papers)))
print('num. invalid. papers = '+str(len(invalid_papers)))
