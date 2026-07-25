import math
from datetime import date, datetime


def parse_moex_date(date_str: str) -> date:
    """MOEX ISS отдаёт даты в формате 'YYYY-MM-DD'."""
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def days_between(start: date, end: date) -> int:
    return (end - start).days


def future_payments_count(days: int, payments_per_year: int) -> int:
    """Сколько купонных выплат ещё произойдёт за days дней."""
    return math.ceil(days / 365 * payments_per_year)
