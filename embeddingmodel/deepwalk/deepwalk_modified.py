# Created on 16th May 2016

import getWalks as gw
import multiprocessing
import logging
import gensim
import time
import os
import sys

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
CORES = multiprocessing.cpu_count()

FLAG_preTrained = False


def writeAsText(random_walks):
    out_f = open('random_walk.txt', 'w')
    for walk in random_walks:
        arr = [str(node) for node in walk]
        string = ' '.join(arr) + '\n'
        out_f.write(string)
    out_f.close()

def getContext(graph_file, num_walks, walk_size):
    graph = gw.load_edgelist(graph_file)
    random_walks = gw.build_deepwalk_corpus(graph, num_walks, walk_size)
    #writeAsText(random_walks)
    return random_walks

def train(model_params):
    sentences = getContext(model_params['graph_file'], model_params['num_walks'], model_params['walk_size'])
    model = gensim.models.Word2Vec(size=model_params['vec_size'], window=model_params['window'], min_count=0, workers=CORES)
    model.build_vocab(sentences)
    if FLAG_preTrained:
        model.intersect_word2vec_format(model_params['embd_file'])
    model.train(sentences)
    return model

def main(model_params):
    #for i in range(1, 1):
    #model_params['graph_file'] = str(i) + 'k_sim.txt'
    model = train(model_params)
    #if i==1:
    model.save_word2vec_format(sys.argv[2], binary=False)

#if __name__ == '__main__':
model_params = {'graph_file': sys.argv[1], 'num_walks': 10, 'walk_size': 80, 'embd_file': './embeddings/10d2v_200.txt', 'vec_size': 128, 'window': 5}
main(model_params)
#getContext(model_params['graph_file'], model_params['num_walks'], model_params['walk_size'])
