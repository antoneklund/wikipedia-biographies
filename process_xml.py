'''This file handles the processing of a xml-file from a raw wikipedia dump.
    This includes cleaning of the text and saving the cleaned wiki data.
    The main function is process_xml which loops though the xml element tree. 
'''

import xml.etree.ElementTree as ET
import json
from text_processing import process_text
import tqdm

BATCH_SIZE = 50000


def process_xml(xml_path, save_path, biography_identifying_regex, language, min_characters=0):
    '''Iterates the xml element tree at xml_path.
        Finds the elements which are id, title, and the
        text body. The biography_identifying_regex determines
        which entries are considered biographies.
        The text body is processed in process_text where
        the text is stripped from tokens as well
        categories and names are extracted.
        BATCH_SIZE determines how large each batch, and
        in extension, each json-file should be.

        strategy to figure out which "id" tag it is
        (we want pages, not revisions):
        based on https://stackoverflow.com/questions/12792998/elementtree-iterparse-strategy
    '''
    print(biography_identifying_regex)
    redirect = False
    total_articles = 0
    file_count = 0
    text_batch = []
    path = []

    for event, elem in tqdm.tqdm(iterable=ET.iterparse(xml_path, events=("start", "end"))):
        tag = extract_tag(elem)

        if event == "start":
            path.append(tag)
        else:
            if tag == "id" and "revision" not in path:
                page_id = elem.text
            elif tag == "redirect":
                redirect = True
            elif tag == "title":
                title = elem.text
            elif tag == "text":
                text = elem.text

                if redirect:
                    redirect = False
                elif text is not None and biography_identifying_regex.search(text):
                    processed_text, names, categories = process_text(
                        text, language)
                    if len(processed_text) > min_characters:
                        text_batch.append({"id": page_id, "title": title, "names": names,
                                          "categories": categories, "text": str(processed_text)})
                        total_articles += 1

                if len(text_batch) >= BATCH_SIZE:
                    print("Biographies found: {}".format(total_articles))
                    current_save_path = save_path.replace(
                        ".json", "") + "_" + str(file_count) + ".json"
                    save_batch(current_save_path, text_batch)
                    text_batch = []
                    file_count += 1
            path.pop()
            elem.clear()

    print("Biographies found: {}".format(total_articles))
    current_save_path = save_path.replace(
        ".json", "") + "_" + str(file_count) + ".json"
    save_batch(current_save_path, text_batch)


def extract_tag(elem):
    '''The first 43 chars are the same
        for all tags so we remove them
    '''
    return elem.tag[43:]


def save_batch(save_path, batch):
    '''Convert a batch to json and
        saves a batch of BATCH_SIZE biographies to a json dump.
    '''
    print("Saving to json at: " + save_path)
    with open(save_path, 'w+', encoding="utf-8") as new_json_file:
        json.dump(batch, new_json_file, indent=1, ensure_ascii=False)
