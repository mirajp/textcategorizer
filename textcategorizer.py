# ECE 467, NLP: Assignment 1
# Miraj Patel
# Naive Bayes Text Categorizer

from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tag import _pos_tag as postagger
from nltk.tag.perceptron import PerceptronTagger
from math import log

tagset = None
tagger = PerceptronTagger()
lemmatizer = WordNetLemmatizer()
stemmer = SnowballStemmer("english")
# Use lemmatization as opposed to stemming to group words by meaning

# alpha = additive smoothing factor, 0 < alpha <= 1
alpha = 1.0
#Count number of times each word appears in each category
wordsCount = {}
#Count the total number of words in each category
totalCount = {}
#Count the number of documents in each category
docCount = {}
numDocuments = 0.0
testProbs = {}

trainingList = raw_input('Enter the filename of the list of training documents: ')
testingList = raw_input('Enter the filename of the list of testing documents: ')
predictionsList = raw_input('Enter the filename to save the predictions: ')
print "\n"

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

    #Stem
    if len(cleaned_word) > 0:
        cleaned_word = stemmer.stem(cleaned_word)

    """
    #Lemmatize
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
    """

    return cleaned_word

trainingList = open(trainingList, "rb")
for line in trainingList:
    line = line.split()
    trainingDoc = line[0]
    trainingCat = line[1]
    #print "File: ", trainingDoc, ", cat: ", trainingCat
    if trainingCat not in wordsCount:
        #print "Adding dictionary for category:", trainingCat
        wordsCount[trainingCat] = {}
        totalCount[trainingCat] = 0.0
        testProbs[trainingCat] = 0.0
        docCount[trainingCat] = 0.0
    
    trainingDoc = open(trainingDoc, "rb")
    for line in trainingDoc:
        words = line.split()
        numWords = len(words)
        wordIter = 0
        while wordIter < numWords:
            #Turns out capitalization affects POS tag
            #cleaned_word = (words[wordIter]).lower()
            foundWord = clean_word(words[wordIter])
            
            if len(foundWord) > 0 and foundWord not in stopwords.words('english'):
                if foundWord not in wordsCount[trainingCat]:
                  wordsCount[trainingCat][foundWord] = alpha
                  totalCount[trainingCat] += alpha
                
                wordsCount[trainingCat][foundWord] += 1
                totalCount[trainingCat] += 1
            
            wordIter += 1

    docCount[trainingCat] += 1
    numDocuments += 1
    trainingDoc.close()
    if numDocuments > 100:
        break

trainingList.close()


for category in totalCount:
    print "Printing category:", category
    for uniqueword in wordsCount[category]:
        print "\t", category, "--", uniqueword, ":", wordsCount[category][uniqueword], "/", totalCount[category]
    print "\n\n"


testingList = open(testingList, "rb")
predictionsList = open(predictionsList, "wb")
for testingDocName in testingList:
    testingDocName = (testingDocName.split())[0]
    #print "File: ", testingDoc
    testingDoc = open(testingDocName, "rb")
    for category in totalCount:
        testProbs[category] = 0

    for line in testingDoc:
        words = line.split()
        numWords = len(words)
        wordIter = 0
        while wordIter < numWords:
            #Turns out capitalization affects POS tag
            #cleaned_word = (words[wordIter]).lower()
            foundWord = clean_word(words[wordIter])
            
            for category in wordsCount:
                if foundWord in wordsCount[category]:
                    #print "Numerator:", (wordsCount[category][foundWord])
                    #print "Denominator:", (totalCount[category])
                    #print "Fraction:", float(wordsCount[category][foundWord])/float(totalCount[category])
                    
                    testProbs[category] += log(float(wordsCount[category][foundWord]/totalCount[category]))
                    #testProbs[category] *= (float(wordsCount[category][foundWord]/totalCount[category]))
                else:
                    testProbs[category] += log(float(alpha/totalCount[category]))
                    #testProbs[category] *= (float(alpha/totalCount[category]))

            wordIter += 1

    for category in wordsCount:
        print "category '", category, "' prob:", float(docCount[category]/numDocuments), "logval =", log(float(docCount[category]/numDocuments)) 
        print "word log sum prob =", testProbs[category]
        testProbs[category] += log(float(docCount[category]/numDocuments))
        #testProbs[category] *= (float(docCount[category]/numDocuments))
        print "new prob =", testProbs[category]

    testingDoc.close()
    maxProb = float("-inf")
    likelyCategory = ""

    for category in testProbs:
        print "category '", category, "' has prob", testProbs[category]
        if testProbs[category] > maxProb:
            print "Switching prediction to", category
            likelyCategory = category
            maxProb = testProbs[category]
        
    predictionsList.write(testingDocName + " " + likelyCategory + '\n')

predictionsList.close()
testingList.close()
