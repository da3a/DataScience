from nltk.corpus import wordnet

syns = wordnet.synsets('program')

#print(syns)

synonyms =[]
antonyms = []


for syn in wordnet.synsets('protection'):
    for l in syn.lemmas():
  #      print(l)
        synonyms.append(l.name())
        if l.antonyms():
            for a in l.antonyms():
                antonyms.append(a.name())

# print(synonyms)
# print(antonyms)


w1 = wordnet.synset('protective_covering.n.01')
for l in w1.lemmas():
     print(l.)

