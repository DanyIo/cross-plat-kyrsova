import { HttpService } from './http.service';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, BehaviorSubject } from 'rxjs';
import { tap, map } from 'rxjs/operators';
import { User } from '../models/user.model';
import { jwtDecode } from 'jwt-decode';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private apiUrl = 'auth/';
  private isAuthenticated = new BehaviorSubject<boolean>(this.hasToken());

  constructor(
    private _httpService: HttpService,
    private _router: Router,
  ) {}

  private hasToken(): boolean {
    return !!localStorage.getItem('access_token');
  }

  login(credentials: User): Observable<any> {
    return this._httpService.post(`${this.apiUrl}login/`, credentials).pipe(
      tap((response: any) => {
        localStorage.setItem('access_token', response.access);
        localStorage.setItem('refresh_token', response.refresh);
        this.isAuthenticated.next(true);
      }),
    );
  }

  register(newUser: User): Observable<any> {
    return this._httpService.post(`${this.apiUrl}register/`, newUser);
  }

  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    this.isAuthenticated.next(false);
    this._router.navigate(['/login']);
  }

  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  getTokenExpiration(): number | null {
    const token = this.getToken();
    if (!token) return null;

    try {
      const decodedToken: any = jwtDecode(token);
      return decodedToken.exp * 1000; // Convert to milliseconds
    } catch (error) {
      return null;
    }
  }

  isTokenExpired(): boolean {
    const expiration = this.getTokenExpiration();
    return expiration ? Date.now() > expiration : true;
  }

  isLoggedIn(): Observable<boolean> {
    return this.isAuthenticated.asObservable().pipe(
      map((loggedIn: boolean) => {
        if (!loggedIn || this.isTokenExpired()) {
          return false;
        }
        return true;
      }),
    );
  }
}
