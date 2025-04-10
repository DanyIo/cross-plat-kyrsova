
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from apps.transactions.models import Transaction, TransactionType
from apps.category.models import Category

class DashboardService:
    def __init__(self, user):
        self.user = user

    def get_income_expense_chart(self):
        income_data = (
            Transaction.objects.filter(user=self.user, transaction_type=TransactionType.INCOME)
            .annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(total=Sum("amount"))
            .order_by("month")
        )

        expense_data = (
            Transaction.objects.filter(user=self.user, transaction_type=TransactionType.EXPENSE)
            .annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(total=Sum("amount"))
            .order_by("month")
        )

        return {"income": list(income_data), "expense": list(expense_data)}

    def get_financial_summary(self):
        total_income = Transaction.objects.filter(user=self.user, transaction_type=TransactionType.INCOME).aggregate(Sum("amount"))["amount__sum"] or 0
        total_expense = Transaction.objects.filter(user=self.user, transaction_type=TransactionType.EXPENSE).aggregate(Sum("amount"))["amount__sum"] or 0
        net_balance = total_income - total_expense

        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "net_balance": net_balance
        }

    def get_category_breakdown(self):
        category_data = (
            Transaction.objects.filter(user=self.user, transaction_type=TransactionType.EXPENSE)
            .annotate(month=TruncMonth("date"))
            .values("month", "category")
            .annotate(total=Sum("amount"))
            .order_by("-month", "-total")
        )

        # Fetch category colors from the database
        category_colors = {c.name: c.color for c in Category.objects.filter(user=self.user)}

        # Add colors to category data
        for entry in category_data:
            entry["color"] = category_colors.get(entry["category"], "#000000")  # Default to black if not found

        return list(category_data)


    def get_budget_vs_actual(self, monthly_budget=2000):  # Default budget
        total_expense = (
            Transaction.objects.filter(user=self.user, transaction_type=TransactionType.EXPENSE)
            .aggregate(Sum("amount"))["amount__sum"] or 0
        )

        return {
            "budget": monthly_budget,
            "actual_spent": total_expense,
            "remaining_budget": max(0, monthly_budget - total_expense),
            "percent_spent": min(100, (total_expense / monthly_budget) * 100 if monthly_budget else 0)
        }

    def get_recent_transactions(self, limit=5):
        transactions = Transaction.objects.filter(user=self.user).order_by("-date")[:limit]
        return [
            {
                "category": t.category,
                "amount": t.amount,
                "date": t.date,
                "transaction_type": t.transaction_type,
                "description": t.description
            }
            for t in transactions
        ]
