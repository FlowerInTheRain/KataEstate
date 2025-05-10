import {
  AfterViewInit,
  Component,
  ElementRef,
  OnDestroy,
  OnInit,
  QueryList,
  ViewChild,
  ViewChildren
} from '@angular/core';
import {RouterOutlet} from '@angular/router';
import {Property, PropertyService} from './services/properties.service';
import {Store} from '@ngrx/store';
import {removeProperty, setProperties} from './properties/properties.actions';
import {CommonModule} from '@angular/common';
import {fromEvent, interval, Observable, of, startWith, Subscription, switchMap, tap, withLatestFrom} from 'rxjs';
import {catchError} from 'rxjs/operators';
import {selectAllProperties} from './properties/properties.selectors';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, CommonModule],
  templateUrl: './app.component.html',
  standalone: true,
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit, AfterViewInit, OnDestroy {
  title = 'kata-aubay';
  properties$: Observable<ReadonlyArray<Property>>;
  @ViewChildren("deleteProperty") deleteButtons!: QueryList<ElementRef<HTMLButtonElement>>;
  private clickSubs: Subscription[] = [];

  constructor(private propertyService: PropertyService, private propertiesStore: Store<Property>) {
    this.properties$ = this.propertiesStore.select(selectAllProperties);
  }

  ngOnInit(): void {
    interval(2 * 60 * 1000) // 2 minutes
      .pipe(
        startWith(0), // pour déclencher immédiatement au démarrage
        switchMap(() => this.propertyService.getAllProperties())
      )
      .subscribe({
        next: (properties) => {
          this.propertiesStore.dispatch(setProperties({properties}));
          this.properties$ = this.propertiesStore.select(selectAllProperties);
        },
        error: (err) => {
          console.error('Failed to fetch properties:', err);
        }
      });
  }

  ngAfterViewInit() {
    this.deleteButtons.changes.subscribe(() => {
      this.subscribeToDeleteClicks();
    });

    // Si les boutons sont déjà là au premier passage :
    this.subscribeToDeleteClicks();
  }

  private subscribeToDeleteClicks() {
    this.clickSubs.forEach(sub => sub.unsubscribe());
    this.clickSubs = [];

    this.deleteButtons.forEach((btnRef, index) => {
      const sub = fromEvent(btnRef.nativeElement, 'click').pipe(
        withLatestFrom(this.properties$),
        switchMap(([_, properties]) => {
          const property = properties[index];
          if (!property) return of(null); // Or EMPTY if you want to cancel
          return this.propertyService.deleteProperty(property.id!).pipe(
            tap(() => {
              alert('Property deleted successfully');
              this.propertiesStore.dispatch(removeProperty({id: property.id!}));
            }),
            catchError((error) => {
              alert('Error deleting property');
              return of(null);
            })
          );
        })
      ).subscribe();

      this.clickSubs.push(sub);
    });
  }

  ngOnDestroy() {
    this.clickSubs.forEach(sub => sub.unsubscribe());
  }

  protected readonly selectAllProperties = selectAllProperties;
}
