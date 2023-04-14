from nltk.corpus import treebank

t = treebank.parsed_sents('wsj_001.mrg')[0]
t.draw()
