#!/usr/bin/env python3
import json
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'data/home_loan_rates.json'
d=json.loads(p.read_text())
allowed={'LIVE_VERIFIED','OFFICIAL_DOCUMENT_VERIFIED','STALE','FAILED','SAMPLE'}
for r in d.get('rates',[]):
    assert r['product']=='HOME_LOAN' and r['rate_type']=='floating'
    assert r['verification_status'] in allowed and r['rate_min'] is not None
    assert r['source_url'].startswith('https://') and r['source_table'] and r['source_row'] and r['rate_source_column']
print(f"Validated {len(d.get('rates',[]))} home-loan records")
