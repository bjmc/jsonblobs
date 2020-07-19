import camelot

from collections import namedtuple
import pandas as pd
import numpy as np

COLUMNS = ('lower', 'upper', 'single', 'married_joint', 'married_separate', 'head_of_household')

TaxRow = namedtuple('TaxRow', COLUMNS)

def process_pageN(table):
	rows = (slice(1, 21), slice(22, 42), slice(43, 63))
	columns = (slice(0, 6), slice(6, 12), slice(12, 18))
	segments = []
	for c in columns:
		for r in rows:
			segments.append(table.df.iloc[r, c])
	for t in segments:
		t.columns = COLUMNS
	merged = pd.concat(segments, axis=0)
	return merged.apply(lambda x: x.str.replace(',', '')).astype(int)

def process_page1(table):
	t1 = table.df.iloc[0:62, 0:6]
	t2 = table.df.iloc[5:62, 6:12]
	t3 = table.df.iloc[5:62, 12:18]
	for t in (t1, t2, t3):
		t.columns = COLUMNS
	merged = pd.concat((t1, t2, t3), axis=0)
	merged.replace('', np.nan, inplace=True)
	merged.dropna(inplace=True)
	return merged.apply(lambda x: x.str.replace(',', '')).astype(int)


def get_tables(filename='i1040tt.pdf'):
	tables = camelot.read_pdf(filename, flavor='stream', pages='3-14')
	page1 = process_page1(tables[1])


