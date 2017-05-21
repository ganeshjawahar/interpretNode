import sys
fmap = {}
with open(sys.argv[1]) as f:
  i=0
  dim=None
  for line in f:
    i=i+1
    if i==1:
      content = line.strip().split()
      dim=int(content[1])
    else:
      content=line.strip().split()
      assert(len(content)==(dim+1))
      fmap[content[0]]=line.strip()[len(content[0]):]

w=open(sys.argv[3], 'w')
with open(sys.argv[2]) as f:
  i=0
  dim=None
  for line in f:
    i=i+1
    if i==1:
      content = line.strip().split()
      dim=int(content[1])
      w.write(content[0]+" "+str(2*dim)+"\n")
    else:
      content = line.strip().split()
      assert(len(content)==(dim+1))
      w.write(content[0]+fmap[content[0]]+line.strip()[len(content[0]):]+"\n")

w.close()
