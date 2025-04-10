import { Injectable } from '@angular/core';
import { HttpService } from './http.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class DashboardService {
  private apiUrl = 'dashboard/';
  constructor(private _httpService: HttpService) {}

  getDashboardData(): Observable<any> {
    return this._httpService.get(`${this.apiUrl}overview/`);
  }
}
