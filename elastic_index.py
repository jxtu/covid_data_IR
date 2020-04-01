import time

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Index, Document, Text, Keyword, InnerDoc, Date
from elasticsearch_dsl.analysis import analyzer
from elasticsearch import helpers
from elasticsearch_dsl.connections import connections

import pandas as pd


# sample custom analyzer for testing
my_analyzer = analyzer('custom',
                       tokenizer='standard',
                       filter=['lowercase', 'stop'])


class CovidMeta(Document):
    """
    create Document mapping schema
    """
    sha = Text()
    title = Text()
    abstract = Text()
    authors = InnerDoc()  # data type for an array of objects
    authors_full = InnerDoc()
    institutions = InnerDoc()
    countries = InnerDoc()
    journal = Keyword()
    publish_time = InnerDoc()
    es_date = Date()  # Date data type

    def save(self, *args, **kwargs):
        return super(CovidMeta, self).save(*args, **kwargs)


class ESIndex(object):
    def __init__(self, index_name, docs):
        # connect to localhost (for elasticsearch)
        connections.create_connection(hosts=['127.0.0.1'])
        self.index = index_name
        # connect to localhost (for elasticsearch-dsl)
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        es_index = Index(self.index)
        # delete existing index that has the same name
        if es_index.exists():
            es_index.delete()
        es_index.document(CovidMeta)
        es_index.create()
        if docs is not None:
            self.load(docs)

    def to_bulk_iterable(self, docs):
        # bulk insertion
        for i, doc in enumerate(docs):
            docid = doc.get('docid')
            identifier = i if docid is None else docid
            # doc to be inserted should be consistent with Document mapping we defined above
            yield {
                "_type": "_doc",
                "_id": identifier,
                "_index": self.index,
                "sha": doc['sha'],
                "title": doc['title'],
                "abstract": doc['abstract'],
                "authors": doc['authors'],
                "authors_full": doc.get('authors_full', []),
                "institutions": doc.get('institutions', []),
                "countries": doc.get('countries', []),
                "journal": doc['journal'],
                "publish_time": doc['publish_time'],
                "es_date": doc['es_date']}

    def load(self, docs):
        helpers.bulk(self.es, self.to_bulk_iterable(docs))


if __name__ == "__main__":
    # for testing
    st = time.time()
    csv_df = pd.read_csv('raw_data/sub_meta.csv')
    docs = []
    for i, item in enumerate(csv_df.iloc):
        docs.append(item.to_dict())
    ESIndex('covid_meta_index', docs)
    print(f"=== Built index in {round(time.time() - st, 4)} seconds ===")

