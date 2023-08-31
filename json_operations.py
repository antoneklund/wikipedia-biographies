import json
import pandas as pd
import numpy as np
from tqdm import tqdm

def combine_json(path_json, save_path, nr_files):
    '''Combines multiple json files to one.
    path should be the path to the files except the '_#.json' at the end.
    E.g. path_json = "wiki_data/enwiki-20230401"
    '''
    all_files = []
    for i in range(nr_files):
        print(i)
        with open(path_json + "_" + str(i) + ".json") as json_file:
            json_data = json.load(json_file)
            all_files = pd.concat([all_files, json_data])
        with open(save_path, "w+") as fp:
            json.dump(all_files, fp=fp)


def sample_from_multiple_json(path_json, nr_samples=50000, json_file_size=50000, total_json_files=1, save_path="sample.json"):
    ''' It requires too much memory to just combine all files into
        one large json. Therefore, we sampple from multiple files and 
        create one sample json.
    '''
    last_file = pd.read_json(path_json + "_" + str(total_json_files-1) + ".json")
    total_biographies = json_file_size*(total_json_files-1) + len(last_file)
    random_locs = np.random.choice(a=total_biographies, size=nr_samples, replace=True)
    print(random_locs)

    df = pd.DataFrame(columns = last_file.columns)

    for file_id in tqdm(range(total_json_files)):
        low = file_id * json_file_size
        high = (file_id + 1) * json_file_size
        iloc_positions = np.where(np.logical_and(random_locs>=low, random_locs<high))[0]
        ilocs = random_locs[iloc_positions]
        ilocs = ilocs - low

        current_file = pd.read_json(path_json + "_" + str(file_id) + ".json")
        new_df = current_file.iloc[ilocs]
        df = pd.concat([df, new_df])
    
    df = df.reset_index()
    df = df.drop(columns=["index"])
    df.to_json(save_path)
    return df, total_biographies
        

def apply_character_threshold(path_json, total_json_files=1, threshold=1000):
    last_file = pd.read_json(path_json + "_" + str(total_json_files-1) + ".json")
    df = pd.DataFrame(columns=last_file.columns)
    for file_id in range(0, total_json_files, 1):
        print(file_id)
        current_df = pd.read_json(path_json + "_" + str(file_id) + ".json")
        current_df["str_len"] = current_df.text.str.len()
        df = pd.concat([df, current_df[current_df["str_len"]>threshold]])
    print(df)
    df = df.reset_index()
    df = df.sample(50000)
    df.to_json("shortened.json")


def main():
    # combine_json()
    sample_from_multiple_json(path_json="wiki_data/chinese/zhwiki-20230401", total_json_files=2)
    # apply_character_threshold(path_json="wiki_data/chinese/zhwiki-20230401", total_json_files=6, threshold=500)

if __name__=="__main__":
    main()