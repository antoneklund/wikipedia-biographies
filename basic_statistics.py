import pandas as pd
from tqdm import tqdm
import jieba
import matplotlib.pyplot as plt
import re
import numpy as np
import seaborn as sns


def basic_statistics(path_to_jsons, language="en"):
    '''Loop through all the json and gather statistics for the corpus.
    YOU CAN CHANGE THIS FREELY BUT I JUST MADE SOME SORT OF STRUCTURE.
    '''
    print("BASIC STATISTICS")
    json_sample, total_nr_biographies, total_nr_char, total_nr_words, corpus_size = process_all_json(path_to_jsons, language)
    plot_word_distribution(json_sample, language)
    plot_char_distribution(json_sample, language)
    plot_pronoun(json_sample, language)
    print_basic_statistics(total_nr_biographies, total_nr_char, total_nr_words, corpus_size)
    
    
def process_all_json(path_to_jsons, language):
    '''Loop through all the json and gather statistics for the corpus.
    '''
    return None


def plot_word_distribution(json_sample, language):
    '''Jingwen function
    '''
    return None

def plot_char_distribution(json_sample, language):
    '''Jingwen function
    '''
    return None

def plot_pronoun(json_sample, language):
    '''Jingwen function
    '''
    return None

def print_basic_statistics(total_nr_biographies, total_nr_char, total_nr_words, corpus_size):
    '''Print the statistics.
    '''
    print(f"Total nr of biographies: {total_nr_biographies}")
    print(f"Total nr characters: {total_nr_char}")
    print(f"Total nr words: {total_nr_words}")
    print(f"Average number of characters per biography: {total_nr_char/total_nr_biographies}")
    print(f"Average number of words per biography: {total_nr_words/total_nr_biographies}")
    ### Add more here 
