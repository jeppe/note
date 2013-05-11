#-*- coding:utf-8 -*-

import nltk

"""The Buddha, the Godhead, resides quite as comfortably in the circuits of a digital
computer or the gears of a cycle transmission as he does at the top of a mountain
or in the petals of a flower. To think otherwise is to demean the Buddha...which is
to demean oneself."""

text = '''Hypermethylation of the <I>TPEF/HPP1</I> Gene in Primary and
          Metastatic Colorectal Cancers,2005,0,3943,"Keywords: methylation, epigenetic, 
          metastasis, promoter, colon cancer."'''

# Used when tokenizing words

from nltk.corpus import stopwords
stopwords = stopwords.words('english')


lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.stem.porter.PorterStemmer()

#Taken from Su Nam Kim Paper...
grammar = r"""
    NBAR:
        {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
        
    NP:
        {<NBAR>}
        {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
"""

def leaves(tree):
    """Finds NP (nounphrase) leaf nodes of a chunk tree."""
    for subtree in tree.subtrees(filter = lambda t: t.node=='NP'):
        yield subtree.leaves()

def normalise(word):
    """Normalises words to lowercase and stems and lemmatizes it."""
    word = word.lower()
    word = stemmer.stem_word(word)
    word = lemmatizer.lemmatize(word)
    return word

def acceptable_word(word):
    """Checks conditions for acceptable word: length, stopword."""
    accepted = bool(2 <= len(word) <= 40
        and word.lower() not in stopwords)
    return accepted


def get_terms(tree):
    for leaf in leaves(tree):
        term = [ normalise(w) for w,t in leaf if acceptable_word(w) ]
        yield term

def tokenize(text):
    sentence_re = r'''(?x)      # set flag to allow verbose regexps
          ([A-Z])(\.[A-Z])+\.?  # abbreviations, e.g. U.S.A.
        | \w+(-\w+)*            # words with optional internal hyphens
        | \$?\d+(\.\d+)?%?      # currency and percentages, e.g. $12.40, 82%
        | \.\.\.                # ellipsis
        | [][.,;"'?():-_`]      # these are separate tokens
    '''

    chunker = nltk.RegexpParser(grammar)

    toks = nltk.regexp_tokenize(text, sentence_re)
    postoks = nltk.tag.pos_tag(toks)

    tree = chunker.parse(postoks)

    terms = get_terms(tree)
    
    tokens = [' '.join(term) for term in terms if len(term) > 0]

    tokens = list( set(tokens) )

    return tokens


