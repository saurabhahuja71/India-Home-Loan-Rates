import json
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
def main():
    d=json.loads((ROOT/'data/home_loan_rates.json').read_text()); configured=yaml.safe_load((ROOT/'config/lenders.yaml').read_text())['lenders']; lines=['# 🇮🇳 India Home Loan Rates','','Official-source comparison of publicly advertised Indian floating home-loan rates. Rates are conditional and are not approval offers.','','## Lowest Advertised Starting Home Loan Rates','']
    labels={'public_sector':'🏛️ Public Sector Banks','private_sector':'🏦 Private Sector Banks','housing_finance_company':'🏠 Housing Finance Companies'}
    for cat,label in labels.items():
        allc=[r for r in d.get('rates',[]) if r['category']==cat]; total=sum(x['category']==cat and x.get('enabled',True) for x in configured); good=sorted([r for r in allc if r['verification_status'] in {'LIVE_VERIFIED','OFFICIAL_DOCUMENT_VERIFIED'}],key=lambda x:(x['rate_min'],x['lender']))[:5]
        lines += [f'### {label}','',f'Coverage: **{len(good)} / {total} configured lenders currently verified**','','Ranked among currently verified official evidence; coverage is not a complete market census.','', '| Rank | Lender | Starting Rate | Conditions | Type | Verification | Last Verified | Source |','|---:|---|---:|---|---|---|---|---|']
        for i,r in enumerate(good,1): lines.append(f"| {i} | {r['lender']} | {r['rate_min']:.2f}% | {r['conditions']} | {r['rate_type']} | {r['verification_status']} | {r['last_verified']} | [Official]({r['source_url']}) |")
        if not good: lines.append('| — | No current verified official evidence | — | — | — | — | — | — |')
        lines.append('')
    lines += ['## Data and audit files','','- [All lenders](all-lenders.html)','- [Ranking audit](data/ranking_audit.json)','- [Verification report](data/verification_report.md)','','> Starting rates are conditional and may depend on credit profile, loan amount, occupation, property, LTV and other eligibility criteria. Verify the lender’s official terms before applying.']
    (ROOT/'README.md').write_text('\n'.join(lines)+'\n')
if __name__=='__main__': main()
