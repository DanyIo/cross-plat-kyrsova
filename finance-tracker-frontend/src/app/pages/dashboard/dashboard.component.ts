import { Component } from '@angular/core';
import { NgxChartsModule, Color, ScaleType } from '@swimlane/ngx-charts';
import { DashboardService } from '../../services/dashboard.service';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatTableModule } from '@angular/material/table';
import { MatSliderModule } from '@angular/material/slider';
import { MatCardModule } from '@angular/material/card';
import { FormsModule } from '@angular/forms';
import { MatListModule } from '@angular/material/list';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
@Component({
  selector: 'app-dashboard',
  imports: [
    NgxChartsModule,
    MatProgressBarModule,
    MatTableModule,
    MatSliderModule,
    FormsModule,
    MatCardModule,
    MatListModule,
    MatInputModule,
    MatSelectModule,
    MatFormFieldModule,
  ],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
})
export class DashboardComponent {
  chartData: any[] = [];
  categoryDataByMonth: { [month: string]: any[] } = {}; // Stores category data for each month
  categoryData: any[] = []; // Current month's category data
  budgetData: any = {};
  financialSummary: any = {};
  recentTransactions: any[] = [];
  months: string[] = []; // Available months
  selectedMonth: string = ''; // Currently selected month
  showGeneralCategoryData: boolean = false; // Toggle for general category data

  displayedColumns: string[] = ['category', 'amount', 'transaction_type', 'date'];
  colorScheme: Color = {
    name: 'custom',
    selectable: true,
    group: ScaleType.Ordinal,
    domain: ['#00c853', '#d50000'],
  };
  pieColorScheme: Color = {
    name: 'pieScheme',
    selectable: true,
    group: ScaleType.Ordinal,
    domain: ['#ff9800', '#4caf50', '#03a9f4', '#e91e63', '#673ab7'],
  };

  constructor(private _dashboardService: DashboardService) { }

  ngOnInit(): void {
    this.loadDashboardData();
  }

  loadDashboardData(): void {
    this._dashboardService.getDashboardData().subscribe((data) => {
      this.financialSummary = data.financial_summary;
      this.chartData = this.formatChartData(data.income_expense_chart);
      this.categoryDataByMonth = this.formatCategoryData(
        data.category_breakdown
      );
      this.budgetData = data.budget_vs_actual;
      this.recentTransactions = data.recent_transactions;

      this.months = Object.keys(this.categoryDataByMonth);
      this.selectedMonth = this.months[this.months.length - 1] || ''; // Default to last available month
      this.updateCategoryData();
    });
  }

  formatChartData(data: any): any[] {
    if (!data) return [];
    const { income, expense } = data;

    return [
      { name: 'Income', series: income.map(this.formatChartEntry) },
      { name: 'Expense', series: expense.map(this.formatChartEntry) },
    ];
  }

  formatChartEntry(entry: any): any {
    return {
      name: new Date(entry.month).toLocaleString('default', {
        month: 'short',
        year: 'numeric',
      }),
      value: entry.total,
    };
  }

  formatCategoryData(data: any[]): { [month: string]: any[] } {
    const result: { [month: string]: any[] } = {};

    data.forEach((category) => {
      const date = new Date(category.month);
      const monthKey = `${date.getFullYear()}-${(date.getMonth() + 1)
        .toString()
        .padStart(2, '0')}`;

      if (!result[monthKey]) {
        result[monthKey] = [];
      }
      result[monthKey].push({
        name: category.category,
        value: category.total,
        color: category.color,
      });
    });

    return result;
  }

  updateCategoryData(): void {
    if (this.showGeneralCategoryData) {
      this.categoryData = this.aggregateCategoryData();
    } else {
      this.categoryData = this.categoryDataByMonth[this.selectedMonth] || [];
    }

    // Extract colors from category data
    this.pieColorScheme = {
      name: 'customScheme',
      selectable: true,
      group: ScaleType.Ordinal,
      domain: this.categoryData.map((category) => category.color),
    };
  }

  aggregateCategoryData(): any[] {
    const aggregatedData: {
      [category: string]: { value: number; color: string };
    } = {};

    // Aggregate data for all months, preserving category colors
    Object.values(this.categoryDataByMonth).forEach((monthData) => {
      monthData.forEach((category) => {
        if (!aggregatedData[category.name]) {
          aggregatedData[category.name] = { value: 0, color: category.color };
        }
        aggregatedData[category.name].value += category.value;
      });
    });

    // Update pie color scheme
    this.pieColorScheme = {
      name: 'customScheme',
      selectable: true,
      group: ScaleType.Ordinal,
      domain: Object.values(aggregatedData).map((category) => category.color),
    };

    return Object.keys(aggregatedData).map((category) => ({
      name: category,
      value: aggregatedData[category].value,
      color: aggregatedData[category].color,
    }));
  }
}
