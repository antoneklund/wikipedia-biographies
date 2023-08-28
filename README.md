# Wikipedia Biographies

Code for extracting biographies from a Wikipedia dump in multiple languages. The code takes the xml from a wikipedia dump and outputs a json-file with cleaned biographies texts along with some other data like the different names for the same biography and categories.

Presented at the 2023 RANLP conference.


## Extracting biographies

1. Download a "Database backup dump" in the preferred language from https://dumps.wikimedia.org/.
2. ```
   pip install requirements.txt 
    ```

3. Extract biographies and clean data with 
    ```sh
    python main.py -p path/to/enwiki-20230401ms24.xml -s path/to/save/biographies_corpus.json -l english
    ```
    where ``enwiki-20230401ms24.xml`` is the English Wikipedia dump and should be changed to the recently downloaded dump. The input ``english`` should be changed to the language chosen.

    __note__ There will most likely be multiple json-files. The default is to have batches of 50'000.


### Basic statistics
Some basic statistics, such as frequencies, can be calculated from the biographies_corpus. To do that run: 

```
python main.py --statistics -s path/to/corpus.json -l english
```

### Supported Languages

|Language | lan_code |
|--- | --- |
|English | en |
|Swedish | sv |
|Russian | ru |
|Chinese | zh |
|Persian | fa |


## Adding a New Language 

To add a new language, there are multiple locations in the code that need to be extended. In the file ``regex_patterns.py`` one should create a LANGCODE_identifying_regex and a LANGCODE_vocab_regex and then extend the regex_pattern_by_language in the same way as the other languages. To know what to put as the actual regex requires knowledge of the target language and an investigation on how the Wikipedia markdown is structured in that language.

(Fill out a basic methodology for filling out the regex in new languages here.)

## Cite 

(Will come when uploaded to the anthology.)