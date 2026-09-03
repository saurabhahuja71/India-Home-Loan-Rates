import re
from common.parser import Tables,explicit
URL='https://www.icici.bank.in/personal-banking/loans/home-loan/interest-rates'
def parse(raw):
    p=Tables(); p.feed(raw.decode(errors='replace') if isinstance(raw,bytes) else raw)
    for table in p.tables:
        rows=table
        if not rows or not any(re.search(r'fixed tenure|home loan', ' '.join(r),re.I) for r in rows): continue
        for row in rows:
            if len(row)>=2 and re.search(r'month|year',row[0],re.I) and not re.search(r'balance transfer|top.?up|plot|property', ' '.join(row),re.I):
                nums=[float(x) for x in re.findall(r'(?<!\d)(\d+(?:\.\d+)?)\s*%', ' '.join(row[1:]))]
                if nums: return explicit('ICICI Bank',URL,' | '.join(row),min(nums),max(nums),column='Rate of Interest',conditions='New home loan fixed-tenure rate table; final rate is subject to borrower profile and applicable terms')
    raise ValueError('ICICI explicit new home-loan rate row not found')
