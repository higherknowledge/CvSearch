import json
from gensim import corpora, models, similarities
import os.path as File
from nltk.corpus import wordnet
import itertools
import sys

corpus_path = "./tmp/hk.mm"
index_path = "./tmp/hk.index"
lsi_path = "./tmp/hk.lsi"
dict_path = "./tmp/hk.dict"
stop_words = set("for a an the in of at and to".split())

def getFileContents():
    f = open("input.json", "r")
    file_content = f.read()
    f.close()
    return file_content

def initialize():
    file_content = getFileContents()
    section_array = json.loads(file_content)
    sections = section_array["sections"]

    ## sections contains input strings which are interested headings in the resumes.

    stop_words = set("for a an the in of at and to".split())
    
    # change sections to have synonyms
    section_texts = [[word for word in document.split() if word not in stop_words] for document in sections]

    dictionary = corpora.Dictionary(section_texts)  
    dictionary.save(dict_path)
    corpus = [dictionary.doc2bow(doc) for doc in section_texts]
    corpora.MmCorpus.serialize(corpus_path, corpus)
    index = similarities.MatrixSimilarity(corpus)
    index.save(index_path)


def findSimilarity(heading):    
    if int(sys.argv[2]) == 1:
        initialize()
    
    heading = str(heading)
    index = similarities.MatrixSimilarity.load(index_path)
    #corpus = corpora.MmCorpus(corpus_path)
    dictionary = corpora.Dictionary.load(dict_path)
    #lsi = models.LsiModel(corpus, id2word = dictionary, num_topics=2)
    vec_heading = dictionary.doc2bow(heading.lower().split())
    #vec_lsi = lsi[vec_heading]
    sims = index[vec_heading]
    sims = list(sims)
    index = -1
    max_sim = -1
    for x in range(0, len(sims)):
        if sims[x] > max_sim:
            max_sim = sims[x]
            index = x
    
    if x != -1 and sims[index] > 0:        
        file_content = getFileContents()
        section_array = json.loads(file_content)
        sections = section_array["sections"]
        print "Tag : " + str(sections[index]) + ", input : " + str(heading) + ", similarity : " + str(sims[index])        

def getSimHeader(sentence):
    synonyms = {}
    words = str(sentence).split()
    length = len(words)
    # should remove stop words
    for word in words:
        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                if not synonyms.has_key(word):
                    synonyms[word] = set()
                synonyms[word].add(l.name())
    
    if length == 1:
        for x in synonyms[sentence]:
            findSimilarity(x)
        findSimilarity(sentence)
        return
    
    for i in range(0, length):
        for j in range(i + 1, length):
            product = itertools.product(synonyms[words[i]], synonyms[words[j]])
            for x in list(product):
                clean = x[0] + " " + x[1]
                findSimilarity(clean)
    findSimilarity(sentence)
    
getSimHeader(sys.argv[1])
