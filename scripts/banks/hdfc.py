from .common_adapter import parse as _parse
def parse(raw): return _parse(raw,'HDFC Bank','https://www.hdfc.bank.in/home-loan/interest-rates')
