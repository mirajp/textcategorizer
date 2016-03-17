# ECE 467, NLP: Assignment 1
# Miraj Patel
# Naive Bayes Text Categorizer

from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from math import log

#By default, don't use stopwords (only use for corpus1)
useStopWords = 0
stemmer = SnowballStemmer("english")
engstopwords = stopwords.words("english")
mystopwords = {}

for i in range(0, len(engstopwords)):
    mystopwords[engstopwords[i]] = 1

# alpha = additive smoothing factor, 0 < alpha <= 1
alpha = 0.05

#Count number of times each word appears in each category
wordsCount = {}

#Count the total number of words in each category
totalCount = {}

#Keep track of vocabulary across entire training
vocab = {}
vocabSize = 0

#Count the number of documents in each category
docCount = {}
numDocuments = 0.0
testProbs = {}
trainingDocs = {}

def clean_word(input_word):
    global useStopWords
    cleaned_word = input_word.lower()
    cleaned_word = cleaned_word.replace(",", "")
    cleaned_word = cleaned_word.replace("!", "")
    cleaned_word = cleaned_word.replace("?", "")
    
    #Remove last period, but not the period in initialization token
    if cleaned_word.find(".") == len(cleaned_word)-1:
        cleaned_word = cleaned_word[:-1]

    cleaned_word = cleaned_word.replace(":", "")
    cleaned_word = cleaned_word.replace(";", "")
    cleaned_word = cleaned_word.replace("\"", "")
    cleaned_word = cleaned_word.replace("~", "")
    cleaned_word = cleaned_word.replace("`", "")
    cleaned_word = cleaned_word.replace("(", "")
    cleaned_word = cleaned_word.replace(")", "")
    cleaned_word = cleaned_word.replace("-", "")

    if useStopWords == 1:
        #Remove the 't of words like can't and haven't so they are matched to the stopwords list
        cleaned_word = cleaned_word.replace("'t", "")
     
    cleaned_word = cleaned_word.replace("\'", "")
        
    #Stem
    if len(cleaned_word) > 0 and useStopWords == 1:
        cleaned_word = stemmer.stem(cleaned_word)
    
    return cleaned_word

def trainWithDoc(fileName, category):
    global alpha, vocabSize, numDocuments
    trainingDoc = open(fileName, "rb")
    for line in trainingDoc:
        words = line.split()
        numWords = len(words)
        wordIter = 0
        while wordIter < numWords:
            foundWord = clean_word(words[wordIter])

            if len(foundWord) > 0 and foundWord not in mystopwords:
                totalCount[category] += 1
                if foundWord not in vocab:
                    vocab[foundWord] = 1
                    vocabSize += 1
                 
                if foundWord not in wordsCount[category]:
                    wordsCount[category][foundWord] = alpha + 1
                else:
                    wordsCount[category][foundWord] += 1    

            wordIter += 1

    docCount[category] += 1
    numDocuments += 1
    trainingDoc.close()
    return

def trainNaiveBayes(trainingList):
    global useStopWords
    trainingListFile = open(trainingList, "rb")
    startOfFile = trainingListFile.tell()
    firstLine = trainingListFile.readline()
    firstLine = firstLine.split()
    firstCat = firstLine[1]

    firstCat = firstCat.lower()
    #Use stopwords for only the first corpus
    if firstCat == "str" or firstCat == "pol" or firstCat == "dis" or firstCat == "cri" or firstCat == "oth":
        useStopWords = 1

    #Reset file pointer
    trainingListFile.seek(startOfFile)

    for line in trainingListFile:
        line = line.split()
        trainingDoc = line[0]
        trainingCat = line[1]
        trainingDocs[trainingDoc] = trainingCat
        #print "File: ", trainingDoc, ", cat: ", trainingCat
        if trainingCat not in wordsCount:
            #print "Adding dictionary for category:", trainingCat
            wordsCount[trainingCat] = {}
            totalCount[trainingCat] = 0.0
            testProbs[trainingCat] = 0.0
            docCount[trainingCat] = 0.0
            
        trainWithDoc(trainingDoc, trainingCat)

    trainingListFile.close()
    return

def makePrediction(fileName):
    global alpha, vocabSize, numDocuments
    prediction = ""
    testingDoc = open(fileName, "rb")
    for category in testProbs:
        testProbs[category] = 0

    for line in testingDoc:
        words = line.split()
        numWords = len(words)
        wordIter = 0
        while wordIter < numWords:
            foundWord = clean_word(words[wordIter])

            if len(foundWord) > 0 and foundWord not in mystopwords:
                for category in testProbs:
                    if foundWord in wordsCount[category]:
                        testProbs[category] += log((wordsCount[category][foundWord]/(totalCount[category] + alpha*vocabSize)))
                    else:
                        testProbs[category] += log((alpha/(totalCount[category] + alpha*vocabSize)))
                            
            wordIter += 1

    for category in testProbs:
        testProbs[category] += log((docCount[category]/numDocuments))
        
    testingDoc.close()

    maxProb = float("-inf")
    for category in testProbs:
        #print "category '", category, "' has prob", testProbs[category]
        if testProbs[category] > maxProb:
            #print "Switching prediction to", category
            prediction = category
            maxProb = testProbs[category]

    return prediction

def selectiveRetrain():
    numRepeats = 6
    while numRepeats > 5:
        numRepeats = 0
        for trainingDoc in trainingDocs:
            trueCat = trainingDocs[trainingDoc]
            predictedCat = makePrediction(trainingDoc)

            while predictedCat != trueCat:
                numRepeats += 1
                trainWithDoc(trainingDoc, trueCat)
                predictedCat = makePrediction(trainingDoc)
        
    return

def testNaiveBayes(testingList, predictionsList):
    global alpha, vocabSize, numDocuments
    testingListFile = open(testingList, "rb")
    predictionsListFile = open(predictionsList, "wb")
    for testingDocName in testingListFile:
        testingDocName = (testingDocName.split())[0]
        likelyCategory = makePrediction(testingDocName)
        predictionsListFile.write(testingDocName + " " + likelyCategory + "\n")

    testingListFile.close()
    predictionsListFile.close()
    return

trainingList = raw_input("Enter the filename of the list of training documents: ")
testingList = raw_input("Enter the filename of the list of testing documents: ")
predictionsList = raw_input("Enter the filename to save the predictions: ")
trainNaiveBayes(trainingList)
#selectiveRetrain()
testNaiveBayes(testingList, predictionsList)
exit()
