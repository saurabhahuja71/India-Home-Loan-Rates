import re
from common.parser import Tables,explicit
URL='https://www.bajajhousingfinance.in/home-loan-interest-rates'
def parse(raw):
    p=Tables(); p.feed(raw.decode(errors='replace') if isinstance(raw,bytes) else raw)
    for table in p.tables:
        for row in table:
            if row and row[0].strip().lower()=='home loan' and len(row)>1:
                nums=[float(x) for x in re.findall(r'(?<!\d)(\d+(?:\.\d+)?)\s*%',row[1])]
                if nums: return explicit('Bajaj Housing Finance',URL,' | '.join(row),min(nums),max(nums),column='Effective ROI (p.a.)',conditions='Home Loan product; published range, subject to borrower profile and lender terms')
    raise ValueError('Bajaj home-loan row not found')
