import nltk

#http://www.nltk.org/data.html
nltk.download()
text = "Mary had a little lamb. Its Fleece was white as snow."

#step 1 tokenization 
from nltk.tokenize import word_tokenize, sent_tokenize

sents = sent_tokenize(text)
#print(sents)
words = [word_tokenize(sent) for sent in sents]
print(words)

#step 2 remove stopwords
 
from nltk.corpus import stopwords
from string import punctuation

customStopWords=set(stopwords.words('english')+list(punctuation))

wordsWOStopWords = [word for word in word_tokenize(text) if word not in customStopWords ]

print(wordsWOStopWords)

#handle Bigrams
from nltk.collocations import *

bigram_measures = nltk.collocations.BigramAssocMeasures()
finder = BigramCollocationFinder.from_words(wordsWOStopWords)

s = sorted(finder.ngram_fd.items())

print(s)

#Stemming 

text2 = "mary closed on closing night. When she was in the mood to close."

from nltk.stem.lancaster import LancasterStemmer
st = LancasterStemmer()
stemmedWords=[st.stem(word) for word in word_tokenize(text2)]
print(stemmedWords)

result = nltk.pos_tag(word_tokenize(text2))
print(result)

#word sense disambiguation

from nltk.corpus import wordnet as wn

for ss in wn.synsets('bass'):   
    print(ss, ss.definition())

from nltk.wsd import lesk

sense1 = lesk(word_tokenize('sing in a lower tone along with the bass'),'bass')
print(sense1, sense1.definition())
sense2 = lesk(word_tokenize('the bass is a fish that swims in the deepest part of the ocean'),'bass')
print(sense2,sense2.definition())