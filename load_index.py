import time
import argparse
import pandas as pd

from elastic_index import ESIndex
from data.meta import ParseMetaData


def load_es_index(index_name, doc_file: str):
    meta_parser = ParseMetaData('')
    st = time.time()
    csv_df = pd.read_csv(doc_file)
    docs = []
    for i, item in enumerate(csv_df.iloc):
        meta_parser(item.to_dict())
        docs.append(meta_parser.meta_doc)
    ESIndex(index_name, docs)
    print(f"=== Built {index_name} in {round(time.time() - st, 4)} seconds ===")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('index_name')
    parser.add_argument('file_path')
    args = parser.parse_args()
    load_es_index(args.index_name, args.file_path)
    # load_es_index('covid_meta_index', 'raw_data/sub_meta.csv')
