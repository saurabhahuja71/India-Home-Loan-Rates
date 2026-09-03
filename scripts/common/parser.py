from html.parser import HTMLParser
import re

class Tables(HTMLParser):
    def __init__(self):
        super().__init__(); self.tables=[]; self._table=None; self._row=None; self._cell=None
    def handle_starttag(self, tag, attrs):
        if tag == 'table': self._table=[]
        elif self._table is not None and tag == 'tr': self._row=[]
        elif self._row is not None and tag in ('th','td'): self._cell=[]
    def handle_data(self, data):
        if self._cell is not None: self._cell.append(data)
    def handle_endtag(self, tag):
        if tag in ('th','td') and self._cell is not None:
            self._row.append(' '.join(''.join(self._cell).split())); self._cell=None
        elif tag == 'tr' and self._table is not None and self._row is not None:
            if self._row: self._table.append(self._row)
            self._row=None
        elif tag == 'table' and self._table is not None:
            if self._table: self.tables.append(self._table)
            self._table=None

def number(value):
    m=re.search(r'(?<!\d)(\d+(?:\.\d+)?)\s*%', value or '')
    return float(m.group(1)) if m else None

def parse_explicit_home_table(raw):
    p=Tables(); p.feed(raw.decode(errors='replace') if isinstance(raw,bytes) else raw)
    for table in p.tables:
        text=' '.join(' '.join(r) for r in table).lower()
        if 'home loan' not in text and 'housing loan' not in text: continue
        headers=[]
        for row in table:
            joined=' '.join(row).lower()
            if any(k in joined for k in ('rate','interest')): headers=row
        rate_col=next((i for i,c in enumerate(headers) if 'rate' in c.lower() or 'interest' in c.lower()),None)
        if rate_col is None: continue
        rows=[]
        for row in table:
            if len(row)<=rate_col or not re.search(r'home|housing|resident|salaried|individual', ' '.join(row),re.I): continue
            rate=number(row[rate_col])
            if rate is not None: rows.append((row,rate,headers[rate_col]))
        if rows: return table,rows
    raise ValueError('explicit home-loan rate table not found')

def result(rows, lender, source_url, source_type='HTML'):
    row, rate, column=max(rows,key=lambda x:x[1])
    return {'lender':lender,'category':None,'product':'HOME_LOAN','rate_type':'floating','rate_min':rate,'rate_max':rate,'borrower_type':'resident retail borrower','credit_score_min':None,'credit_score_max':None,'loan_amount_min':None,'loan_amount_max':None,'ltv_min':None,'ltv_max':None,'benchmark_type':None,'benchmark_value':None,'spread':None,'effective_date':None,'verification_status':'LIVE_VERIFIED','source_url':source_url,'source_type':source_type,'source_table':' | '.join(row),'source_row':' | '.join(row),'rate_source_column':column,'conditions':'Official home-loan table; lender-specific eligibility applies','last_verified':None,'collection_timestamp':None}
