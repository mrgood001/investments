TAX = 0.13  # налог


def round_two_simbol(num: float) -> float:
    str_val = str(num)
    if '.' in str_val:
        integer_part, fractional_part = str_val.split('.')
        return float(integer_part + '.' + fractional_part[:2])


class Bond:
    def __init__(
        self,
        name: str,
        price: float,
        nominal: int,
        nkd: float,
        commission: float,
        coupon: float,
        payments: int,
        payments_per_year: int,
        days: int
    ):
        self.name = name
        self.price = price
        self.nominal = nominal
        self.nkd = nkd
        self.commission = commission
        self.coupon = coupon
        self.payments = payments
        self.payments_per_year = payments_per_year
        self.days = days

    @property
    def purchase_price(self):
        return self.price + self.nkd + self.commission


    @property
    def redemption_sum(self):
        return self.coupon_sum + self.nominal

    @property
    def clean_income(self):
        income = self.redemption_sum - self.purchase_price
        return round_two_simbol(income - income * TAX)

    @property
    def total_yield(self):
        return round_two_simbol(self.clean_income * 100 / self.purchase_price)

    @property
    def coupon_sum(self):
        return self.coupon * self.payments

    @property
    def annual_coupon_yield(self):
        clean_coupon = round_two_simbol(self.coupon * (1 - TAX))
        percent = round_two_simbol(clean_coupon * 100 / self.purchase_price)
        return percent * self.payments_per_year

    @property
    def annual_yield(self):
        return round_two_simbol(
            self.total_yield
            / self.days
            * 365
        )
