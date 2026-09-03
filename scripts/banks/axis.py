import re
from common.parser import Tables,explicit
URL='https://www.axis.bank.in/loans/home-loan/interest-rates-charges'
def parse(raw):
    p=Tables(); p.feed(raw.decode(errors='replace') if isinstance(raw,bytes) else raw)
    for table in p.tables:
        has_header=any(re.search(r'cibil score', ' '.join(r),re.I) and re.search(r'effective rate', ' '.join(r),re.I) for r in table)
        for row in table:
            joined=' | '.join(row)
            if has_header and len(row)>=3 and re.search(r'cibil score',joined,re.I) and re.search(r'\d',row[-1]):
                nums=[float(x) for x in re.findall(r'(?<!\d)(\d+(?:\.\d+)?)\s*%',row[-1])]
                if nums: return explicit('Axis Bank',URL,joined,min(nums),max(nums),column='Effective Rate of Interest',conditions=f"{row[0]}; floating home loan; final pricing is credit-profile dependent",credit_score_min=751)
    raise ValueError('Axis explicit home-loan CIBIL/rate row not found')
