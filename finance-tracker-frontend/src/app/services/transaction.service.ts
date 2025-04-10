import { Injectable } from '@angular/core';
import { HttpService } from './http.service';
import { Observable } from 'rxjs';
import { Transaction } from '../models/transaction.model';

@Injectable({
  providedIn: 'root',
})
export class TransactionService {
  private apiUrl = 'transactions/';

  constructor(private _httpService: HttpService) {}

  getTransactions(): Observable<Transaction[]> {
    return this._httpService.get<Transaction[]>(this.apiUrl);
  }

  addTransaction(transaction: Transaction): Observable<Transaction> {
    return this._httpService.post<Transaction>(this.apiUrl, transaction);
  }

  updateTransaction(
    id: number,
    transaction: Transaction
  ): Observable<Transaction> {
    return this._httpService.put<Transaction>(
      `${this.apiUrl}${id}/`,
      transaction
    );
  }

  deleteTransaction(id: number): Observable<void> {
    return this._httpService.delete<void>(`${this.apiUrl}${id}/`);
  }
}
