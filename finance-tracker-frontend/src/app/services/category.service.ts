import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpService } from './http.service';
import { Category } from '../models/category.model';

@Injectable({
  providedIn: 'root',
})
export class CategoryService {
  private apiUrl = 'categories/';

  constructor(private _httpService: HttpService) {}

  getCategories(): Observable<Category[]> {
    return this._httpService.get<Category[]>(this.apiUrl);
  }

  addCategory(category: Category): Observable<Category> {
    return this._httpService.post<Category>(this.apiUrl, category);
  }

  updateCategory(category: Category): Observable<Category> {
    return this._httpService.put<Category>(
      `${this.apiUrl}${category.id}/`,
      category
    );
  }

  deleteCategory(id: number): Observable<void> {
    return this._httpService.delete<void>(`${this.apiUrl}${id}/`);
  }
}
