import re
from common.parser import Tables,explicit
URL='https://homeloans.hdfc.bank.in/ps/home-loans-in-india/interest-rates'
def parse(raw):
    p=Tables(); p.feed(raw.decode(errors='replace') if isinstance(raw,bytes) else raw)
    for table in p.tables:
        for row in table:
            joined=' | '.join(row)
            if row and re.search(r'Special Housing Loan Rates',joined,re.I):
                continue
            if len(row)>=2 and row[0].strip().lower()=='for all loans*':
                m=re.search(r'=\s*(\d+(?:\.\d+)?)\s*%\s*to\s*(\d+(?:\.\d+)?)\s*%',row[1])
                if m: return explicit('HDFC Bank',URL,joined,float(m.group(1)),float(m.group(2)),column='Interest Rates (% p.a.) — effective range',conditions='Special housing rate for salaried and self-employed professionals/non-professionals; final rate depends on credit profile, employment, property and loan value',benchmark_type='Policy Repo Rate')
    raise ValueError('HDFC explicit HOUSING rate row not found')
