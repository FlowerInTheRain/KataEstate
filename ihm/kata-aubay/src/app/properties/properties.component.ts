import {AfterViewInit, Component, ElementRef, OnDestroy, OnInit, QueryList, ViewChildren} from '@angular/core';
import {NgForOf, NgIf, NgStyle} from "@angular/common";
import {Property, PropertiesService} from '../services/properties.service';
import {fromEvent, interval, of, startWith, Subscription, switchMap, tap, withLatestFrom} from 'rxjs';
import {addProperty, removeProperty, setProperties, updateProperty} from './properties.actions';
import {catchError} from 'rxjs/operators';
import {Store} from '@ngrx/store';
import {FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators} from '@angular/forms';
import {selectAllProperties} from './properties.selectors';

@Component({
  selector: 'app-properties',
  imports: [
    NgForOf,
    NgIf,
    NgStyle,
    FormsModule,
    ReactiveFormsModule
  ],
  templateUrl: './properties.component.html',
  styleUrl: './properties.component.scss'
})
export class PropertiesComponent implements OnInit, AfterViewInit, OnDestroy {
  propertyForm!: FormGroup;
  properties$: Property[] = [];
  types = ['Residential', 'Commercial']
  statuses = ['Vacant', 'Occupied'];
  today: string;
  @ViewChildren("deleteProperty") deleteButtons!: QueryList<ElementRef<HTMLButtonElement>>;
  private clickSubs: Subscription[] = [];

  constructor(private propertyService: PropertiesService, private propertiesStore: Store<Property>, private fb: FormBuilder) {
    const now = new Date();
    this.today = now.toISOString().split('T')[0];
  }

  ngOnInit(): void {
    this.initForm();

    interval(2 * 60 * 1000) // 2 minutes
      .pipe(
        startWith(0), // pour déclencher immédiatement au démarrage
        switchMap(() => this.propertiesStore.select(selectAllProperties))
      )
      .subscribe({
        next: (properties) => {
          this.properties$ = properties.map(p => ({...p}));
        },
        error: (err) => {
          console.error('Failed to fetch properties:', err);
        }
      });
  }

  private initForm() {
    this.propertyForm = this.fb.group({
      address: ['', [Validators.required, Validators.minLength(10)]],
      type: ['', Validators.required],
      status: ['', Validators.required],
      purchase_date: ['', Validators.required],
      price: [0, [Validators.required, Validators.min(0)]],
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
    // Unsubscribe existing subscriptions
  this.clickSubs.forEach(sub => sub.unsubscribe());
  this.clickSubs = [];

  // Subscribe to click events
  this.deleteButtons.forEach((btnRef, index) => {
    const sub = fromEvent(btnRef.nativeElement, 'click').pipe(
      switchMap(() => {
        const property = this.properties$[index];
        if (!property) return of(null);

        return this.propertyService.deleteProperty(property.id!).pipe(
          tap(() => {
            alert('Property deleted successfully');
            this.propertiesStore.dispatch(removeProperty({ id: property.id! }));
            this.propertyService.getAllProperties().subscribe({
            next: (properties) => {
              this.properties$ = properties.map(p => ({...p}));
              this.initForm()
            }
          })
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

  onSubmit(): void {
    if (this.propertyForm.valid) {
      const newProperty: Property = this.propertyForm.value;
      this.propertyService.createProperty(newProperty).subscribe({
        next : (id) => {
          // @ts-ignore
          newProperty.id = id
          this.propertiesStore.dispatch(addProperty({property: newProperty}))
          this.propertiesStore.select(selectAllProperties).subscribe(
            {
              next: (properties) => {
              this.properties$ = properties.map(p => ({...p}));
              this.initForm()
            }
            }
          )
      },
        error: (err) => console.error('Failed to update:', err)
      })

      // Call your API here
    } else {
      this.propertyForm.markAllAsTouched();
    }
  }

  ngOnDestroy() {
    this.clickSubs.forEach(sub => sub.unsubscribe());
  }

  updateProperty(updatedProperty: Property) {

    this.propertyService.updateProperty(updatedProperty).subscribe({
      next: () => {
        alert("Propriété modifiée avec succès")
        this.propertiesStore.dispatch(updateProperty({property: updatedProperty}))
      },
      error: (err) => console.error('Failed to update:', err)
    });

  }
}
