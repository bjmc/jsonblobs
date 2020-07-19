from pdfminer.high_level import extract_text

def parse(rawtext):
	split_blanklines = raw.split('\n\n')
	chunks = ((12, 13, 14, 15, 16, 17),
		(18, 19, , 35)
	)
	points = []
	for s, e in chunks:
		result = process_chunk(split_blanklines[s:e])
		points.extend(result)

from collections import namedtuple
TaxRow = namedtuple('TaxRow', ('lower', 'upper', 'single', 'married_joint', 'married_separate', 'head_of_household'))


def process_chunk(chunks):
	splitrows = map(lambda x: x.split(), chunks)
	toint = map(lambda x: int(x.replace(',', '')), splitrows)
	return [TaxRow(*i) for i in zip(*toint)]


def main(filename)
	raw = extract_text(filename, page_numbers=range(2,14))
	chunks = raw.split('\n\n')
	chunks.index('But\nless\nthan')
