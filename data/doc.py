import json
import pprint
from os import listdir, path
from collections import Counter, defaultdict
import argparse


class ParseJsonDoc(object):
    """
    paper_id
    metadata
    abstract
    body_text
    bib_entries
    ref_entries
    back_matter
    """
    def __init__(self, file_dir, json_name):
        self.fields = {}
        try:
            if json_name.endswith('.json'):
                with open(path.join(file_dir, json_name), 'r') as f:
                    self.doc = json.load(f)
            else:
                with open(path.join(file_dir, json_name) + '.json', 'r') as f:
                    self.doc = json.load(f)
        except FileNotFoundError:
            pass
        else:
            self._parse_meta()

    def _parse_meta(self):
        meta = self.doc['metadata']
        authors = meta['authors']
        institutions = []
        countries = []
        for au in authors:
            try:
                inst = au['affiliation']['institution']
                if inst:
                    institutions.append(inst)
            except KeyError:
                pass
            try:
                country = au['affiliation']['location']['country']
                if country:
                    countries.append(country)
            except KeyError:
                pass

        self.fields['institutions'] = list(dict.fromkeys(institutions).keys())
        self.fields['countries'] = list(dict.fromkeys(countries).keys())


    # def _inspect_body_text(self):
    #     body_t = self.doc['body_text']
    #     sections = dict.fromkeys([b['section'] for b in body_t])
    #     sections = tuple(sections.keys())
    #     self.info['sections_count'] = len(sections)
    #
    # def _inspect_bib(self):
    #     bibs = self.doc['bib_entries']
    #     bibs_count = len(bibs)
    #     self.info['bibs_count'] = bibs_count
    #
    # def _inspect_ref(self):
    #     ref_counter = Counter()
    #     refs = self.doc['ref_entries']
    #     ref_counter.update(refs[k]['type'] for k in refs)
    #     for k in ref_counter:
    #         self.info[f'{k}s_count'] = ref_counter[k]
    #
    # def _inspect_abstract(self):
    #     # TODO:
    #     abstract = self.doc['abstract']


if __name__ == "__main__":
    for p in listdir('../raw_data/comm_use_subset'):
        ParseJsonDoc('../raw_data/comm_use_subset/' + p)





