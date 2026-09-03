from common.parser import parse_explicit_home_table, result
def parse(raw, lender, source_url):
    table, rows = parse_explicit_home_table(raw)
    return result(rows,lender,source_url)
