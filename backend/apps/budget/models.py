from django.db import models
from django.utils import timezone
from apps.users.models import User
from apps.category.models import Category


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.month.strftime('%B %Y')}"


class BudgetCategory(models.Model):
    budget = models.ForeignKey(
        Budget, related_name="categories", on_delete=models.CASCADE
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.budget} - {self.category.name}: {self.amount}"
