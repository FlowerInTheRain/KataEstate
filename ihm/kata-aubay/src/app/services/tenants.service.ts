import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {Observable, throwError} from 'rxjs';
import {catchError, retry} from 'rxjs/operators';

export interface Tenant {
  id?: number;
  name: string;
  contact_info: string;
  lease_term_start: string;
  lease_term_end: string;
  rent_paid: 'Paid' | 'Pending';
  property_id?: number;
}

@Injectable({
  providedIn: 'root',
})
export class TenantsService {
  private apiUrl = 'http://localhost:5000/api/tenants/';

  constructor(private http: HttpClient) {}

  getAllTenants(): Observable<Tenant[]> {
    return this.http.get<Tenant[]>(this.apiUrl).pipe(
      retry(2), // retry twice if request fails
      catchError(this.handleError)
    );
  }

  createTenant(tenant: Tenant): Observable<Tenant> {
    return this.http.post<Tenant>(this.apiUrl, tenant).pipe(
      catchError(this.handleError)
    );
  }

  updateTenant(tenant: Tenant): Observable<Tenant> {
    return this.http.put<Tenant>(`${this.apiUrl}`, tenant).pipe(
      catchError(this.handleError)
    );
  }

  deleteTenant(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}${id}`);
  }

  private handleError(error: HttpErrorResponse) {
    // Handle error with more detail in real apps
    console.error('API error:', error);
    return throwError(() => new Error('An error occurred with the API'));
  }
}
