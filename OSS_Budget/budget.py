import datetime
import json
import os
from expense import Expense

class Budget:
    def __init__(self):
        self.expenses = []
        self.monthly_budget = 0
        self.load_budget()
        
    def add_expense(self, category, description, amount, date_str=None):
        if date_str:
            try:
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                print("날짜 형식이 잘못됐습니다다. (예: 2025-06-04)")
                return
        else:
            date = datetime.date.today()

        expense = Expense(date.isoformat(), category, description, amount)
        self.expenses.append(expense)
        print("지출이 추가되었습니다.\n")

    def list_expenses(self):
        if not self.expenses:
            print("지출 내역이 없습니다.\n")
            return
        print("\n[지출 목록]")
        for idx, e in enumerate(self.expenses, 1):
            print(f"{idx}. {e}")
        print()

    def total_spent(self):
        total = sum(e.amount for e in self.expenses)
        print(f"총 지출: {total}원\n")

    def set_monthly_budget(self, amount):
        self.monthly_budget = amount
        self.save_budget()
        print("월 용돈이 설정됐습니다다.\n")

    def save_budget(self):
        with open("budget_config.json", "w") as f:
            json.dump({"monthly_budget": self.monthly_budget}, f)

    def load_budget(self):
        if os.path.exists("budget_config.json"):
            with open("budget_config.json", "r") as f:
                data = json.load(f)
                self.monthly_budget = data.get("monthly_budget", 0)

    def recommended_daily_spending(self):
        today = datetime.date.today()
        last_day = (today.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)
        days_left = (last_day - today).days + 1

        spent = sum(
            e.amount for e in self.expenses
            if datetime.datetime.strptime(e.date, "%Y-%m-%d").month == today.month
        )
        remaining = self.monthly_budget - spent

        if self.monthly_budget == 0:
            print("먼저 월 용돈을 설정하세요.\n")
        elif days_left <= 0:
            print("이번 달이 이미 끝났습니다.\n")
        else:
            daily = remaining / days_left
            print(f"남은 예산: {remaining}원")
            print(f"남은 일수: {days_left}일")
            print(f"하루 사용 가능 금액: {daily:.2f}원\n")