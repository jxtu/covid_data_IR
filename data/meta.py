"""
sha,source_x,title,doi,pmcid,pubmed_id,license,abstract,publish_time,authors,journal,Microsoft Academic Paper ID,
WHO #Covidence,has_full_text,full_text_file
"""
from typing import Sequence
from string import digits, ascii_lowercase, ascii_uppercase


class ParseMetaData(object):
    def __init__(self, fields: Sequence):
        # TODO: add choices for selecting fields
        self.meta_doc = None
        self._get_word_shape_mapping()
        self.DATE_ABBR = dict(zip(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                                  [str(n) if n > 9 else '0' + str(n) for n in range(1, 13)]))

    def _parse_authors(self):
        try:
            authors = self.meta_doc['authors']
        except KeyError:
            return
        authors = authors.split(';')
        authors = [self._split_name(author.split(', ')) for author in authors]
        self.meta_doc['authors'] = authors

    @staticmethod
    def _split_name(name: Sequence):
        if len(name) > 1:
            return {'last_name': name[0], 'first_name': name[1]}
        else:
            return {'last_name': name[0], 'first_name': ''}

    def _parse_date(self):
        """
        possible date format:
        'dddd-dd-dd': 12281, 'dddd Ccc dd': 7323, 'dddd Ccc d': 3016, 'dddd Ccc': 736, 'dddd': 117,
        'dddd Ccc dd Ccc-Ccc': 45, 'dddd Ccc-Ccc': 41, 'dddd Ccc d Ccc-Ccc': 21, 'dddd Cccccc': 9,
        'dddd Ccc dd Cccccc': 3, 'dddd Ccc d Cccccc': 1, 'dddd Cccc': 1
        :return:
        """
        # TODO: get full date (year, month, day)
        date = self.meta_doc['publish_time']
        date_shape = ''.join(self.WORD_SHAPE_MAPPING[d] for d in date)
        if date_shape == 'dddd':
            date = {'year': date, 'month': ''}
        elif date_shape == 'dddd-dd-dd':
            date = {'year': date[:4], 'month': date[5:7]}
        elif date_shape.startswith('dddd Ccc'):
            date = {'year': date[:4], 'month': self.DATE_ABBR.get(date[5:8], '')}
        self.meta_doc['publish_time'] = date

    def _gen_es_date(self):
        """
        in the format as xxxx-xx-xx
        applied after self._parse_date()
        :return:
        """
        # hard code the day as the first day of each month
        year = self.meta_doc['publish_time']['year']
        month = self.meta_doc['publish_time']['month']
        if not year:
            year = '2019'
        if not month:
            month = '01'
        self.meta_doc['es_date'] = '-'.join([year, month, '01'])

    def _get_word_shape_mapping(self):
        self.WORD_SHAPE_MAPPING = {}
        self.WORD_SHAPE_MAPPING.update(zip(digits, len(digits) * 'd'))
        self.WORD_SHAPE_MAPPING.update(zip(ascii_lowercase, len(ascii_lowercase) * 'c'))
        self.WORD_SHAPE_MAPPING.update(zip(ascii_uppercase, len(ascii_uppercase) * 'C'))
        self.WORD_SHAPE_MAPPING.update({' ': ' ', '-': '-'})

    def __call__(self, meta_doc: dict):
        self.meta_doc = meta_doc
        self._parse_authors()
        self._parse_date()
        self._gen_es_date()


if __name__ == "__main__":
    pass
