import {Component, OnInit} from '@angular/core';
import {RouterLink, RouterLinkActive, RouterOutlet} from '@angular/router';
import {CommonModule} from '@angular/common';
import {interval, startWith, switchMap} from 'rxjs';
import {setProperties} from './properties/properties.actions';
import {PropertiesService, Property} from './services/properties.service';
import {Store} from '@ngrx/store';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, CommonModule, RouterLink, RouterLinkActive],
  templateUrl: './app.component.html',
  standalone: true,
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit{
  title = 'kata-aubay';

  constructor(private propertyService:PropertiesService, private propertiesStore: Store<Property>) {
  }

  ngOnInit(){
    interval(2 * 60 * 1000) // 2 minutes
      .pipe(
        startWith(0), // pour déclencher immédiatement au démarrage
        switchMap(() => this.propertyService.getAllProperties())
      )
      .subscribe({
        next: (properties) => {
          this.propertiesStore.dispatch(setProperties({properties}));
        },
        error: (err) => {
          console.error('Failed to fetch properties:', err);
        }
      });
  }
}
