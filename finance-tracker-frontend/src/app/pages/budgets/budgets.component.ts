import { Component } from '@angular/core';
import { BudgetService } from '../../services/budget.service';
import { MatDialog } from '@angular/material/dialog';
import { BudgetDialogComponent } from '../../components/budget-dialog/budget-dialog.component';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-budgets',
  imports: [CommonModule],
  templateUrl: './budgets.component.html',
  styleUrl: './budgets.component.css',
})
export class BudgetComponent {
  budgets: any[] = [];

  constructor(
    private _budgetService: BudgetService,
    public dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.loadBudgets();
  }

  loadBudgets(): void {
    this._budgetService.getBudgets().subscribe((data) => {
      debugger;
      this.budgets = data;
    });
  }

  openDialog(): void {
    const dialogRef = this.dialog.open(BudgetDialogComponent, {
      width: '400px',
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.loadBudgets();
      }
    });
  }
}
