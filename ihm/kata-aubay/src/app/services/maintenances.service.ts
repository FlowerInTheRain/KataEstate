import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {Observable, throwError} from 'rxjs';
import {catchError, retry} from 'rxjs/operators';

export interface Maintenance {
  id?: number;
  task_description: string;
  status: 'Pending' | 'In Progress' | 'Completed';
  scheduled_date: string;
  property_id?: number;
}

@Injectable({
  providedIn: 'root',
})
export class MaintenancesService {
  private apiUrl = 'http://localhost:5000/api/maintenances/';

  constructor(private http: HttpClient) {}

  getAllMaintenanceTasks(): Observable<Maintenance[]> {
    return this.http.get<Maintenance[]>(this.apiUrl).pipe(
      retry(2), // retry twice if request fails
      catchError(this.handleError)
    );
  }

  createMaintenanceTask(maintenance: Maintenance): Observable<Maintenance> {
    return this.http.post<Maintenance>(this.apiUrl, maintenance).pipe(
      catchError(this.handleError)
    );
  }

  updateMaintenanceTask(maintenance: Maintenance): Observable<Maintenance> {
    return this.http.put<Maintenance>(`${this.apiUrl}`, maintenance).pipe(
      catchError(this.handleError)
    );
  }

  deleteMaintenanceTask(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}${id}`);
  }

  private handleError(error: HttpErrorResponse) {
    // Handle error with more detail in real apps
    console.error('API error:', error);
    return throwError(() => new Error('An error occurred with the API'));
  }
}
