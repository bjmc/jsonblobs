import camelot

import pandas as pd
import numpy as np

COLUMNS = ('lower', 'upper', 'single', 'married_joint', 'married_separate', 'head_of_household')

def clean_and_concat(segments):
    for t in segments:
        t.columns = COLUMNS
    merged = pd.concat(segments, axis=0)
    merged.replace('', np.nan, inplace=True)
    merged.dropna(inplace=True)
    return merged.apply(lambda x: x.str.replace(',', '')).astype(int)

def process_pageN(df):
    rows = (slice(1, 21), slice(22, 42), slice(43, 63))
    columns = (slice(0, 6), slice(6, 12), slice(12, 18))
    segments = []
    for c in columns:
        for r in rows:
            segments.append(df.iloc[r, c])
    return clean_and_concat(segments)

def process_page1(df):
    t1 = df.iloc[0:62, 0:6]
    t2 = df.iloc[5:62, 6:12]
    t3 = df.iloc[5:62, 12:18]
    segments = (t1, t2, t3)
    return clean_and_concat(segments)

def process_page14(df):
	top, mid, bottom = slice(5, 25), slice(27, 47), slice(48, 68)
	left, center, right = slice(0, 6), slice(6, 12), slice(12. 18)
    subsets = (
        (top, left),  # 93,000
        (mid, left),  # 94,000
        (bottom, left),  # 95,000
        (top, center),  # 96,000
        (mid, center),  # 97,000
        (bottom, center),  # 98,000
        (top, right),  # 99,000
    )
    segments = []
    for rows, columns in subsets:
        segments.append(df.iloc[rows, columns])
    return clean_and_concat(segments)

def get_tables(filename='i1040tt.pdf'):
    tables = camelot.read_pdf(filename, flavor='stream', pages='3-14')
    return tables

def reformat(tables):
    page1 = process_page1(tables[1].df)
    normals = [process_pageN(t.df) for t in tables[2:11]]
    cols = sorted(set(range(0, 21)).difference({5, 12, 19}))
    page13 = process_pageN(tables[11].df.iloc[4:, cols])
    page14 = process_page14(tables[12].df)
    total = [page1] + normals + [page13, page14]
    final = pd.concat(total, axis=0)
    return final.reset_index(drop=True)
