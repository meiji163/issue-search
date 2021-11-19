import gensim
from gensim.corpora import Dictionary
from gensim.models import Word2Vec, Phrases
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.similarities import Similarity
import numpy as np

from .utils import *

from typing import List, Dict
Docs = List[List[str]]

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')

STOP_WORDS = set(stopwords.words('english'))
QUOTES = {'""',"'","''",'`','``','```'}
PUNCT = '!"#$%&\'()*+,./;<=>?@[\\]^_`{|}~ ' #keep '-' for flags and ':' for emojis

def tokenize(s: str) -> List[str]:
    tok = [ t.strip().lower() for t in word_tokenize(s)]
    def is_token(s):
        return len(s)>1 and len(s)<12 \
            and s not in STOP_WORDS\
            and s not in QUOTES
    tok = filter(is_token, tok)
    return list(tok)

def add_ngrams(issues: Docs, min_count=10) -> None:
    bigram = Phrases(issues, min_count=min_count)
    for idx in range(len(issues)):
        for token in bigram[issues[idx]]:
            if '_' in token:
                issues[idx].append(token)

def issue2vec(issues: Docs) -> Doc2Vec:
    ''' Train Doc2Vec on list of tokenized issues '''
    docs = [tokenize(content(iss)) for iss in issues]
    w2v = Word2Vec(
            docs, 
            vector_size=100,
            min_count=2,
            workers=4,
        )

    tagged_docs = [ TaggedDocument(docs[i], [i]) for i in range(len(docs)) ]

    d2v = Doc2Vec(vector_size=120, min_count=2, epochs=40)
    d2v.build_vocab(tagged_docs)
    d2v.train(tagged_docs, total_examples=d2v.corpus_count, epochs=d2v.epochs)
    return d2v

def normalize(vecs: np.ndarray) -> np.ndarray:
    '''Normalize batch of vectors (B x D np array)'''
    norms = np.linalg.norm(vecs, axis=1)
    return vecs / norms[:,None]

