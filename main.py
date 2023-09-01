'''Argument parser for cleaning the wikibios dataset.
    Example usage:
    Extracting and cleaning
    python main.py -p dumps/enwiki-20221220ms24.xml -s wiki_data/enwiki-20221220.json -l english
    
    Statistics
    python main.py --statistics -s enwiki-20221220.json -l english
    
'''

import re
from process_xml import process_xml
from argparse import ArgumentParser
from regex_patterns import regex_patterns_by_language
from basic_statistics import basic_statistics


ARG_PARSER = ArgumentParser(
    description=("Example usage: \n "
                 "python main.py -p dumps/enwiki-20221220ms24.xml -s wiki_data/enwiki-20221220.json -l english.")
)

ARG_PARSER.add_argument(
    "-p",
    "--wiki-dump-path",
    default="dumps/enwiki-20221220-pages-articles-multistream24.xml-p50564554p52064553",
    help=(
        "Path to the data."
    ),
)

ARG_PARSER.add_argument(
    "-s",
    "--save-path",
    default="wiki_data/wiki.json",
    help=(
        "Where to save the database output."
    ),
)

ARG_PARSER.add_argument(
    "-l",
    "--language",
    default="english",
    help=(
        "Choose the language. The language decides which regex to use for extracting biographies."
    ),
)

ARG_PARSER.add_argument(
    "-mc",
    "--min-characters",
    default=1000,
    help=(
        "Set a min_characters. Only adds articles longer than min_characters"
    ),
)

ARG_PARSER.add_argument(
    "-re",
    "--custom-regex",
    default=None,
    help=(
        "Add a custom regex."
    ),
)

ARG_PARSER.add_argument(
    "-stats",
    "--statistics",
    action="store_true",
    help=(
        "If flag set, then the statistics calculation will run from the save path of the json. \n"
        "Example usage: python main.py --statistics -s enwiki-20221220.json --nr_files 25 -l english"
    ),
)

ARG_PARSER.add_argument(
    "-nrf",
    "--nr_files",
    default=1,
    help=(
        "Give the number of json files in the path. \n"
    ),
)

def main():
    args = ARG_PARSER.parse_args()
    if args.statistics:
        basic_statistics(args.save_path, args.nr_files, args.language)
        return
    if args.custom_regex:
        biography_regex_pattern = re.compile(args.custom_regex)
    else:
        regex_patterns = regex_patterns_by_language[args.language]
        biography_identifying_pattern = regex_patterns["biograpy_identifying_regex"]
        biography_regex_pattern = re.compile(biography_identifying_pattern)

    print(biography_identifying_pattern)
    process_xml(xml_path=args.wiki_dump_path,
                save_path=args.save_path,
                biography_identifying_regex=biography_regex_pattern,
                language=args.language,
                min_characters=int(args.min_characters))


if __name__ == "__main__":
    main()
