import re
from common.parser import explicit
URL='https://bankofbaroda.bank.in/loans/home-loan/baroda-home-loan'
def parse(raw):
    text=raw.decode(errors='replace') if isinstance(raw,bytes) else raw
    if not re.search(r'Baroda Home Loan',text,re.I) or not re.search(r'Resident Indians',text,re.I): raise ValueError('BOB resident home-loan product context not found')
    m=re.search(r'home loan starting\s*@\s*(\d+(?:\.\d+)?)\s*%',text,re.I)
    if not m: raise ValueError('BOB explicit home-loan starting rate not found')
    return explicit('Bank of Baroda',URL,m.group(0),float(m.group(1)),column='Official home-loan starting-rate statement',conditions='Resident Indian applicants; floating rate linked to BRLLR; final rate depends on CIBIL, income and loan details',benchmark_type='BRLLR')
