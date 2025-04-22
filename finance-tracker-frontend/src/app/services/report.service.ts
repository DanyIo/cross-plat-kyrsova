import { Injectable } from '@angular/core';
import { HttpService } from './http.service';
import { HttpClient } from '@angular/common/http';
@Injectable({
  providedIn: 'root',
})
@Injectable({ providedIn: 'root' })
export class ReportService {
  private baseUrl = 'report/';

  constructor(
    private _httpService: HttpService,
    private _http: HttpClient,
  ) {}

  getReportData() {
    return this._httpService.get(`${this.baseUrl}data/`);
  }

  downloadPdf() {
    return this._http.get('http://localhost:8000/api/report/pdf/', {
      responseType: 'blob',
    });
  }
}
