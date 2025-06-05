import datetime
import json
import os
from expense import Expense

class Budget:
    def __init__(self):
        self.expenses = []
        self.monthly_budget = 0
        self.load_budget()

    def add_expense(self, category, description, amount):
        today = datetime.date.today().isoformat()
        expense = Expense(today, category, description, amount)
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
        print("월 용돈이 설정되었습니다.\n")

    def save_budget(self):
        with open("budget_config.json", "w") as f:
            json.dump({"monthly_budget": self.monthly_budget}, f)

    def load_budget(self):
        if os.path.exists("budget_config.json"):
            with open("budget_config.json", "r") as f:
                data = json.load(f)
                self.monthly_budget = data.get("monthly_budget", 0)
