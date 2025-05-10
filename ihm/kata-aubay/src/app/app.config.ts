import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import {provideHttpClient} from '@angular/common/http';
import {provideStore} from '@ngrx/store';
import {PropertiesReducer} from './properties/properties.reducer';

export const appConfig: ApplicationConfig = {
  providers: [provideHttpClient(),provideZoneChangeDetection({ eventCoalescing: true }), provideRouter(routes),provideStore({ properties: PropertiesReducer }),]
};
