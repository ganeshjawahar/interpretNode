import scipy.io
import numpy as np
mat = scipy.io.loadmat('../POS.mat')
#print(mat)

nodes={}
graph=mat['network']
edges={}
cx = scipy.sparse.coo_matrix(graph)
w=open('graph4_line', 'w')
for i,j,v in zip(cx.row, cx.col, cx.data):
  key=str(i)+":"+str(j)
  key_rev=str(j)+":"+str(i)
  #if key_rev not in edges:
  w.write(str(i)+" "+str(j)+" "+str(v)+"\n")
  #w.write(str(i)+" "+str(j)+" "+"\n")
  edges[key]=1
  nodes[i]=[]
  nodes[j]=[]
w.close()
print(len(nodes))

'''
labels=mat['group']
cx = scipy.sparse.coo_matrix(labels)
w=open('graph4_labels', 'w')
k=0
for i,j,v in zip(cx.row, cx.col, cx.data):
  if i not in nodes or j not in nodes:
    print('error')
  nodes[i].append(j)
  #w.write(str(i)+" "+str(j)+" "+str(v)+"\n")
  k=k+1
for key in nodes:
  res=''
  for val in nodes[key]:
    res+=str(val)+","
  res=res[:-1]
  w.write(str(key)+" "+res+"\n")
w.close()
print(k)
'''
'''
graph=mat['network']
cx = scipy.sparse.coo_matrix(graph)
wt=np.zeros(shape=(5000, 5000))
wt.fill(-1)
for i,j,v in zip(cx.row, cx.col, cx.data):
  wt[i][j]=v

for i,j,v in zip(cx.row, cx.col, cx.data):
  if wt[i][j]!=wt[j][i]:
    print('error')
print('success')
'''