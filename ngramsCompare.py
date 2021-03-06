# ngrams.py
# James Yang
# program used to generate n-gram counts for the data of #metoo posts
# some of the methods originally written by Eric Alexander and modified

import csv
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


''' Function takes in a given text filename and counts one-grams in the file '''
def getOneGrams(reader):
    oneGramCounts = {}
    for row in reader:
        line = row['status_message']

        # Clean out punctuation
        for ch in '!@#$%^&*()_+-=;:",./<>?\\':
            line = line.replace(ch, ' ')
    
        # Reduce to all lowercase
        line = line.lower()
        
        # Split into words
        words = line.split()

        # Get stopwords
        with open("stopwords.txt") as f:
            stopwords = [word for line in f for word in line.split()]

        # Add to oneGramCounts for each word
        for word in words:
            if word not in stopwords:
                oneGramCounts[word] = oneGramCounts.get(word, 0) + 1

    return oneGramCounts

def getTwoGrams(reader):
    ''' Function takes in a given text filename and returns 2-grams for the given text '''
    twoGramCounts = {}
    #reader = csv.DictReader(filename, delimiter = ',')
    for row in reader:
        line = row['status_message']
        # Clean out punctuation
        for ch in '!@#$%^&*()_+-=;:",./<>?\\':
            line = line.replace(ch, ' ')
        
        while '  ' in line:
            line = line.replace('  ', ' ')
        
        # Reduce to all lowercase
        line = line.lower()
        
        # Split into words
        words = line.split()
        
        '''
        # Take care of numbers
        data = nltk.pos_tag(words)

        
        for i in range(len(data)):
            if 'CD' in data[i][1]:
                words[i] = 'num'
        '''
        # Get stopwords
        with open("stopwords.txt") as f:
            stopwords = [word for line in f for word in line.split()]

        # Add to twoGramCounts for each word
        i = 0
        for i in range(len(words) - 1):
            # the case when phrases with both stopwords are excluded
            # if not (words[i] in stopwords and words[i+1] in stopwords):

            # the case when only phrases with both non-stopwords are included
            if words[i] not in stopwords and words[i+1] not in stopwords:
                word = words[i] + ' ' + words[i+1]
                twoGramCounts[word] = twoGramCounts.get(word, 0) + 1

    return twoGramCounts

def getNGrams(reader, n):
    nGramCounts = {}
    for row in reader:

        line = row['status_message']

        # Clean out punctuation
        for ch in '!@#$%^&*()_+-=;:",./<>?\\':
            line = line.replace(ch, ' ')
        
        while '  ' in line:
            line = line.replace('  ', ' ')
        
        # Reduce to all lowercase
        line = line.lower()
        
        # Split into words
        words = line.split()

        '''
        # Take care of numbers
        data = nltk.pos_tag(words)

        for i in range(len(data)):
            if 'CD' in data[i][1]:
                words[i] = 'num'
            # if words[i] in stopwords:
                # words.remove(words[i])
        '''
        
        # Add to twoGramCounts for each word
        i = 0
        for i in range(len(words) - n + 1):
            sublist = words[i:i+n]
            j = 0
            word = ''
            for j in range(len(sublist)):
                word += sublist[j] + ' '
            nGramCounts[word] = nGramCounts.get(word, 0) + 1

    return nGramCounts

def main():
    myfile = open("3gramsData.csv",'w')
    writer = csv.writer(myfile)
    writer.writerow(["word", "count", "dataset"])

    n = int(input("How many grams? "))
    display = int(input("How many to display? "))
    files = ["136598840398995_facebook_statuses.csv", "amazonReviewSnippets_GroundTruth.csv", "movieReviewSnippets_GroundTruth.csv", 
             "nytEditorialSnippets_GroundTruth.csv", "tweets_GroundTruth.csv"]
    names = ["metoo", "amazon", "movies", "nyt", "tweets"]
    for i in range(len(files)):
        file = open(files[i])
        reader = csv.DictReader(file, delimiter = ',')

        if n == 1:
            nGrams = getOneGrams(reader)
        elif n == 2:
            nGrams = getTwoGrams(reader)
        else: 
            nGrams = getNGrams(reader, n)

        for key, val in nGrams.items():
            writer.writerow([key, val, names[i]])

if __name__ == '__main__':
    main()