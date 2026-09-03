import json,html
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
def main():
    d=json.loads((ROOT/'data/home_loan_rates.json').read_text()); rows={r['lender']:r for r in d.get('rates',[])}; configured=yaml.safe_load((ROOT/'config/lenders.yaml').read_text())['lenders']; body=''
    for c in configured:
        r=rows.get(c['name']); status=r['verification_status'] if r else 'FAILED'; rate=f"{r['rate_min']:.2f}%" if r else '—'; typ=r['rate_type'] if r else '—'; conditions=r['conditions'] if r else 'No current official evidence collected'; source=(r or c)['source_url']
        body += f"<tr><td>{html.escape(c['name'])}</td><td>{html.escape(c['category'])}</td><td>{status}</td><td>{rate}</td><td>{html.escape(typ)}</td><td>{html.escape(conditions)}</td><td><a href='{html.escape(source)}'>Official source</a></td></tr>"
    page=f"<!doctype html><meta charset='utf-8'><title>India Home Loan Rates</title><h1>India Home Loan Rates</h1><p>Lowest advertised starting rates among currently verified official evidence.</p><p><a href='all-lenders.html'>All lenders and failure diagnostics</a></p><table border='1'><tr><th>Lender</th><th>Category</th><th>Status</th><th>Starting rate</th><th>Type</th><th>Conditions</th><th>Source</th></tr>{body}</table>"
    (ROOT/'index.html').write_text(page); (ROOT/'all-lenders.html').write_text(page)
if __name__=='__main__': main()
