import nltk
import numpy as np

nltk.download('punkt')

from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()

def tokenize(sentence):
    """
    Takes in a sentence and returns a list of tokens of that sentence
    Example : "I love chatbots" will be returned as ['I', 'love', 'chatbots']
    """
    return nltk.word_tokenize(sentence)

def stem(word):
    """
    Removes the the endings of similar words in an array of words
    Example : ["Organize", "Organs", "Organisms"] will be returned as ["Organ", "Organ", "Organ"]

    """
    return stemmer.stem(word.lower())


def bag_of_words(tokenized_sentence, words):
    """
    return bag of words array:
    1 for each known word that exists in the sentence, 0 otherwise
    example:
    sentence = ["hello", "how", "are", "you"]
    words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
    bog   = [  0 ,    1 ,    0 ,   1 ,    0 ,    0 ,      0]
    """
    # stem each word
    sentence_words = [stem(word) for word in tokenized_sentence]
    # initialize bag with 0 for each word
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words: 
            bag[idx] = 1

    return bag