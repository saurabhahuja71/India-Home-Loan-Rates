import re
from common.parser import explicit
URL='https://sbi.co.in/web/business/information/interest-rates'
def parse(raw):
    text=raw.decode(errors='replace') if isinstance(raw,bytes) else raw
    m=re.search(r'HOME LOANS\s*\(Term Loans\)(.*?)(?:HOME LOANS\s*\(MAXGAIN\)|Other Conditions)',text,re.I|re.S)
    if not m: raise ValueError('SBI home-loan term-loan section not found')
    section=re.sub(r'<[^>]+>',' ',m.group(1)); section=' '.join(section.split())
    rates=[float(x) for x in re.findall(r'ER\s*(\d+(?:\.\d+)?)\s*%',section)]
    if not rates: raise ValueError('SBI effective home-loan rates not found')
    return explicit('State Bank of India',URL,'HOME LOANS (Term Loans) | CIBIL-linked effective rates | '+ ' '.join(f'{x:.2f}%' for x in rates),min(rates),max(rates),column='Effective Rate (ER)',conditions='Resident home-loan term loan; CIBIL-linked pricing; minimum CIBIL threshold 550; rates vary by score and loan details',credit_score_min=550,benchmark_type='EBR')
