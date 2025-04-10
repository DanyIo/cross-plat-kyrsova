from django.db import models
from apps.users.models import User
from apps.category.models import Category

# Create your models here.
class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class BudgetCategory(models.Model):
    budget = models.ForeignKey(Budget, related_name="categories", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  

    def __str__(self):
        return f"{self.budget.name} - {self.category.name}: {self.amount}"