# creates directed graph
r = open('/Users/ganeshj/Dropbox/int_node/input/graph1', 'r')
w = open('directed', 'w')
edge_map = {}
for line in r:
  content = line.strip().split(' ')
  if content[0] in edge_map and content[1] in edge_map[content[0]]:
    print('copy found')
    break
  if content[0] not in edge_map:
    edge_map[content[0]] = {}
  edge_map[content[0]][content[1]]=1
  w.write(content[0]+" "+content[1]+" "+content[2]+"\n")
  w.write(content[1]+" "+content[0]+" "+content[2]+"\n")
r.close()
w.close()