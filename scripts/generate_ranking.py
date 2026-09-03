import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CATS=['public_sector','private_sector','housing_finance_company']
def main():
    d=json.loads((ROOT/'data/home_loan_rates.json').read_text()); rows=d.get('rates',[]); out=[]
    for cat in CATS:
        eligible=sorted([r for r in rows if r['category']==cat and r['verification_status'] in {'LIVE_VERIFIED','OFFICIAL_DOCUMENT_VERIFIED'}],key=lambda r:(r['rate_min'],r['lender']))
        out.append({'profile':'advertised_starting_rate','category':cat,'ranking':[{'rank':i,'lender':r['lender'],'rate':r['rate_min'],'verification_status':r['verification_status']} for i,r in enumerate(eligible,1)],'excluded':[{'lender':r['lender'],'reason':r.get('verification_status','FAILED')} for r in rows if r['category']==cat and r not in eligible]})
    (ROOT/'data/ranking_audit.json').write_text(json.dumps({'generated_at':d.get('generated_at'),'rankings':out},indent=2)+'\n')
if __name__=='__main__': main()
