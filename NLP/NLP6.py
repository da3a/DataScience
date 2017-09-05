import nltk, re, pprint

text = "This my example document. Not a very interesting piece of text. It is composed of three sentences. That's it!"

def ie_preprocess(document):
    sentences = nltk.sent_tokenize(document)
    print(sentences) # list of sentences 
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    print(sentences) #list of list of words
    sentences = [nltk.pos_tag(sent) for sent in sentences ] #list of list of tuples (word and POS (Part of Speech))
    print(sentences)

#ie_preprocess(text)


def extract_np(psent):
  for subtree in psent.subtrees():
    if subtree.label() == 'NP':
      yield ' '.join(word for word, tag in subtree.leaves())


from nltk.corpus import stopwords
stopwords = stopwords.words('english')

sentence = [("the", "DT"), ("little", "JJ"), ("yellow", "JJ"), ("dog", "NN"), ("barked", "VBD"), ("at", "IN"),  ("the", "DT"), ("cat", "NN")]

#an NP chunk should be formed whenever the chunker finds an optional determiner (DT) followed by any number of adjectives (JJ) and then a noun (NN)
grammar = 'NP: {<DT>?<JJ>*<NN>}'
cp = nltk.RegexpParser(grammar)
result = cp.parse(sentence)

for npstr in extract_np(result):
    print(npstr)