import os
import pandas as pd
from tqdm import tqdm
import jieba
import matplotlib.pyplot as plt
import re
import numpy as np
import seaborn as sns
from json_operations import sample_from_multiple_json


def basic_statistics(path_to_jsons, number_json_files, language='en', plot=True):
    '''Loop through all the json and gather statistics for the corpus.
    '''
    number_json_files = int(number_json_files)
    tot_words, tot_char, tot_size, tot_categories = get_global_counts(path_to_jsons, number_json_files, language)
    if plot:
        json_sample, tot_biographies = sample_from_multiple_json(path_to_jsons, nr_samples=50000, json_file_size=50000, total_json_files=number_json_files)
        category_counts, char_counts, word_counts = process_sample_for_plotting(json_sample, language)
        plot_word_char_histogram(char_counts, word_counts, language)
        plot_word_char_density(char_counts, word_counts, language)
        # Pronoun values need to be manully calculated, here's an example
        # plot_pronoun(feminine=240485, masculine=842644, neutral=93448, 'en')
    print_basic_statistics(json_sample, tot_biographies, tot_words, tot_char, tot_size, tot_categories, language)
    
def get_global_counts(path_to_jsons, number_json_files, language):
    tot_words = 0
    tot_chars = 0
    tot_categories = 0
    tot_size = 0
    for i in range(number_json_files):
        corpus_batch_df = pd.read_json(path_to_jsons + "_" + str(i) + ".json")
        tot_size += os.path.getsize(path_to_jsons + "_" + str(i) + ".json")
        tot_categories += corpus_batch_df["categories"].apply(len).sum()
        tot_chars += corpus_batch_df["text"].apply(len).sum()

        for i, row in corpus_batch_df.iterrows():
            # Chinese don't seperate words with spaces so jieba is required to split into words
            if (language == "zh") or (language == "chinese"):
                word_count = jieba.cut(row.text, cut_all=False)  # use jieba to split Chinese into words
                tot_words += len(list(word_count))
            else:
                word_count = re.split('\s+', row.text)  # splitting into words for non-Chinese languages
                tot_words += len(list(word_count))
    return tot_words, tot_chars, tot_size, tot_categories

def process_sample_for_plotting(json_sample, language):
    categories = json_sample['categories'].tolist()
    texts = json_sample['text'].tolist()
    category_counts = []
    word_counts = []
    char_counts = []

    for i in tqdm(range(len(json_sample))):
        category_count = len(categories[i])
        category_counts.append(category_count)

        text_i = texts[i]
        char_counts.append(len(text_i))
        
        # Chinese don't seperate words with spaces so jieba is required to split into words
        if (language == "zh") or (language == "chinese"):
            word_count = jieba.cut(text_i, cut_all=False)  # use jieba to split Chinese into words
            word_counts.append(len(list(word_count)))
        else:
            word_count = re.split('\s+', text_i)  # splitting into words for non-Chinese languages
            word_counts.append(len(word_count))

    return category_counts, char_counts, word_counts


def plot_word_char_histogram(char_counts, word_counts, language):
    '''Figure 1 (a) : Histogram of averaged number of characters/words per biography
    '''
    mean_nr_words = np.mean(word_counts)
    std_nr_words = round(np.std(word_counts), 2)
    mean_nr_char = np.mean(char_counts)
    std_nr_char = round(np.std(char_counts), 2)
    
    plt.figure(figsize=(10, 8), dpi=200)
    ax = plt.axes()
    plt.grid(axis='y', c='#d2c9eb', linestyle='--', zorder=0)
    width = 0.1
    position = 0.1  # number of corpus compared here

    plt.bar(position, mean_nr_words, yerr=(std_nr_words / 2), width=width, label='mean_nr_words', color='salmon',
            edgecolor='#d2c9eb',
            linewidth=0.5)
    plt.bar(position + width, mean_nr_char, yerr=(std_nr_char / 2), width=width, label='mean_nr_chars',
            color='lightblue',
            edgecolor='#d2c9eb', linewidth=0.5)

    plt.text(position, mean_nr_words, '%.2f' % mean_nr_words, va='baseline', ha='right', color='black', fontsize=19)
    plt.text(position + width, mean_nr_char, '%.2f' % mean_nr_char, va='baseline', ha='left', color='black',
             fontsize=19)

    plt.legend(prop={'family': 'Times New Roman', 'size': 20}, ncol=1)
    plt.xticks([])
    plt.xlim(0, 0.3)
    plt.yticks(fontproperties='Times New Roman', fontsize=12, color='black')
    plt.xlabel(language, fontproperties='Times New Roman', fontsize=25)
    plt.ylabel('Averaged Number', fontproperties='Times New Roman', fontsize=25)
    plt.title('Histogram of averaged number of characters/words per text', fontproperties='Times New Roman',
              fontsize=25)
    plt.show()
    return None


def plot_word_char_density(nr_char, nr_words, language):
    '''Figure 1 (b): Histogram and Density Plot for Number of Characters/Words
    '''
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 5), dpi=200)
    sns.histplot(nr_char, kde=True, stat='count', color='salmon', ax=ax1, line_kws={'lw': 2},
                 kde_kws={'clip': (0, 5000)})
    ax1.set_xlim([0, 5000])
    ax1.set_xlabel(f'Number of Characters of {language} Biography', fontproperties='Times New Roman', fontsize=20)
    ax1.set_ylabel('Number of Biographies', fontproperties='Times New Roman', fontsize=20)
    ax1.set_title('Histogram and Density Plot for Number of Characters')

    sns.histplot(nr_words, kde=True, stat='count', color='salmon', ax=ax2, line_kws={'lw': 2},
                 kde_kws={'clip': (0, 1000)})
    ax2.set_xlim([0, 1000])
    ax2.set_xlabel(f'Number of Words of {language} Biography', fontproperties='Times New Roman', fontsize=20)
    ax2.set_ylabel('Number of Biographies', fontproperties='Times New Roman', fontsize=20)
    ax2.set_title('Histogram and Density Plot for Number of Words')

    plt.subplots_adjust(wspace=0.3)

    plt.show()
    return None


def plot_pronoun(feminine, masculine, neutral, language):
    '''Histogram of pronoun frequency
    Need to feed in numbers of gendered terms as input
    '''
    plt.figure(figsize=(10, 7), dpi=200)
    ax = plt.axes()
    plt.grid(axis='y', c='#d2c9eb', linestyle='--', zorder=0)
    position = 0.2

    plt.bar(position, height=masculine, color='salmon', label='Masculine Pronouns', width=0.1)
    plt.bar(position, height=feminine, bottom=masculine, color='lightblue', label='Feminine Pronouns', width=0.1)
    plt.bar(position, height=neutral, bottom=masculine + feminine, color='grey', label='Neutral/Nonbinary Pronouns',
            width=0.1)

    cols = ['feminine', 'masculine', 'neutral']
    sum = feminine + masculine + neutral
    percentages = [(feminine / sum), (masculine / sum), (neutral / sum)]
    percents = ['{:.2%}'.format(p) for p in percentages]

    plt.text(position, feminine / 2 + masculine, percents[0], ha='center', va='center', color='black', fontsize=19)
    plt.text(position, masculine / 2, percents[1], ha='center', va='center', color='black', fontsize=19)
    plt.text(position, neutral / 2 + feminine + masculine, percents[2], ha='center', va='bottom', color='black',
             fontsize=19)

    plt.legend(prop={'family': 'Times New Roman', 'size': 20}, ncol=1, loc='lower right')
    plt.xticks([])
    plt.xlim(0, 0.4)
    plt.yticks(fontsize=12)
    plt.xlabel(language, fontproperties='Times New Roman', fontsize=25)
    plt.ylabel('Pronoun Frequency', fontproperties='Times New Roman', fontsize=25)
    plt.ticklabel_format(axis='y', style='plain')
    plt.title('Histogram of pronoun frequency', fontproperties='Times New Roman',
              fontsize=25)
    plt.show()

    return None


def print_basic_statistics(json_sample, tot_biographies, tot_words, tot_char, tot_size, tot_categories, language):
    '''Print the statistics.
    '''
    pd.set_option('display.max_columns', None)
    print(f"A sample of the corpus: \n {json_sample[:5]}\n")
    print("BASIC STATISTICS FOR ", language, ' BIOGRAPHIES.')
    print(f"Total nr of biographies: {tot_biographies}")
    print(f"Total size of the data: {tot_size}")
    print(f"Total number of words: {tot_words}")
    print(f"Total number of chars: {tot_char}")
    print(f"Total number of categories: {tot_categories}")
    print(f"Average number of words per biography: {tot_words/tot_biographies}")
    print(f"Average number of characters per biography: {tot_char/tot_biographies}")
    print(f"Average number of categories per biography: {tot_categories/tot_biographies}")


# basic_statistics('./english_sample_long.json', 'en')

