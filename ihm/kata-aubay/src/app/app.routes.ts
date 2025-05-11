import {Routes} from '@angular/router';
import {PropertiesComponent} from './properties/properties.component';
import {TenantsComponent} from './tenants/tenants.component';

export const routes: Routes = [
  { path: '', component: PropertiesComponent },
  { path: 'tenants', component: TenantsComponent },
  //{ path: 'maintenances', component: MaintenancesComponent },
];
