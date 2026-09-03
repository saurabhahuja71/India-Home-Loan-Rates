import io,re
from common.parser import explicit
URL='https://pnb.bank.in/downloadprocess.aspx?fid=qTs2rpANCFLABEyLLQff2g%3D%3D'
def parse(raw):
    from pypdf import PdfReader
    text='\n'.join(p.extract_text() or '' for p in PdfReader(io.BytesIO(raw)).pages)
    start=text.find('HOUSING LOAN')
    section=text[start:start+2400]
    if start<0 or 'FLOATING ROI' not in section: raise ValueError('PNB housing-loan floating section not found')
    rates=[float(x) for x in re.findall(r'present\s*ly\s*(\d+(?:\.\d+)?)\s*%',section,re.I)]
    if not rates: raise ValueError('PNB explicit housing-loan rates not found')
    return explicit('Punjab National Bank',URL,'HOUSING LOAN | FLOATING ROI | '+ ' '.join(f'{x:.2f}%' for x in rates),min(rates),max(rates),column='Floating ROI — presently effective rate',conditions='Resident housing loan; rates vary by CIBIL score, loan amount and LTV; lowest published slab is for CIBIL 800+ and loan above ₹30 lakh with LTV ≤80%',credit_score_min=600,benchmark_type='RLLR+BSP',source_type='PDF')
