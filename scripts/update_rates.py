#!/usr/bin/env python3
import argparse, importlib, json, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'scripts'))
def fetch(url):
    req=urllib.request.Request(url,headers={'User-Agent':'India-Home-Loan-Rates/1.0'})
    with urllib.request.urlopen(req,timeout=25) as r: return r.read(),r.status,r.url,r.headers.get('content-type','')
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--lender',action='append'); ap.add_argument('--verbose',action='store_true'); args=ap.parse_args()
    cfg=yaml.safe_load((ROOT/'config/lenders.yaml').read_text())['lenders']; now=datetime.now(timezone.utc).isoformat()
    old=json.loads((ROOT/'data/home_loan_rates.json').read_text()) if (ROOT/'data/home_loan_rates.json').exists() else {'rates':[]}
    rates=[]; discoveries=[]; failures=[]
    for lender in cfg:
        if not lender.get('enabled',True) or (args.lender and lender['id'] not in args.lender): continue
        url=lender['source_url']; attempt={'url':url,'official_domain':True,'source_type':lender.get('source_type','html'),'http_status':None,'usable':False,'reason':''}
        try:
            raw,status,final,ctype=fetch(url); attempt['http_status']=status; attempt['final_url']=final
            mod=importlib.import_module('banks.'+lender['parser']); rec=mod.parse(raw)
            rec.update({'category':lender['category'],'source_url':final,'source_type':rec.get('source_type',lender.get('source_type','HTML')).upper(),'last_verified':now[:10],'collection_timestamp':now})
            rates.append(rec); attempt.update({'usable':True,'reason':'explicit HOME_LOAN rate evidence parsed'})
            if args.verbose: print(f"[{lender['id']}] {status} {final} -> {rec['rate_min']:.2f}%")
        except Exception as exc:
            if hasattr(exc, 'code'): attempt['http_status'] = exc.code
            if hasattr(exc, 'url'): attempt['final_url'] = exc.url
            attempt['reason']=str(exc); failures.append({'lender':lender['name'],'failure_reason':str(exc),'attempted_sources':[attempt],'last_attempt':now})
            if args.verbose: print(f"[{lender['id']}] FAILED: {exc}")
        discoveries.append({'lender':lender['name'],'sources_checked':[attempt],'selected_source':url if attempt['usable'] else None,'status':'LIVE_VERIFIED' if attempt['usable'] else 'FAILED'})
    out={'generated_at':now,'rates':rates,'failures':failures}
    (ROOT/'data').mkdir(exist_ok=True); (ROOT/'data/home_loan_rates.json').write_text(json.dumps(out,indent=2)+'\n')
    (ROOT/'data/source_discovery_report.json').write_text(json.dumps({'generated_at':now,'lenders':discoveries},indent=2)+'\n')
    (ROOT/'data/verification_report.md').write_text(report(rates,failures))
    # Never publish an empty ranking after a transient outage or source block.
    # Keep the last successful snapshot visible; diagnostics still record this run.
    if not rates and old.get('rates'):
        (ROOT/'data/home_loan_rates.json').write_text(json.dumps(old,indent=2)+'\n')
        return 0
    import generate_ranking, generate_readme, generate_site
    generate_ranking.main(); generate_readme.main(); generate_site.main()
    return 0
def report(rates, failures):
    lines=['# Home Loan Verification Report','',f'Generated: `{datetime.now(timezone.utc).isoformat()}`','']
    for r in rates: lines += [f"## {r['lender']}",f"- Product: `{r['product']}`",f"- Rate: **{r['rate_min']:.2f}%**",f"- Exact row: `{r['source_row']}`",f"- Rate column: `{r['rate_source_column']}`",f"- Source: {r['source_url']}",'']
    for f in failures: lines += [f"## {f['lender']}",f"- Status: **FAILED**",f"- Reason: {f['failure_reason']}",'']
    return '\n'.join(lines)+'\n'
if __name__=='__main__': raise SystemExit(main())
