import requests

MOEX_BASE_URL = 'https://iss.moex.com/iss/securities'

def fetch_bond_by_isin(isin: str) -> dict:
    """Запрашивает данные по облигации у MOEX по ISIN"""
    url = f'{MOEX_BASE_URL}/{isin}.json'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # ISS возвращает данные в формате columns/data — нужно сматчить индексы
    columns = data['description']['columns']
    rows = data['description']['data']

    parsed = {row[columns.index('name')]: row[columns.index('value')] for row in rows}

    return {
        'nominal': float(parsed.get('FACEVALUE', 0)),
        'coupon': float(parsed.get('COUPONVALUE', 0)),
        'payments_per_year': int(parsed.get('COUPONFREQUENCY', 1)) if parsed.get('COUPONFREQUENCY') else 1,
        'maturity_date': parsed.get('MATDATE'),
        # НКД на конкретную дату придётся брать отдельным запросом (marketdata),
        # см. ниже про случай "покупка не сегодня"
    }
