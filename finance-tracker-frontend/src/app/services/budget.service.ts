import { Injectable } from '@angular/core';
import { HttpService } from './http.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class BudgetService {
  constructor(private _httpService: HttpService) { }

  private apiUrl = 'budget/';

  getBudget(): Observable<any> {
    return this._httpService.get(this.apiUrl);
  }

  updateBudget(budget: any): Observable<any> {
    debugger;
    return this._httpService.put(`${this.apiUrl}`, budget);
  }

  deleteBudget(id: number): Observable<any> {
    return this._httpService.delete(`${this.apiUrl}${id}/`);
  }
}
