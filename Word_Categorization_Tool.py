import sys
import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from multiprocessing import Process

filepath = input("Please enter the file path and the name of file with extention:\n")

def main():
    rline = readFile(filepath)
    print("Lines of the file:\n\n", rline)

    print("\n")
    
    tline = tokenizeSentences()
    print("Tokenize of the lines into words:\n\n", tline)

    print("\n")
      
    fline = filterTokenWords()
    print("Filter the token words with stopwords and punctuations:\n\n", fline)

    print("\n")
     
    tagword = posTagging()
    print("Tag the filtered words with parts of speech:\n\n", tagword)

    print("\n")
      
    descw = descendantofWords()
    print("Descendant of the filtered words:\n\n", descw)

    print("\n")
      
    s, synonym = synsets_Synonym_words()
    print("Synsets of the filtered words:\n\n", s)
    print("\n")
    print("Peer of the filtered words:\n\n", synonym)

    print("\n")
      
    h, rh = hypernymsofWords()
    print("Hypernyms of the filtered words:\n\n", h)
    print("\n")
    print("Root hypernyms of the filtered words: \n\n", rh)
    
def readFile(filepath):
    
    readline = []
    with open(filepath) as fp:
        for line in fp:
            readline.append(line.lower())
    return readline
    
def tokenizeSentences():
    lines = readFile(filepath)
    for l in lines:
        tokenWords = word_tokenize(l)
    return tokenWords
    
def filterTokenWords():
    text_tokens = tokenizeSentences()
    stop_Words = set(stopwords.words('english'))
    filtered_sentence = [word for word in text_tokens if not word in stop_Words]
    filtered_sentence = []
    for test_str in text_tokens:
        if test_str not in stop_Words:
            filtered_sentence.append(re.sub(r'[^\w\s]', '', test_str))
            res = filtered_sentence[ : 0] + [j for i, j in zip(filtered_sentence, filtered_sentence[0 : ]) if i or j]
    return res

def posTagging():
    filterData = filterTokenWords()
    tagged = nltk.pos_tag(filterData)
    
    chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP>}"""
    chunkParser = nltk.RegexpParser(chunkGram)
    
    chunked = chunkParser.parse(tagged)
    print(chunked)
    chunked.draw()
    return tagged

def descendantofWords():
        words = filterTokenWords()
        lancaster = nltk.LancasterStemmer()
        descwords = []
        for w in words:
             descwords.append(lancaster.stem(w))
        return descwords
    
def synsets_Synonym_words():
    syn_array = []
    v = []
    words = filterTokenWords()
    syns = {w: [] for w in words}
    for k, v in syns.items():
        for synset in wn.synsets(k):
            for lemma in synset.lemmas():
                syn_array.append(synset)
                v.append(lemma.name())
    return syn_array, syns
    
def hypernymsofWords():
    syns_words = synsets_Synonym_words()[0]
    hyp = []
    root_hyp = []
    for s in syns_words:
        hyp.append(s.hypernyms())
        root_hyp.append(s.root_hypernyms())
    return hyp, root_hyp
         
if __name__ == "__main__":
    main()
   
