import pandas as pd
from tqdm import tqdm
import jieba
import matplotlib.pyplot as plt
import re
import numpy as np
import seaborn as sns

def number_cats(data):
    #input is the corpus, output is the list of num_cats and median number of categories
    cats = data['categories']
    cats = cats.tolist()

    num_cats = []
    for i in range(len(data)):
        num_cats_i = len(cats[i])
        num_cats.append(num_cats_i)

    mean_num_cats = np.mean(num_cats)
    std_num_cats = round(np.std(num_cats),2)
    #print('The number of categories of each article is: ', num_cats)
    #print('The mean of the number of categories is: ', mean_num_cats)
    return num_cats, mean_num_cats, std_num_cats


def article_length(data, data_is_Chinese=False):
    #calculate the length of the article, both in characters and words
    #Chinese doesn't have spaces to seperate the words, so sometimes one character in Chinese can mean a single word
    """
    :param data_is_Chinese: if it is Chinese, then use jieba to make Chinese into words
    :return:
    """
    texts = data['text']
    texts = texts.tolist()

    num_words = []
    num_char = []
    for i in range(len(data)):
        text_i = texts[i]
        num_char.append(len(text_i)) #same for all languages

        if not data_is_Chinese:
            text_words = re.split('\s+', text_i) #seperating words by spaces for languages which are not Chinese
            num_words.append(len(text_words))
        else:
            text_words = jieba.cut(text_i, cut_all=False) #use jieba to cut Chinese into words
            num_words.append(len(list(text_words)))

    mean_num_words = np.mean(num_words)
    std_num_words = round(np.std(num_words), 2)
    mean_num_char = np.mean(num_char)
    std_num_char = round(np.std(num_char), 2)

    # print(num_words)
    #print('The mean of the number of words in each text is: ',mean_num_words)

    return num_words, num_char, mean_num_words, std_num_words, mean_num_char, std_num_char


def save_statistics(en_path, sv_path, ru_path, zh_path, output_path, NEED_TO_SAVE = False):
    """
    Save the statistical results of each demo corpus for later ploting
    :param en_path, sv_path, ru_path, zh_path: the path of saved json file of each corpus demo
    :param output_path: Where to save the results
    :param NEED_TO_SAVE: Defult setting is False (the results is already saved), if need to process again, set to True
    :return: csv file
    """

    #load the corpus which needed to be processed,
    en = pd.read_json(en_path)  # English demo
    sv = pd.read_json(sv_path)  # Swedish demo
    ru = pd.read_json(ru_path)  # Russion demo
    zh = pd.read_json(zh_path)  # Chinese demo
    lans = [en, sv, ru, zh]
    names = ['en', 'sv', 'ru', 'zh']

    num_cats = [] #number of categories for each bio of each language demo
    mean_num_cats = [] #mean of num_cats
    std_num_cats = [] #standard deviation of num_cats
    num_words = [] #number of words for each bio of each language demo
    num_chars = [] #number of characters for each bio of each language demo
    mean_num_words = [] #mean of num_words
    mean_num_chars = [] #mean of num_chars
    std_num_words = [] #standard deviation of num_words
    std_num_chars = [] #standard deviation of num_chars

    for i in range(len(lans)):
        lan = lans[i]

        num_cats_lan, mean_num_cats_lan, std_num_cats_lan = number_cats(lan)
        #Determine if it is Chinese
        if i == 3:
            #print(lan)
            is_Chinese = True
        else:
            is_Chinese = False

        num_words_lan, num_char_lan, mean_num_words_lan, std_num_words_lan,mean_num_char_lan,std_num_char_lan= article_length(lan, data_is_Chinese=is_Chinese)

        num_cats.append(num_cats_lan)
        mean_num_cats.append(mean_num_cats_lan)
        std_num_cats.append(std_num_cats_lan)
        num_words.append(num_words_lan)
        num_chars.append(num_char_lan)
        mean_num_words.append(mean_num_words_lan)
        mean_num_chars.append(mean_num_char_lan)
        std_num_words.append(std_num_words_lan)
        std_num_chars.append(std_num_char_lan)

    statistics = pd.DataFrame({'languages':names, 'mean_num_categories':mean_num_cats, 'std_num_categories':std_num_cats,
                               'mean_num_words': mean_num_words, 'std_num_words': std_num_words,
                               'mean_num_characters': mean_num_chars, 'std_num_characters': std_num_chars,
                               'num_categories':num_cats, 'num_words':num_words, 'num_characters':num_chars})
    statistics.to_csv(output_path, index=False)

#start ploting

#Figure 1 (a) : Histogram of averaged number of characters/words per text
def corpus_comparison(results, save_path):
    #plot graphs to compare statistics for different corpus
    #input is the DataFrame which has saved all results
    names = ['en', 'sv', 'ru', 'zh']
    para1, para2, para3, para4 = results.keys()[3:7]
    # print(para1)
    # print(para2)
    # print(para3)
    # print(para4)
    stat1 = results[para1] #mean_num_words
    stat2 = results[para2] #std_num_words
    stat3 = results[para3]  # mean_num_characters
    stat4 = results[para4]  # std_num_characters


    x_len = np.arange(len(names))
    total_width, n = 0.6, len(names)
    width = 0.3
    xticks = x_len - (total_width - width) / 2

    plt.figure(figsize=(10,8), dpi=200)
    ax = plt.axes()
    plt.grid(axis='y', c='#d2c9eb', linestyle='--', zorder=0)

    plt.bar(xticks, stat1, yerr=(stat2/2), width=0.9*width, label=para1, color='salmon', edgecolor='#d2c9eb', linewidth=0.5)
    plt.bar(xticks+width, stat3,  yerr=(stat4/2),width=0.9 * width, label=para3, color='lightblue', edgecolor='#d2c9eb', linewidth=0.5)

    for i in range(len(names)): # plot std
        plt.text(xticks[i], stat1[i], '%.2f'%stat1[i], va='baseline', ha='right',color='black',fontsize=20)
        plt.text(xticks[i]+0.3, stat3[i], '%.2f'%stat3[i], va='baseline', ha='left',color='black', fontsize=20)

    plt.legend(prop={'family':'Times New Roman', 'size':25}, ncol = 1)
    plt.xticks(x_len, names, fontproperties='Times New Roman', fontsize=25)
    plt.yticks(fontproperties='Times New Roman', fontsize=23, color='black')
    plt.xlabel('Languages', fontproperties='Times New Roman', fontsize=35)
    plt.ylabel('Averaged Number', fontproperties='Times New Roman', fontsize=38)
    plt.title('Histogram of averaged number of characters/words per text', fontproperties='Times New Roman', fontsize=25)

    plt.savefig(save_path)
    # plt.show()

#Figure 1 (b): Histogram and Density Plot for Number of Characters/Words
def density_plot(results, save_path):
    #plot graphs to compare statistics for different corpus
    #input is the DataFrame which has saved all results
    labels = ['en', 'sv', 'ru', 'zh']
    para5, para6 = results.keys()[8:]
    # print(para5)
    # print(para6)
    stat5 = results[para5] #num_words
    stat6 = results[para6] #num_chars
    lanws = []
    lanchs = []
    for i in range(len(labels)):
        stat5_i = stat5[i][1:-1]
        stat5_i = stat5_i.split(',')
        stat5_i = [int(n) for n in stat5_i]
        stat6_i = stat6[i][1:-1]
        stat6_i = stat6_i.split(',')
        stat6_i = [int(m) for m in stat6_i]
        lanws.append(stat5_i)
        lanchs.append(stat6_i)

    enw = lanws[0]
    ench = lanchs[0]
    svw = lanws[1]
    svch = lanchs[1]
    ruw = lanws[2]
    ruch = lanchs[2]
    zhw = lanws[3]
    zhch = lanchs[3]

    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 5), dpi=200)
    sns.histplot(ench, kde=True, stat='count', label='English', color='salmon', ax=ax1, line_kws={'lw': 2},
                 kde_kws={'clip': (0, 5000)})
    sns.histplot(svch, kde=True, stat='count', label='Swedish', color='lightblue', ax=ax1, line_kws={'lw': 2},
                 kde_kws={'clip': (0, 5000)})
    sns.histplot(ruch, kde=True, stat='count', label='Russian', color='#FFD0E9', ax=ax1, line_kws={'lw': 2},
                 kde_kws={'clip': (0, 5000)})
    sns.histplot(zhch, kde=True, stat='count', label='Chinese', color='#D8E7CA', ax=ax1, line_kws={'lw': 2},
                 kde_kws={'clip': (0, 5000)})
    ax1.set_xlim([0, 5000])
    # plt.legend(prop={'family':'Times New Roman', 'size':15}, ncol = 1)
    ax1.set_xlabel('Number of Characters', fontproperties='Times New Roman', fontsize=25)
    ax1.set_ylabel('Number of Biographies', fontproperties='Times New Roman', fontsize=25)
    ax1.set_title('Histogram and Density Plot for Number of Characters')

    sns.histplot(enw, kde=True, stat='count', label='English', color='salmon', ax=ax2, line_kws={'lw': 2},
                 kde_kws={'clip': (0, 1000)})
    sns.histplot(svw, kde=True, stat='count', label='Swedish', color='lightblue', ax=ax2, line_kws={'lw': 2},
                 kde_kws={'clip': (0, 1000)})
    sns.histplot(ruw, kde=True, stat='count', label='Russian', color='#FFD0E9', ax=ax2, line_kws={'lw': 2},
                 kde_kws={'clip': (0, 1000)})
    sns.histplot(zhw, kde=True, stat='count', label='Chinese', color='#D8E7CA', ax=ax2, line_kws={'lw': 2},
                 kde_kws={'clip': (0, 1000)})
    ax2.set_xlim([0, 1000])
    ax2.set_xlabel('Number of Words', fontproperties='Times New Roman', fontsize=25)
    ax2.set_ylabel('Number of Biographies', fontproperties='Times New Roman', fontsize=25)
    ax2.set_title('Histogram and Density Plot for Number of Words')

    handles, _ = ax1.get_legend_handles_labels()
    plt.figlegend(handles, labels, loc='center left', bbox_to_anchor=(0.897, 0.5), fontsize=15)

    plt.subplots_adjust(wspace=0.3)

    plt.savefig(save_path)
    # plt.show()



#Figure 2: Histogram of pronoun frequency
def pronoun_plot(data, save_path):
    #plot graphs to compare statistics for different corpus
    #input is the excel which contains pre-calculated pronoun frequency for each language
    plt.figure(figsize=(10,7),dpi=200)
    ax = plt.axes()
    plt.grid(axis='y', c='#d2c9eb', linestyle='--', zorder=0)

    plt.bar(x = data.index.values, height=data.masculine, color = 'salmon', label = 'Masculine Pronouns',
            tick_label = ['en', 'sv', 'ru', 'zh'], width=0.6)
    plt.bar(x = data.index.values, height=data.feminine,bottom=data.masculine, color='lightblue',label='Feminine Pronouns', width=0.6)
    plt.bar(x=data.index.values, height=data.neutral, bottom=data.masculine + data.feminine, color='grey', label='Neutral/Nonbinary Pronouns', width=0.6)

    cols = ['feminine', 'masculine', 'neutral']
    sum = data[cols].sum(axis=1).tolist()
    percentages = []
    for i in range(len(data)):
        pct_i = []
        pct_i.append(data.feminine.tolist()[i]/sum[i])
        pct_i.append(data.masculine.tolist()[i] / sum[i])
        pct_i.append(data.neutral.tolist()[i] / sum[i])
        percentages.append(pct_i)

    for i, row in data.iterrows():
        for j, value in row.iloc[1:].iteritems():
            if j=='feminine':
                j = 0
            elif j =='masculine':
                j = 1
            else:
                j = 2
            percent = '{:.2%}'.format(percentages[i][j])
            if j == 1:
                plt.text(i, value/2, percent, ha='center', va='center',color='black',fontsize=19)
            elif j == 2:
                if i == 0:
                    plt.text(i + 1.15, value / 2 + row[1:3].sum(), '7.93% Neutral(plural) & 0.01% Nonbinary', ha='center', va='center', color='black', fontsize=19)
                else:
                    plt.text(i, value / 2 + row[1:3].sum(), percent, ha='center', va='bottom',color='black',fontsize=19)
            else:
                plt.text(i, value / 2 + row[2], percent, ha='center', va='center',color='black',fontsize=19)


    plt.legend(prop={'family': 'Times New Roman', 'size': 20}, ncol=1, bbox_to_anchor = (0.415 , 0.55))
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=12)
    plt.xlabel('Languages', fontproperties='Times New Roman', fontsize=25)
    plt.ylabel('Pronoun Frequency', fontproperties='Times New Roman', fontsize=25)
    plt.ticklabel_format(axis='y', style='plain')
    plt.title('Histogram of pronoun frequency', fontproperties='Times New Roman',
              fontsize=25)

    plt.savefig(save_path)
    plt.show()


save_statistics(en_path='./english_sample_long.json', sv_path= './swedish_sample_long.json', ru_path= './russian_sample_long.json',
                zh_path='./chinese_sample_w_category.json', output_path='./statistics.csv',NEED_TO_SAVE=False)

stats = pd.read_csv('./statistics.csv')
corpus_comparison(stats, './char_word_lans_comparison.png')

density_plot(stats,'./prob_char.png')

pro = pd.read_excel('./pronoun.xlsx')
pronoun_plot(pro, './pronoun_frequency.png')








