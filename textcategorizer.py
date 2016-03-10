# ECE 467, NLP: Assignment 1
# Miraj Patel
# Naive Bayes Text Categorizer

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.tag import _pos_tag as postagger
from nltk.tag.perceptron import PerceptronTagger

tagset = None
tagger = PerceptronTagger()
lemmatizer = WordNetLemmatizer()
# Use lemmatization as opposed to stemming to group words by meaning

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def clean_word(input_word):
    cleaned_word = input_word.replace(",", "")
    cleaned_word = cleaned_word.replace("!", "")
    cleaned_word = cleaned_word.replace("?", "")
    #Remove last period, but not the period in initialization token
    #cleaned_word = cleaned_word.replace(".", "")
    if cleaned_word.find('.') == len(cleaned_word)-1:
        cleaned_word = cleaned_word[:-1]

    cleaned_word = cleaned_word.replace(":", "")
    cleaned_word = cleaned_word.replace(";", "")
    cleaned_word = cleaned_word.replace("\"", "")
    cleaned_word = cleaned_word.replace("\'", "")
    cleaned_word = cleaned_word.replace("~", "")
    cleaned_word = cleaned_word.replace("`", "")
    cleaned_word = cleaned_word.replace("(", "")
    cleaned_word = cleaned_word.replace(")", "")
    cleaned_word = cleaned_word.replace("-", "")

    if len(cleaned_word) > 0:
        #print "word =", cleaned_word
        #posTag = (nltk.tag._pos_tag([cleaned_word], tagset, tagger))[0][1]
        posTag = (postagger([cleaned_word], tagset, tagger))[0][1]
        #print posTag
        #posTag = (tagger.tag([cleaned_word]))[0][1]
        posTag = get_wordnet_pos(posTag)
        #print "pos =", posTag
        cleaned_word = (lemmatizer.lemmatize(cleaned_word, posTag)).lower()
        #print "Changed from", words[wordIter], "to", cleaned_word

    return cleaned_word

trainingList = raw_input('Enter the filename of the list of training documents: ')
testingList = raw_input('Enter the filename of the list of testing documents: ')

# alpha = additive smoothing factor, 0 < alpha <= 1
alpha = 1
catWords = {}
catCounts = {}

trainingList = open(trainingList, "rb")
for line in trainingList:
    line = line.split()
    trainingDoc = line[0]
    trainingCat = line[1]
    print "File: ", trainingDoc, ", cat: ", trainingCat
    if trainingCat not in catWords:
        print "Adding dictionary for category:", trainingCat
        catWords[trainingCat] = {}
        catCounts[trainingCat] = 0
    
    trainingDoc = open(trainingDoc, "rb")
    for line in trainingDoc:
        words = line.split()
        numWords = len(words)
        wordIter = 0
        while wordIter < numWords:
            #Turns out capitalization affects POS tag
            #cleaned_word = (words[wordIter]).lower()
            foundWord = clean_word(words[wordIter])
            
            if len(foundWord) > 0:
                if foundWord not in catWords[trainingCat]:
                  catWords[trainingCat][foundWord] = alpha
                  catCounts[trainingCat] += alpha
                
                catWords[trainingCat][foundWord] += 1
                catCounts[trainingCat] += 1
            
            wordIter += 1

    trainingDoc.close()

trainingList.close()


for category in catCounts:
  print category, "dictionary has", catCounts[category], "total words"
  #for uniqueword in catWords[category]:
    #print "\t", uniqueword, "appears", catWords[category][uniqueword], "times"

testingList = open(testingList, "rb")
for testingDoc in testingList:
    testingDoc = (testingDoc.split())[0]
    print "File: ", testingDoc
    testingDoc = open(testingDoc, "rb")
    testingDoc.close()

testingList.close()
