from .common_adapter import parse as _parse
def make(lender,url):
    return lambda raw: _parse(raw,lender,url)
