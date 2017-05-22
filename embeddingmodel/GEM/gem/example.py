from gem.embedding.gf import GraphFactorization as gf
from gem.evaluation import evaluate_graph_reconstruction as gr
from gem.utils.graph_util import *

# Instatiate the embedding method with hyperparameters
em = gf(2, 100000, 1*10**-4, 1.0)

# Load graph
graph = loadGraphFromEdgeListTxt('data/karate.edgelist')

# Learn embedding - accepts a networkx graph or file with edge list
Y, t = em.learn_embedding(graph, edge_f=None, is_weighted=True, no_python=True)

# Evaluate on graph reconstruction
MAP, prec_curv = gr.evaluateStaticGraphReconstruction(graph, em, Y, None)

print MAP, prec_curve
