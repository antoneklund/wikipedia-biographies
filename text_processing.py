#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''This file contains all the functions for cleaning the 
    text as well as extracting alias names and categories.

'''

import mwparserfromhell as mwp
import pandas as pd
import json
import re
from regex_patterns import regex_patterns_by_language

def extract_names(text):
    '''Extract any NAMES (bold, in first paragraph) and return them.
        Names are the different aliases that a biography is linked to.
    '''
    names = ""
    paragraphs = text.split('.\\n', maxsplit=1)
    par1 = paragraphs[0]
    alias_pattern = "'''(.*?)'''"
    names = re.findall(alias_pattern, par1)
    return names

def extract_categories(text, rd):
    '''Extracts the categories of the biography.
    '''
    category_pattern = '\[\['+rd["category"]+':.+?\]\]'
    paragraphs = text.split('.\\n', maxsplit=1)
    par1 = paragraphs[0]
    categories = re.findall(category_pattern, par1)
    categories = [clean_category(category, rd) for category in categories]
    return categories

def clean_category(text, rd):
    '''Sub-function for extract_categories. Removes the junk
        around the category text.
    '''
    text = re.sub('\[\['+rd["category"] + ':', '', text)
    text = re.sub('\]\]', '', text)
    text = re.sub('\|.*', '', text)
    return text

def strip_newlines(text):
    '''Strips all newline placeholders ('\''\'n technically).
        TODO: Is this pattern correct?
    '''
    nl_pattern = '\\\\n'
    return re.sub(nl_pattern, " ", text)


def strip_files(text, rd):
    '''Strip files and images (this loses any captions/alt text)
        TODO: decide if you want the captions/altext after all
        (currently: sort of bc it's nongreedy...)
    '''
    file_pattern = '\[\[('+rd['image']+'|'+rd['file']+'):.+?\]\]'
    temp = re.sub(file_pattern, " ", text)
    file2_pattern = '('+rd['image']+'|'+rd['file']+'):.+?$'
    return re.sub(file_pattern, " ", temp)

def strip_editornotes(text):
    '''Remove all internal editor comments (e.g. needs citation)
    '''
    edit_pattern = '<\!--.+?-->'
    return re.sub(edit_pattern, " ", text)

def strip_headings(text):
    '''Strips section headings, including the internal text
        TODO: decide if we want to keep the actual internal text or not
        (currently: no)
    '''
    heading_pattern = '==+.+?==+'
    return re.sub(heading_pattern, " ", text)

def remove_etc_sections(text, rd):
    '''Gets rid of all the "misc." sections at the end 
        and their contents (references, "see also"s, etc.).
        Currently SHOULD remove each individual section and 
        stop when it reaches the next == section
        TODO: convert for other languages...
    '''
    etc_pattern = '==+[ ]{0,1}('+ rd['references']+'|'+rd['external links']+'|'+rd['further reading']+'|'+rd['see also']+'|'+rd['notes']+')[ ]{0,1}==+[\s\S]+'
    return re.sub(etc_pattern, " ", text)

def remove_etc_sections_greedy(text, rd):
    '''Gets rid of all the "misc." sections at the end 
        and their contents (references, "see also"s, etc.)
        THIS ONE REMOVES EVERY PART OF THE DOCUMENT AFTER 
        THE FIRST ONE OF THESE SECTIONS IT ENCOUNTERS
        TODO: - convert for other languages...
             - Is the commented pattern needed?
    '''
    #etc_pattern = '==+(References|External [Ll]inks|Further [Rr]eading|See [Aa]lso|Sources|Notes|Citations|Other)==+[\s\S]+'
    etc_pattern = '==+[ ]{0,1}('+ rd['references']+'|'+rd['external links']+'|'+rd['further reading']+'|'+rd['see also']+'|'+rd['notes']+')[ ]{0,1}==+[\s\S]+'
    return re.sub(etc_pattern, " ", text)

def plain_links(text, rd):
    '''Gets rid of all the formatting around links, but keeps the running text
    '''
    #deal with regular links (keep middle)
    regular_link_pattern = '\[\[(?!'+rd['image']+'|'+rd['file']+')([^\|]+?)\]\]'
    text = re.sub(regular_link_pattern, link_contents, text)
    
    #deal with piped links:
    piped_link_pattern = '\[\[(?!'+rd['image']+'|'+rd['file']+')([^\]]+?)\|(.+?)\]\]'
    text = re.sub(piped_link_pattern, pipe_contents, text)

    return text

def link_contents(match):
    '''Support function for plain_links
    '''
    if match.group(1) is not None:
        return match.group(1)

def pipe_contents(match):
    '''Support function for plain_links
    '''
    if match.group(2) is not None:
        return match.group(2)

def strip_categories(text, rd):
    cat_pattern = '\[\['+rd["category"]+':.+?\]\]'
    return re.sub(cat_pattern, "", text)

def strip_refs(text):
    '''Remove all references (links/citation info)
    '''
    ref_pattern = '<ref[\s\S]+?/(ref)?>'
    return re.sub(ref_pattern, " ", text)

def strip_imagemap(text):
    imagemap_pattern = '<imagemap>[\s\S]+</imagemap>'
    return re.sub(imagemap_pattern, " ", text)

def strip_tables(text):
    table_pattern = r'\{\|.*class.*wikitable.*(\|\}|\\n\\n\s)'
    return re.sub(table_pattern, " ", text, flags=re.DOTALL)
#    table_pattern = '{\|\s?.*class\s?=\s?(\"|\\\')?wikitable[\s\S]+\|}'
 
def strip_galleries(text):
    ref_pattern = '<gallery.*>[\s\S]+</gallery>'
    return re.sub(ref_pattern, " ", text)

def strip_misc(text):
    '''Strip the remaining junk.
    '''
    format_pattern = '<.+?>'
    text = re.sub(format_pattern, "", text)
    table_pattern = '\{\|.+?\|\}'
    text = re.sub(table_pattern, "", text)
    empty_paren_pattern = '\(\)' #happens e.g. from pronunciation guides
    text = re.sub(empty_paren_pattern, "", text)
    bullet_pattern = '\*'
    text = re.sub(bullet_pattern, "", text)
    ugly_links = '\[http.*\]'
    text = re.sub(ugly_links, "", text)
    return text

def process_text(text, language):
    '''The main function of the text processing.
        Runs a series of extraction and cleaning functions
        on the text. Extracts categories and names.
        
        ***WARNING***
        Be careful when changing the order of the functions
        as they might depend on previous functions to work 
        properly.
    '''
    regex_patterns = regex_patterns_by_language[language]
    regex_vocab = regex_patterns["cleaning_vocab"]
    wikicode = mwp.parse(text)
    templates = wikicode.filter_templates(recursive=False)
    for t in templates:
        text = text.replace(str(t), '')  
    categories = extract_categories(text, regex_vocab)      
    text = strip_refs(text)
    text = strip_editornotes(text)
    #REMOVE <imagemap> NONSENSE HERE!!
    text = strip_imagemap(text)
    #REMOVE {| class="wikitable" .... |} NONSENSE HERE!!
    text = strip_tables(text)
    #REMOVE: <gallery > NONSENSE HERE!!
    text = strip_galleries(text)
#    text = remove_etc_sections(text, regex_vocab)
    text = remove_etc_sections_greedy(text, regex_vocab)
    text = strip_categories(text, regex_vocab)
    names = extract_names(text)
    text = strip_headings(text) #comment out if you want to keep headers
    text = plain_links(text, regex_vocab)
    text = strip_files(text, regex_vocab) #do NOT do this before plain_links!!
    text = strip_newlines(text)
    text = strip_misc(text)
    text = text.replace('\\n', '\n')

    return text, names, categories



