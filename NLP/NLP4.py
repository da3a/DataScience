import nltk
#nltk.download()
text = "Mary had a little lamb. Her fleece was white as snow. little lamb was small."
#sentence tokenization
from nltk.tokenize import word_tokenize, sent_tokenize
sents=sent_tokenize(text)
print(sents)
#word tokenization
words=[word_tokenize(sent) for sent in sents]
print(words)
#remove stopwords
from nltk.corpus import stopwords
from string import punctuation
customStopWords=set(stopwords.words('english') + list(punctuation))
wordWOStopwords = [word for word in word_tokenize(text) if word not in customStopWords]
print(wordWOStopwords)

#find bigrams
from nltk.collocations import *
bigram_measures = nltk.collocations.BigramAssocMeasures()
finder = BigramCollocationFinder.from_words(wordWOStopwords)
print(sorted(finder.ngram_fd.items()))

#stemming
text2 = "Mary closed on closing night when she was in the mood top close."
from nltk.stem.lancaster import LancasterStemmer
st=LancasterStemmer()
stemmedWords=[st.stem(word) for word in word_tokenize(text2)]
print(stemmedWords)

#part of speech tag
print(nltk.pos_tag(word_tokenize(text2)))

#word sense disambiguation - helps understanding meaning
from nltk.corpus import wordnet as wn
for ss in wn.synsets('bass'):
    print(ss, ss.definition())

from nltk.wsd import lesk
#sensel = lesk(word_tokenize('Sing in a lower tone, along with the bass'), 'bass')
sensel = lesk(word_tokenize('This sea bass was really hard to catch'), 'bass')
print(sensel,sensel.definition())
