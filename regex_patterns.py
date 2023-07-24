'''This file contains all the regex patterns that are
    used for identifying biographies and handle cleaning 
    wikipedia dumps in different languages.

    Here one can add more languages by creating a 
    biography_identifying_regex and the cleaning_vocab
    in the wanted language. Then add them to the 
    regex_patterns_by_language dict (bottom of file).
'''

en_vocab_regex = {
    "references" : 'References',
    "external links" : "External [Ll]inks",
    "further reading" : "Further [Rr]eading",
    "see also" : "See [Aa]lso",
    "sources" : "Sources",
    "notes" : "Notes",
    "citations" : "Citations",
    "image" : "Image",
    "file" : "File",
    "category" : "Category"
}

sv_vocab_regex = {
    "references" : 'Referenser',
    "external links" : "Externa länkar",
    "further reading" : "Vidare läsning", 
    "see also" : "Se även",
    "sources" : "Källor", #Webbkällor
    "notes" : "Noter",
    "citations" : "Citations", #Does not seem to be used in Swedish
    "image" : "Bild",
    "file" : "Fil",
    "category" : "Kategori"
}

ru_vocab_regex = {
    "references" : 'Примечания',
    "external links" : "Ссылки",
    "further reading" : "Литература",
    "see also" : "См. также",
    "sources" : "Источники", #Does not seem to be used in Russian
    "notes" : "Примечания", #Does not seem to be used in Russian
    "citations" : "Citations", #Does not seem to be used in Russian
    "image" : "Image", #Does not seem to be used in Russian
    "file" : "Файл",
    "category" : "Категория"  
}

fa_vocab_regex = {
    "references" : 'منابع',
    "external links" : "پیوند به بیرون",
    "further reading" : "Further [Rr]eading",
    "see also" : "جستارهای وابسته",
    "sources" : "منابع",
    "notes" : "پانویس", #یادداشت‌ها
    "citations" : "منابع",
    "image" : "تصویر",
    "file" : "فایل",
    "category" : "رده",
    "gallery" : "نگارخانه"
}

zh_vocab_regex = {
    "references" : '參考文獻|参考文献',
    "external links" : "外部連結|外部链接",
    "further reading" : "參考文獻|参考文献", #Literature
    "see also" : "參見|参见",
    "sources" : "參考資料|参考资料",
    "notes" : "Notes",# Does not seem to be used in Chinese
    "citations" : "Citations",# Does not seem to be used in Chinese
    "image" : "Image", # Does not seem to be used in Chinese
    "file" : "File",
    "category" : "Category" #"(分类|分類|Category)"
}

en_identifying_regex = '\[\[Category:(Living people|.*deaths|.*births)'
sv_identifying_regex = '\[\[Kategori:(Levande personer|Födda.*|Avlidna.*)'
ru_identifying_regex = '\| *[Дд]ата рождения|\| *[Дд]ата смерти|\| *[Мм]есто рождения|\| *[Мм]есто смерти|\[\[Категория:(Персоналии по алфавиту|Родившиеся.*|Умершие.*)'
fa_identifying_regex = '\[\[رده:(افراد زنده.*|زادگان.*|درگذشتگان.*)\]\]'
zh_identifying_regex = '(\[\[(Category|分类|分類):(在世人物|.*逝世|.*出生))|(\{\{bd\|.*\}\})'

regex_patterns_by_language = { 
    'english' : {
        "biograpy_identifying_regex" : en_identifying_regex,
        "cleaning_vocab" : en_vocab_regex,
    },
    'swedish' : {
        "biograpy_identifying_regex" : sv_identifying_regex,
        "cleaning_vocab" : sv_vocab_regex,
    },
    'russian' : {
        "biograpy_identifying_regex" : ru_identifying_regex,
        "cleaning_vocab" : ru_vocab_regex,
    },
    'persian' : {
        "biograpy_identifying_regex" : fa_identifying_regex,
        "cleaning_vocab" : fa_vocab_regex,
    },
    'chinese' : {
        "biograpy_identifying_regex" : zh_identifying_regex,
        "cleaning_vocab" : zh_vocab_regex,
    },
}