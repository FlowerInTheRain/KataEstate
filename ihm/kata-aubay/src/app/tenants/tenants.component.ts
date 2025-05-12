import {Component, ElementRef, QueryList, ViewChildren} from '@angular/core';
import {NgForOf, NgIf, NgStyle} from '@angular/common';
import {FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators} from '@angular/forms';
import {Property} from '../services/properties.service';
import {fromEvent, interval, of, startWith, Subscription, switchMap, tap} from 'rxjs';
import {Store} from '@ngrx/store';
import {catchError} from 'rxjs/operators';
import {Tenant, TenantsService} from '../services/tenants.service';
import {selectAllProperties} from '../properties/properties.selectors';


@Component({
  selector: 'api-tenants',
  imports: [
    NgForOf,
    NgIf,
    ReactiveFormsModule,
    NgStyle,
    FormsModule
  ],
  templateUrl: './tenants.component.html',
  styleUrl: './tenants.component.scss'
})
export class TenantsComponent {
  propertiesMap: { [key: number]: string } = {};
  tenantForm!: FormGroup;
  tenants: Tenant[] = [];
  properties: Property[] = [];
  paymentStatuses = ['Paid', 'Pending'];
  today: string;
  @ViewChildren("deleteTenant") deleteButtons!: QueryList<ElementRef<HTMLButtonElement>>;
  private clickSubs: Subscription[] = [];

  constructor(private tenantsService: TenantsService, private propertiesStore: Store<Property>, private fb: FormBuilder) {
    const now = new Date();
    this.today = now.toISOString().split('T')[0];
  }

  ngOnInit(): void {
    this.initForm();

    this.propertiesStore.select(selectAllProperties).subscribe({
      next: (properties) => {
        this.properties = properties.map(p => ({...p}))
        this.propertiesMap = properties.reduce((acc, p) => {
          acc[p.id!] = p.address;
          return acc;
        }, {} as { [key: number]: string });
      }
    })
    interval(2 * 60 * 1000) // 2 minutes
      .pipe(
        startWith(0), // pour déclencher immédiatement au démarrage
        switchMap(() => this.tenantsService.getAllTenants())
      )
      .subscribe({
        next: (tenants) => {
          this.tenants = tenants.map(p => ({...p}));
        },
        error: (err) => {
          console.error('Failed to fetch properties:', err);
        }
      });
  }

  private initForm() {
    this.tenantForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(10)]],
      contact_info: ['', Validators.required],
      lease_term_start: ['', Validators.required],
      lease_term_end: ['', Validators.required],
      rent_paid: ['', Validators.required],
      property_id: ['', Validators.required]
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
          const tenant = this.tenants[index];
          if (!tenant) return of(null);
          return this.tenantsService.deleteTenant(tenant.id!).pipe(
            tap(() => {
              this.tenants = this.tenants.filter(t => t.id !== tenant.id)
              alert("Locataire supprimé avec succès")
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
    if (this.tenantForm.valid) {
      const newTenant: Tenant = this.tenantForm.value;
      newTenant.property_id = Number(newTenant.property_id)
      if(this.checkInputData(newTenant)){

        this.tenantsService.createTenant(newTenant).subscribe({
          next: (id) => {
            // @ts-ignore
            newTenant.id = id
            this.tenants.push(newTenant)
            alert("Locataire ajouté avec succès")
          },
          error: (err) => alert("Veuillez vérifier les données saisies (le numéro de téléphone doit être valide, le" +
            " nom doit être composé d'au moins 5 caractères, la date de fin de location doit être ultérieure à la" +
            " date de début de location")
        })
      }


      // Call your API here
    } else {
      this.tenantForm.markAllAsTouched();
    }
  }

  ngOnDestroy() {
    this.clickSubs.forEach(sub => sub.unsubscribe());
  }

  checkInputData(tenant: Tenant) {
    if (!tenant.contact_info.match("\\+{0,1}[0-9]{10,12}") || (new Date(tenant.lease_term_start) > new Date(tenant.lease_term_end)) || !this.paymentStatuses.find(s => s === tenant.rent_paid)) {
      alert("Erreur dans le formulaire, veuillez vérifier les dates et le format du numéro de" +
        " téléphone");
      return false;
    }
    return true;
  }

  updateTenant(updatedTenant: Tenant) {
    if(this.checkInputData(updatedTenant)){

      this.tenantsService.updateTenant(updatedTenant).subscribe({
        next: () => {
          alert("Locataire modifiée avec succès")
        },
        error: (err) => alert("Erreur dans le formulaire, veuillez vérifier les dates et le format du numéro de" +
          " téléphone")
      });
    }

  }
}
