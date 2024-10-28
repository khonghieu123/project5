import sqlite3
import csv
from datetime import datetime


class FamilyMember:
    def __init__(self, name, earning_status=True, earnings=0):
        self.name = name
        self.earning_status = earning_status
        self.earnings = earnings

    def __str__(self):
        return (
            f"Name: {self.name}, Earning Status: {'Earning' if self.earning_status else 'Not Earning'}, "
            f"Earnings: {self.earnings}"
        )


class Expense:
    def __init__(self, value, category, description, date):
        self.value = value
        self.category = category
        self.description = description
        self.date = date

    def __str__(self):
        return f"Value: {self.value}, Category: {self.category}, Description: {self.description}, Date: {self.date}"


class FamilyExpenseTracker:
    def __init__(self):
        self.members = []
        self.expense_list = []
        self.budgets = {}

    def add_family_member(self, name, earning_status=True, earnings=0):
        if not name.strip():
            raise ValueError("Name field cannot be empty")

        member = FamilyMember(name, earning_status, earnings)
        self.members.append(member)

    def delete_family_member(self, member):
        self.members.remove(member)

    def update_family_member(self, member, earning_status=True, earnings=0):
        if member:
            member.earning_status = earning_status
            member.earnings = earnings

    def calculate_total_earnings(self):
        total_earnings = sum(
            member.earnings for member in self.members if member.earning_status
        )
        return total_earnings

    def add_expense(self, value, category, description, date):
        if value == 0:
            raise ValueError("Value cannot be zero")
        if not category.strip():
            raise ValueError("Please choose a category")

        expense = Expense(value, category, description, date)
        self.expense_list.append(expense)

    def delete_expense(self, expense):
        self.expense_list.remove(expense)

    def merge_similar_category(self, value, category, description, date):
        if value == 0:
            raise ValueError("Value cannot be zero")
        if not category.strip():
            raise ValueError("Please choose a category")

        existing_expense = None
        for expense in self.expense_list:
            if expense.category == category:
                existing_expense = expense
                break

        if existing_expense:
            existing_expense.value += value
            if description:
                existing_expense.description = description
        else:
            self.add_expense(value, category, description, date)

    def calculate_total_expenditure(self):
        total_expenditure = sum(expense.value for expense in self.expense_list)
        return total_expenditure

    def set_budget(self, category, amount):
        self.budgets[category] = amount

    def get_budget(self, category):
        return self.budgets.get(category, 0)

    def export_to_csv(self, filename="expenses.csv"):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Category", "Value", "Description", "Date"])
            for expense in self.expense_list:
                writer.writerow([expense.category, expense.value, expense.description, expense.date])


def create_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)', ("admin", "password"))
    conn.commit()
    conn.close()


def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()

    conn.close()
    return user is not None


# Tạo cơ sở dữ liệu khi chạy ứng dụng
create_database()

if __name__ == "__main__":
    expense_tracker = FamilyExpenseTracker()

    try:
        # Thêm thành viên gia đình
        expense_tracker.add_family_member("John Doe", True, 5000)
        expense_tracker.add_family_member("Jane Doe", False, 0)

        print("Family Members:")
        for member in expense_tracker.members:
            print(member)

        expense_tracker.add_expense(1500, "Food", "Groceries", "2024-10-01")
        expense_tracker.add_expense(200, "Transportation", "Bus fare", "2024-10-02")

        print("\nExpenses:")
        for expense in expense_tracker.expense_list:
            print(expense)

        print("\nTotal Earnings:", expense_tracker.calculate_total_earnings())
        print("Total Expenditure:", expense_tracker.calculate_total_expenditure())

        # Thêm ngân sách cho các danh mục
        expense_tracker.set_budget("Food", 2000)
        print("Budget for Food:", expense_tracker.get_budget("Food"))

        # Xuất dữ liệu
        expense_tracker.export_to_csv()

    except ValueError as e:
        print(e)
