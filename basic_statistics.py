import pandas as pd
from tqdm import tqdm
import jieba
import matplotlib.pyplot as plt
import re
import numpy as np
import seaborn as sns


def basic_statistics(path_to_jsons, language='en'):
    '''Loop through all the json and gather statistics for the corpus.
    '''
    print("BASIC STATISTICS FOR ", language, ' BIOGRAPHIES.')
    json_sample, total_nr_biographies, mean_nr_categories, \
    nr_char, mean_nr_char, std_nr_char, nr_words, \
    mean_nr_words, std_nr_words = process_all_json(path_to_jsons, language_is_Chinese=False)
    plot_word_char_histogram(mean_nr_char, std_nr_char, mean_nr_words, std_nr_words, language)
    plot_word_char_density(nr_char, nr_words, language)
    # Pronoun values are manully calculated, here's an example
    # plot_pronoun(240485, 842644, 93448, 'en')
    print_basic_statistics(json_sample, total_nr_biographies, mean_nr_categories, mean_nr_char, mean_nr_words)


def process_all_json(path_to_jsons, language_is_Chinese=False):
    '''Loop through all the json and gather statistics for the corpus.
    :param data_is_Chinese: Defult setting is False, if it is Chinese, then use jieba to make Chinese into words
    '''

    json_sample = pd.read_json(path_to_jsons)
    total_nr_biographies = len(json_sample)

    # calculate the number of categories for the corpus (shown in table 1)
    # calculate the averaged length of the main texts of each biographies for the corpus, both in characters and words
    # (shown in table 1 and used for generating figures later)
    categories = json_sample['categories'].tolist()
    texts = json_sample['text'].tolist()
    nr_categories = []
    nr_words = []
    nr_char = []

    for i in tqdm(range(len(json_sample))):
        nr_categories_i = len(categories[i])
        nr_categories.append(nr_categories_i)

        text_i = texts[i]
        nr_char.append(len(text_i))  # same for all languages to calculate the number of charactors of each text

        # Chinese doesn't have spaces to seperate the words, so sometimes one character in Chinese can mean a single word
        if not language_is_Chinese:
            text_words = re.split('\s+', text_i)  # seperating words by spaces for languages which are not Chinese
            nr_words.append(len(text_words))
        else:
            text_words = jieba.cut(text_i,
                                   cut_all=False)  # use jieba to cut Chinese into words, cutting mode can be different
            nr_words.append(len(list(text_words)))

    mean_nr_categories = np.mean(nr_categories)
    std_nr_categories = round(np.std(nr_categories), 2)

    mean_nr_words = np.mean(nr_words)
    std_nr_words = round(np.std(nr_words), 2)
    mean_nr_char = np.mean(nr_char)
    std_nr_char = round(np.std(nr_char), 2)

    return json_sample, total_nr_biographies, mean_nr_categories, nr_char, mean_nr_char, std_nr_char, nr_words, mean_nr_words, std_nr_words


def plot_word_char_histogram(mean_nr_char, std_nr_char, mean_nr_words, std_nr_words, language):
    '''Figure 1 (a) : Histogram of averaged number of characters/words per biography
    '''
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


def print_basic_statistics(json_sample, total_nr_biographies, mean_nr_categories, mean_nr_char, mean_nr_words):
    '''Print the statistics.
    '''
    pd.set_option('display.max_columns', None)
    print(f"A taste of corpus: \n {json_sample[:5]}\n")
    print(f"Total nr of biographies: {total_nr_biographies}")
    print(f"Average number of categories per biography: {mean_nr_categories}")
    print(f"Average number of characters per biography: {mean_nr_char}")
    print(f"Average number of words per biography: {mean_nr_words}")


# basic_statistics('./english_sample_long.json', 'en')

