import { Injectable } from '@angular/core';
import { HttpService } from './http.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class BudgetService {
  constructor(private _httpService: HttpService) {}

  private apiUrl = 'budgets/';

  getBudgets(): Observable<any> {
    return this._httpService.get(this.apiUrl);
  }

  createBudget(budget: any): Observable<any> {
    debugger;
    return this._httpService.post(this.apiUrl, budget);
  }

  updateBudget(id: number, budget: any): Observable<any> {
    return this._httpService.put(`${this.apiUrl}${id}/`, budget);
  }

  deleteBudget(id: number): Observable<any> {
    return this._httpService.delete(`${this.apiUrl}${id}/`);
  }
}
