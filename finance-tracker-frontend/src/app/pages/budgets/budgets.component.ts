import { Component } from '@angular/core';
import { BudgetService } from '../../services/budget.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button'
@Component({
  selector: 'app-budgets',
  imports: [CommonModule, FormsModule, MatButtonModule, MatCardModule, MatFormFieldModule, MatInputModule],
  templateUrl: './budgets.component.html',
  styleUrl: './budgets.component.css',
})
export class BudgetComponent {
  budget: any = { categories: [] };

  constructor(private budgetService: BudgetService) { }

  ngOnInit(): void {
    this.loadBudget();
  }

  loadBudget() {
    this.budgetService.getBudget().subscribe((data: any) => {
      this.budget = data;
    });
  }

  saveBudget() {
    this.budgetService.updateBudget(this.budget).subscribe(() => {
    });
  }

  getTotalAmount(): number {
    return this.budget.categories.reduce((sum: any, cat: any) => sum + Number(cat.amount), 0);
  }
}
