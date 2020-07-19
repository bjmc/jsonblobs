from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
from itertools import chain
from collections import namedtuple

TaxRow = namedtuple(
    'TaxRow',
    ('lower', 'upper', 'single', 'married_joint', 'married_separate', 'head_of_household'),
)

def process_chunk(chunks):
    splitrows = map(lambda x: x.split(), chunks)
    toint = map(lambda x: int(x.replace(',', '')), splitrows)
    return [TaxRow(*i) for i in zip(*toint)]


def merge(segments):
    splitrows = map(lambda x: x.split(), segments)
    asint = map(lambda x: int(x.replace(',', '')), chain(*splitrows))
    return list(asint)

def main(filename='2019/i1040tt.pdf'):
    params = LAParams(
        line_overlap=0.5,
        char_margin=1.0,
        line_margin=0.3,
        word_margin=0.2,
        boxes_flow=0.5,
        detect_vertical=False,
        all_texts=False,
    )
    raw = extract_text(filename, page_numbers=range(2, 14), caching=True, laparams=params)
    chunks = raw.split('\n\n')
    col = merge(chunks[29:37])
    return chunks

if __name__ == '__main__':
    chunks = main()
