# ECE 467, NLP: Assignment 1
# Miraj Patel
# Naive Bayes Text Categorizer

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

# Use lemmatization as opposed to stemming to group words by meaning

trainingList = raw_input('Enter the filename of the list of training documents: ')
#testingList = raw_input('Enter the filename of the list of testing documents: ')

trainingList = open(trainingList, "rb")
#testingList = open(testingList, "rb")

# alpha = additive smoothing factor, 0 < alpha <= 1
alpha = 1
catWords = {}
catCounts = {}

count = 1
for line in trainingList:
    line = line.split()
    trainingDoc = line[0]
    trainingCat = line[1]
    print "Line #", count, ", file: ", trainingDoc, ", cat: ", trainingCat
    if trainingCat not in catWords:
        print "Adding dictionary for category:", trainingCat
        catWords[trainingCat] = {}
        catCounts[trainingCat] = 0
    
    trainingDoc = open(trainingDoc, "rb")
    wordCount = 1
    for line in trainingDoc:
        words = line.split()
        numWords = len(words)
        wordIter = 0
        while wordIter < numWords:
            foundWord = (words[wordIter]).lower()
            foundWord = foundWord.replace(",", "")
            foundWord = foundWord.replace("!", "")
            foundWord = foundWord.replace("?", "")
            foundWord = foundWord.replace(".", "")
            foundWord = foundWord.replace(":", "")
            foundWord = foundWord.replace(";", "")
            foundWord = foundWord.replace("\"", "")
            foundWord = foundWord.replace("\'", "")
            foundWord = foundWord.replace("~", "")
            foundWord = foundWord.replace("`", "")
            foundWord = foundWord.replace("(", "")
            foundWord = foundWord.replace(")", "")
            foundWord = foundWord.replace("-", "")
            
            foundWord = lemmatizer.lemmatize(foundWord)
            print "Changed from", words[wordIter], "to", foundWord
            if len(foundWord) > 0:
                if foundWord not in catWords[trainingCat]:
                  catWords[trainingCat][foundWord] = alpha
                  catCounts[trainingCat] += alpha
                
                catWords[trainingCat][foundWord] += 1
                catCounts[trainingCat] += 1
                
                #print "Word #", wordCount, foundWord
                wordCount += 1
                
            wordIter += 1
    
    count += 1
    if count > 1:
        break

for key in catCounts:
  print key, "dictionary has", catCounts[key], "words"

trainingList.close()
#testingList.close()
