#!/usr/bin/python

import nltk
import csv
import sys
import pickle
import os
import time

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from pathlib import Path
from imp import reload

reload(sys)
sys.setdefaultencoding('utf-8')

# Define some vars
classifier = []
word_features = []
start_time = ""

# Define pickle directory name
pickle_directory_name = "pickles/"

# Define our dataset name
dataset = "dataset/dataset.csv"

# Data preprocessing, our very first step
def preprocess(filename):

    global word_features
    global start_time
    content = []
    category = []
    token = {}
    new_token = []

    # Begin counting process time
    start_time = time.time()

    # Tokenize and remove all punctuation
    tokenizer = RegexpTokenizer(r'\w+')

    print("-- Begin preprocessing. This could take some time. ---")

    # Read the dataset
    for d in csv.DictReader(open(filename), delimiter=','):

        # Read the CSV column (see the dataset structure for more detail)
        line_content = str(d['content'])
        cat_content = str(d['category'])

        content.append(line_content)
        category.append(cat_content)

    print("Creating news token..")
    for i in range(len(content)):

        # Tokenize the document, line by line
        token[i] = tokenizer.tokenize(content[i])

        # Remove the stopwords
        token[i] = [word for word in token[i] if word not in stopwords.words('english')]

        # Save into new variable
        # new_token = (['this', 'is', 'an', 'example', 'of', 'an', 'article'], 'our label')
        new_token.append((token[i], category[i]))

        # print ("Appending token from news no. %i" % (i+1))


    print("Creating word features..")
    # Create the word_features. Read NLTK documentation about features.
    word_features = get_word_features(get_words_in_token(new_token))

    # Save to pickle file
    save_pickle("word_features", word_features)

    # Prepare the training data
    print("Creating training data..")
    training_set = nltk.classify.apply_features(extract_features, new_token)

    # Call the training method
    train(training_set)

# Part of word_feature
def get_words_in_token(token):
    all_words = []
    for (words, sentiment) in token:
        all_words.extend(words)
    return all_words

# Part of word_feature
def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

# Extract the feature from text document
def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

# This is where the training begin
def train(training_set):
    global classifier
    global start_time

    # Train the system and save the training result into 'classifier' variable
    print("Training classifier..")
    classifier = nltk.NaiveBayesClassifier.train(training_set)

    # Save pickle so we don't have to retrain everytime we run the system
    save_pickle("classifier", classifier)
    print("Training done!")
    process_time(start_time)

# This is where you try to classify/predict news from your input
def classify(text):

    global classifier
    global word_features
    global start_time

    start_time = time.time()

    # Classify our input article/text and save the label into 'label' variable
    label = classifier.classify(extract_features(text.split()))

    print("Labelled news = %s" % label)
    process_time(start_time)
    # news = raw_input("News = ")
    # classify(news)
    return label

# Method to save pickle into your hard drive
def save_pickle(name, vars):
    if Path(pickle_directory_name).is_dir() == False:
        os.makedirs(pickle_directory_name)
    save_pickle = open("%s%s.pickle" % (pickle_directory_name, name), "wb")
    pickle.dump(vars, save_pickle)
    save_pickle.close()

# Method to count process time. You can call it anywhere.
def process_time(start_time):
    process = time.strftime('%H:%M:%S', time.gmtime((time.time() - start_time)))
    print("Process done in %s" % process)

# Load all resources needed in this system
def load_resources():
    global word_features
    global classifier

    start_time = time.time()
    print("Loading resources..")

    # Load the word_features from pickle file
    word_features = pickle.load(open("%sword_features.pickle" % pickle_directory_name, "rb"))

    # Load our trained system from pickle file
    classifier = pickle.load(open("%sclassifier.pickle" % pickle_directory_name, "rb"))

    print("Resources loaded.")
    process_time(start_time)

# This is where the system decide to train your system or directly classify your text
if __name__ == '__main__':
    if Path(pickle_directory_name).is_dir():
        load_resources()
        # news = raw_input("News = ")
        # classify(news)
    else:
        preprocess(dataset)
