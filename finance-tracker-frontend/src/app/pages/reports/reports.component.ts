import { Component } from '@angular/core';
import { ReportService } from '../../services/report.service';
import { saveAs } from 'file-saver';
import { NgxChartsModule } from '@swimlane/ngx-charts';

@Component({
  selector: 'app-reports',
  imports: [NgxChartsModule],
  templateUrl: './reports.component.html',
  styleUrl: './reports.component.css',
})
export class ReportsComponent {
  monthlyChartData: any[] = [];
  yearlyChartData: any[] = [];
  showXAxis = true;
  showYAxis = true;
  gradient = false;
  showLegend = true;
  showXAxisLabel = true;
  xAxisLabel = 'Month';
  showYAxisLabel = true;
  yAxisLabel = 'Amount ($)';

  constructor(private reportService: ReportService) {}

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    this.reportService.getReportData().subscribe((data: any) => {
      console.log('✅ Відповідь з API:', data);
      this.processChartData(data);
    });
  }

  processChartData(data: any) {
    const groupedMonthly: any = { income: {}, expense: {} };

    data.monthly.forEach((entry: any) => {
      if (!entry.month) return;

      const rawDate = new Date(entry.month);
      if (isNaN(rawDate.getTime())) return;

      const monthKey = new Date(
        rawDate.getFullYear(),
        rawDate.getMonth(),
        1,
      ).toISOString();

      const type = entry.transaction_type?.toLowerCase();
      if (!type || !groupedMonthly[type]) return;

      groupedMonthly[type][monthKey] = entry.total;
    });

    this.monthlyChartData = [
      {
        name: 'Income',
        series: Object.entries(groupedMonthly.income).map(([k, v]) => ({
          name: new Date(k),
          value: v,
        })),
      },
      {
        name: 'Expense',
        series: Object.entries(groupedMonthly.expense).map(([k, v]) => ({
          name: new Date(k),
          value: v,
        })),
      },
    ];
  }

  downloadPDF(): void {
    this.reportService.downloadPdf().subscribe((blob) => {
      saveAs(blob, 'Financial_Report.pdf');
    });
  }
}
