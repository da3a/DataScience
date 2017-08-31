# Chinking is a part of the chunking process with natural language processing with NLTK. A chink is what we wish to remove from the chunk. We define a chink in a very similar fashion compared to how we defined the chunk. 

import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer

train_text =  state_union.raw("2005-GWBush.txt")
#sample_text = state_union.raw("2006-GWBush.txt")

custom_sent_tokenizer = PunktSentenceTokenizer(train_text)

sample_text = "The sun sat high in the sky. It ws a hot day, a day like no other. This was going to be day that Derek chose to make the big change." 
tokenized = custom_sent_tokenizer.tokenize(sample_text)

def process_content():
    for i in tokenized:
        words = nltk.word_tokenize(i)
        tagged = nltk.pos_tag(words)

        chunkGram = r"""Chunk: {<.*>+}
                        }<VB.?|IN|DT|>+{"""

        chunkParser = nltk.RegexpParser(chunkGram)
        chunked = chunkParser.parse(tagged)

        chunked.draw()


process_content()
