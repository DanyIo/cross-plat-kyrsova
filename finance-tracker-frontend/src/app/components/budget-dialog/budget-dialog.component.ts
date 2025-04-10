import { Component, Inject, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { BudgetService } from '../../services/budget.service';
import { CategoryService } from '../../services/category.service';
import { RouterModule } from '@angular/router';
import { MatListModule } from '@angular/material/list';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatIconModule } from '@angular/material/icon';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';

import { MatTableModule } from '@angular/material/table';
@Component({
  selector: 'app-budget-dialog',
  imports: [
    MatListModule,
    MatInputModule,
    FormsModule,
    MatFormFieldModule,
    CommonModule,
    ReactiveFormsModule,
    MatCheckboxModule,
  ],
  templateUrl: './budget-dialog.component.html',
})
export class BudgetDialogComponent implements OnInit {
  budgetName: string = '';
  selectedCategories: any[] = [];
  availableCategories: any[] = [];

  constructor(
    public dialogRef: MatDialogRef<BudgetDialogComponent>,
    private budgetService: BudgetService,
    private categoryService: CategoryService
  ) {}

  ngOnInit(): void {
    this.categoryService.getCategories().subscribe((categories) => {
      this.availableCategories = categories;
    });
  }

  saveBudget(): void {
    const budgetData = {
      name: this.budgetName,
      categories: this.availableCategories
        .filter((c) => c.selected)
        .map((c) => ({
          category: c.id,
          amount: c.amount,
        })),
    };

    this.budgetService.createBudget(budgetData).subscribe(() => {
      this.dialogRef.close(true);
    });
  }

  toggleCategorySelection(category: any, event: any) {
    category.selected = event.checked;
  }

  close(): void {
    this.dialogRef.close();
  }
}
