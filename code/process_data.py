import re
import numpy as np
import pandas as pd
import map
from nltk.stem.porter import *
from nltk.corpus import wordnet
from nltk.tokenize.treebank import TreebankWordDetokenizer


def expand_contractions(sentence, contraction_mapping):
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())),
                                      flags=re.IGNORECASE|re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match)\
                                if contraction_mapping.get(match)\
                                else contraction_mapping.get(match.lower())
        expanded_contraction = first_char+expanded_contraction[1:]
        return expanded_contraction
    expanded_sentence = contractions_pattern.sub(expand_match, sentence)
    return expanded_sentence

def remove_repeated_characters(tokens):
    repeat_pattern = re.compile(r'(\w*)(\w)\2(\w*)')
    match_substitution = r'\1\2\3'
    def replace(old_word):
        if wordnet.synsets(old_word):
            return old_word
        new_word = repeat_pattern.sub(match_substitution, old_word)
        return replace(new_word) if new_word != old_word else new_word
    correct_tokens = [replace(word) for word in tokens]
    return correct_tokens

files =['data/excitement.csv', 'data/happy.csv', 'data/pleasant.csv', 'data/surprise.csv', 'data/fear.csv', 'data/angry.csv']
processed_files =['processed_data/excitement.csv', 'processed_data/happy.csv', 'processed_data/pleasant.csv', 'processed_data/surprise.csv', 'processed_data/fear.csv', 'processed_data/angry.csv']


for file, process_file in zip(files, processed_files):

    df = pd.read_csv(file, sep='\t', header=None, keep_default_na=False, na_values=[''])

    df.iloc[:,2]=[x.lower() for x in df.iloc[:,2]]
        #This method is to ensure all the words are lowercase
    df.iloc[:, 2] =[re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b','URL',g,flags=re.MULTILINE)for g in df.iloc[:, 2]]
        #This method is to remove URL

    df.iloc[:,2]=[re.sub(r'@[\w]*','',g,flags=re.MULTILINE)for g in df.iloc[:, 2]]
        # This method is to remove the @user which is useless for emotion analysis

    df.iloc[:, 2] = [expand_contractions(sentence, map.CONTRACTION_MAP) for sentence in df.iloc[:, 2]]
        #This method is to expand the word abbreviation like transform isn't into is not

    df.to_csv(process_file, sep='\t', header=['Tweet_ID', 'Created_At', 'Tweet_Text'])
    df.iloc[:, 2] = df.iloc[:, 2].str.replace("[^a-zA-Z0-9#]", " ")
        #This method is to remove the special characters, punctuations  which is useless for emotion analysis

    tokenized_tweet = df.iloc[:, 2].apply(lambda x: x.split())

    tokenized_tweet = [remove_repeated_characters(k) for k in tokenized_tweet]
    tokenized_tweet = pd.Series(tokenized_tweet)
        #This method is to remove the repeated characters like loooove and hellooooo
    # stemmer = PorterStemmer()
    # stemed_tweet = []
    # for x in tokenized_tweet:
    #     tokens = []
    #     for token in x:
    #         if token.startswith("#"):
    #             tokens.extend([token])
    #         else:
    #             tokens.append(stemmer.stem(token))
    #     stemed_tweet.append(tokens)
    # stemed_tweet=pd.Series(stemed_tweet)
        #This method is to extract the stem, which means turn plays into play, turn dying into die and avoid the hashtag being transformed

    df.iloc[:, 2]=pd.Series([TreebankWordDetokenizer().detokenize(k) for k in tokenized_tweet])
        #This is method is to combine each token in a tweet text into a sentence.

    df.to_csv(process_file, sep='\t', header= ['Tweet_ID', 'Created_At', 'Tweet_Text'])

