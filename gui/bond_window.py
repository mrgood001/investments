import tkinter as tk
from tkinter import ttk, simpledialog
from datetime import date

from gui.base_window import BaseApp
from core.calculator import Bond
from core.moex_client import fetch_bond_by_isin
from core.bond_math import parse_moex_date, days_between, future_payments_count
from core.settings import load_commission_rate, save_commission_rate


class BondApp(BaseApp):
    def __init__(self):
        super().__init__(title="Калькулятор облигаций", geometry="600x500")

        calculator_screen = CalculatorScreen(self.container, self)
        self.register_screen("calculator", calculator_screen)
        self.show_screen("calculator")


class CalculatorScreen(ttk.Frame):
    def __init__(self, parent, app: BondApp):
        super().__init__(parent)
        self.app = app

        ttk.Label(self, text="ISIN").pack(anchor="w", padx=10)
        self.isin_entry = ttk.Entry(self)
        self.isin_entry.pack(fill="x", padx=10)

        ttk.Label(self, text="Цена покупки (руб.)").pack(anchor="w", padx=10)
        self.price_entry = ttk.Entry(self)
        self.price_entry.pack(fill="x", padx=10)

        self.non_standard_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            self,
            text="Покупка совершена не сегодня",
            variable=self.non_standard_var,
            command=self._toggle_non_standard_fields,
        ).pack(anchor="w", padx=10, pady=10)

        self.non_standard_frame = ttk.Frame(self)

        ttk.Label(self.non_standard_frame, text="Дата сделки (ГГГГ-ММ-ДД)").pack(anchor="w")
        self.deal_date_entry = ttk.Entry(self.non_standard_frame)
        self.deal_date_entry.pack(fill="x")

        ttk.Label(self.non_standard_frame, text="НКД на дату сделки").pack(anchor="w")
        self.nkd_entry = ttk.Entry(self.non_standard_frame)
        self.nkd_entry.pack(fill="x")

        ttk.Label(self.non_standard_frame, text="Купонов пришло с даты сделки(необязятельно)").pack(anchor="w")
        self.past_payments_entry = ttk.Entry(self.non_standard_frame)
        self.past_payments_entry.pack(fill="x")

        ttk.Button(self, text="Рассчитать", command=self._on_calculate).pack(pady=10)

        self.result_label = ttk.Label(self, text="", justify="left")
        self.result_label.pack(pady=10, padx=10, anchor="w")

    def _toggle_non_standard_fields(self) -> None:
        if self.non_standard_var.get():
            self.non_standard_frame.pack(fill="x", padx=10, pady=(0,20))
        else:
            self.non_standard_frame.pack_forget()

        self.app.update_idletasks()
        self.app.geometry("")  # сброс фиксированного размера — Tk сам посчитает нужный

    def _get_commission(self) -> float:
        rate = load_commission_rate()
        if rate is None:
            rate = simpledialog.askfloat(
                "Комиссия", "Укажи ставку комиссии брокера (например 0.003):"
            )
            save_commission_rate(rate)
        return rate

    def _on_calculate(self) -> None:
        isin = self.isin_entry.get().strip()
        price = float(self.price_entry.get())
        commission_rate = self._get_commission()

        bond_data = fetch_bond_by_isin(isin)
        maturity_date = parse_moex_date(bond_data["maturity_date"])
        today = date.today()

        if self.non_standard_var.get():
            deal_date = parse_moex_date(self.deal_date_entry.get().strip())
            nkd = float(self.nkd_entry.get())
            # past_payments пока не используется — зарезервировано под будущую сверку НКД
            # past_payments = int(self.past_payments_entry.get())

            days = days_between(deal_date, maturity_date)
            payments = future_payments_count(days, bond_data["payments_per_year"])
        else:
            nkd = 0.0
            days = days_between(today, maturity_date)
            payments = future_payments_count(days, bond_data["payments_per_year"])

        bond = Bond(
            name=isin,
            price=price,
            nominal=bond_data["nominal"],
            nkd=nkd,
            commission=price * commission_rate,
            coupon=bond_data["coupon"],
            payments=payments,
            payments_per_year=bond_data["payments_per_year"],
            days=days,
        )

        self.result_label.config(
            text=(
                f"Доходность за период: {bond.total_yield}%\n"
                f"Годовая доходность: {bond.annual_yield}%\n"
                f"Годовая купонная доходность: {bond.annual_coupon_yield}%\n"
                f"Коммисия облигации: {bond.commission}\n"
            )
        )
