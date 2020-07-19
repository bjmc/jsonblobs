from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
from itertools import chain
from collections import namedtuple

COLUMNS = ('lower', 'upper', 'single', 'married_joint', 'married_separate', 'head_of_household')
START_LINE = 'But\nless\nthan'

TaxRow = namedtuple('TaxRow', COLUMNS)

def parse(seg):
    return [int(i.replace(',', '')) for i in seg.split()]

def process_chunk(chunks):
    splitrows = map(lambda x: x.split(), chunks)
    toint = map(lambda x: int(x.replace(',', '')), splitrows)
    return [TaxRow(*i) for i in zip(*toint)]


def merge(segments):
    splitrows = map(lambda x: x.split(), segments)
    asint = map(lambda x: int(x.replace(',', '')), chain(*splitrows))
    return list(asint)

def process(chunks):
    col = -1
    cols = list(list() for i in range(6))
    for lines in chunks:
        if lines == START_LINE:
            print("starting")
            col = 0
        elif col >= 0:
            try:
                segment = parse(lines)
                print("segment is", segment)
            except ValueError:
                sofar = [TaxRow(*i) for i in zip(*cols)]
                print(sofar)
                yield sofar
                col = -1
                cols = list(list() for i in range(6))
            else:
                if segment[0] > cols[col][-1]:
                    cols[col].extend(segment)
                else:
                    col += 1

def main(filename='2019/i1040tt.pdf'):
    params = LAParams(
        line_overlap=0.5,
        char_margin=1.0,
        line_margin=0.3,
        word_margin=0.2,
        boxes_flow=-0.5,
        detect_vertical=False,
        all_texts=False,
    )
    raw = extract_text(filename, page_numbers=range(2, 14), caching=True, laparams=params)
    chunks = raw.split('\n\n')
    return list(process(chunks))

if __name__ == '__main__':
    chunks = main()