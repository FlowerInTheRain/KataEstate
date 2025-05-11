import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

export interface Property {
  id?: number;
  address: string;
  type: 'Residential' | 'Commercial';
  status: 'Occupied' | 'Vacant';
  purchase_date: string; // ISO format
  price: number;
}
@Injectable({
  providedIn: 'root',
})
export class PropertyService {
  private apiUrl = 'http://localhost:5000/api/properties/';

  constructor(private http: HttpClient) {}

  getAllProperties(): Observable<Property[]> {
    return this.http.get<Property[]>(this.apiUrl).pipe(
      retry(2), // retry twice if request fails
      catchError(this.handleError)
    );
  }

  createProperty(property: Property): Observable<Property> {
    return this.http.post<Property>(this.apiUrl, property).pipe(
      catchError(this.handleError)
    );
  }

  updateProperty(property: Property): Observable<Property> {
    return this.http.put<Property>(`${this.apiUrl}`, property).pipe(
      catchError(this.handleError)
    );
  }

  deleteProperty(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}${id}`);
  }

  private handleError(error: HttpErrorResponse) {
    // Handle error with more detail in real apps
    console.error('API error:', error);
    return throwError(() => new Error('An error occurred with the API'));
  }
}
