# source data: http://archive.ics.uci.edu/ml/datasets/Sentiment+Labelled+Sentences

with open('C:/Scripts/Python/DataScience/sentLabSent/imdb_labelled.txt','r') as text_file:
    lines = text_file.read().split('\n')
with open('C:/Scripts/Python/DataScience/sentLabSent/amazon_cells_labelled.txt','r') as text_file:
    lines = text_file.read().split('\n')
with open('C:/Scripts/Python/DataScience/sentLabSent/yelp_labelled.txt','r') as text_file:
    lines = text_file.read().split('\n')

# lines = [line.split('\t') for line in lines if len(line.split('\t')) == 2 and line.split('\t')[1] <> '']



lines = for line in lines:
             if len(line.split('\t')) == 2 and line.split('\t')[1] <> '':
                 line.split('\t')


print(lines)
