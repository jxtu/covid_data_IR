import time

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Index, Document, Text, Keyword, Integer, Nested, InnerDoc
from elasticsearch_dsl.analysis import tokenizer, analyzer
from elasticsearch import helpers
from elasticsearch_dsl.connections import connections

import pandas as pd


# sample custom analyzer
my_analyzer = analyzer('custom',
                       tokenizer='standard',
                       filter=['lowercase', 'stop'])


class CovidMeta(Document):
    # TODO: be familiar with different field type
    sha = Text()
    title = Text()
    abstract = Text()
    authors = InnerDoc()
    journal = Text()
    publish_time = InnerDoc()

    def save(self, *args, **kwargs):
        return super(CovidMeta, self).save(*args, **kwargs)


class ESIndex(object):
    def __init__(self, index_name, docs):
        connections.create_connection(hosts=['127.0.0.1'])
        self.index = index_name
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        es_index = Index(self.index)
        if es_index.exists():
            es_index.delete()
        es_index.document(CovidMeta)
        es_index.create()
        if docs is not None:
            self.load(docs)

    def to_bulk_iterable(self, docs):
        for i, doc in enumerate(docs):
            docid = doc.get('docid')
            identifier = i if docid is None else docid
            # TODO: add more
            yield {
                "_type": "_doc",
                "_id": identifier,
                "_index": self.index,
                "sha": doc['sha'],
                "title": doc['title'],
                "abstract": doc['abstract'],
                "authors": doc['authors'],
                "journal": doc['journal'],
                "publish_time": doc['publish_time']}

    def load(self, docs):
        helpers.bulk(self.es, self.to_bulk_iterable(docs))


if __name__ == "__main__":
    st = time.time()
    csv_df = pd.read_csv('raw_data/sub_meta.csv')
    docs = []
    for i, item in enumerate(csv_df.iloc):
        docs.append(item.to_dict())
    ESIndex('covid_meta_index', docs)
    print(f"=== Built index in {round(time.time() - st, 4)} seconds ===")

