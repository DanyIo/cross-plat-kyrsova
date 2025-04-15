import { Component, OnInit } from '@angular/core';
import { TransactionService } from '../../services/transaction.service';
import { Transaction } from '../../models/transaction.model';
import { MatDialog } from '@angular/material/dialog';
import { TransactionDialogComponent } from '../../components/transaction-dialog/transaction-dialog.component';
import { RouterModule } from '@angular/router';
import { MatListModule } from '@angular/material/list';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatIconModule } from '@angular/material/icon';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { FormsModule } from '@angular/forms';
import { MatTableModule } from '@angular/material/table';

@Component({
  selector: 'app-transactions',
  imports: [
    RouterModule,
    MatListModule,
    MatSidenavModule,
    MatIconModule,
    MatToolbarModule,
    MatButtonModule,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatTableModule,
  ],
  templateUrl: './transactions.component.html',
  styleUrls: ['./transactions.component.scss'],
})
export class TransactionsComponent implements OnInit {
  transactions: Transaction[] = [];

  constructor(
    private transactionService: TransactionService,
    private dialog: MatDialog
  ) { }

  ngOnInit(): void {
    this.loadTransactions();
  }

  loadTransactions(): void {
    this.transactionService.getTransactions().subscribe((data) => {
      this.transactions = data;
    });
  }

  openTransactionDialog(transaction?: Transaction): void {
    const dialogRef = this.dialog.open(TransactionDialogComponent, {
      data: transaction || {
        amount: 0,
        category: '',
        date: new Date().toISOString().split('T')[0],
        description: '',
      },
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        transaction
          ? this.updateTransaction(transaction.id, result)
          : this.addTransaction(result);
      }
    });
  }

  addTransaction(transaction: Transaction): void {
    transaction.date = new Date(transaction.date).toISOString();

    this.transactionService.addTransaction(transaction).subscribe(() => {
      this.loadTransactions();
    });
  }

  updateTransaction(id: number, transaction: Transaction): void {
    this.transactionService.updateTransaction(id, transaction).subscribe(() => {
      this.loadTransactions();
    });
  }

  deleteTransaction(id: number): void {
    if (confirm('Are you sure you want to delete this transaction?')) {
      this.transactionService.deleteTransaction(id).subscribe(() => {
        this.loadTransactions();
      });
    }
  }
}
