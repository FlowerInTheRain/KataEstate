import {Component, ElementRef, QueryList, ViewChildren} from '@angular/core';
import {NgForOf, NgIf, NgStyle} from '@angular/common';
import {FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators} from '@angular/forms';
import {Property} from '../services/properties.service';
import {fromEvent, interval, of, startWith, Subscription, switchMap, tap} from 'rxjs';
import {Store} from '@ngrx/store';
import {catchError} from 'rxjs/operators';
import {Tenant, TenantsService} from '../services/tenants.service';
import {selectAllProperties} from '../properties/properties.selectors';
import {Maintenance, MaintenancesService} from '../services/maintenances.service';


@Component({
  selector: 'api-maintenances',
  imports: [
    NgForOf,
    NgIf,
    ReactiveFormsModule,
    NgStyle,
    FormsModule
  ],
  templateUrl: './maintenances.component.html',
  styleUrl: './maintenances.component.scss'
})
export class MaintenancesComponent {
  propertiesMap: { [key: number]: string } = {};
  maintenanceForm!: FormGroup;
  maintenances: Maintenance[] = [];
  properties: Property[] = [];
  taskCompletionStatus = ['In Progress', 'Pending', 'Completed'];
  @ViewChildren("deleteMaintenanceTask") deleteButtons!: QueryList<ElementRef<HTMLButtonElement>>;
  private clickSubs: Subscription[] = [];

  constructor(private maintenancesService: MaintenancesService, private propertiesStore: Store<Property>, private fb: FormBuilder) {
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
        switchMap(() => this.maintenancesService.getAllMaintenanceTasks())
      )
      .subscribe({
        next: (maintenances) => {
          this.maintenances = maintenances.map(p => ({...p}));
        },
        error: (err) => {
          console.error('Failed to fetch properties:', err);
        }
      });
  }

  private initForm() {
    this.maintenanceForm = this.fb.group({
      task_description: ['', [Validators.required, Validators.minLength(10)]],
      status: ['', Validators.required],
      scheduled_date: ['', Validators.required],
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
          const maintenance = this.maintenances[index];
          if (!maintenance) return of(null);
          return this.maintenancesService.deleteMaintenanceTask(maintenance.id!).pipe(
            tap(() => {
              this.maintenances = this.maintenances.filter(t => t.id !== maintenance.id)
              alert("Tâche supprimé avec succès")
            }),
            catchError((error) => {
              alert('Error deleting task');
              return of(null);
            })
          );
        })
      ).subscribe();

      this.clickSubs.push(sub);
    });
  }

  onSubmit(): void {
    if (this.maintenanceForm.valid) {
      const newMaintenanceTask: Maintenance = this.maintenanceForm.value;
      newMaintenanceTask.property_id = Number(newMaintenanceTask.property_id)
      if(this.checkInputData(newMaintenanceTask)){

        this.maintenancesService.createMaintenanceTask(newMaintenanceTask).subscribe({
          next: (id) => {
            // @ts-ignore
            newMaintenanceTask.id = id
            this.maintenances.push(newMaintenanceTask)
            alert("Tâche ajoutée avec succès")
            this.initForm()
          },
          error: (err) => alert("Veuillez vérifier les données saisies (le numéro de téléphone doit être valide, le" +
            " nom doit être composé d'au moins 5 caractères, la date de fin de location doit être ultérieure à la" +
            " date de début de location")
        })
      }


      // Call your API here
    } else {
      this.maintenanceForm.markAllAsTouched();
    }
  }

  ngOnDestroy() {
    this.clickSubs.forEach(sub => sub.unsubscribe());
  }

  checkInputData(task: Maintenance) {
    if (task.task_description.length < 10 || task.scheduled_date.length !== 10 || !this.taskCompletionStatus.find(s => s === task.status)) {
      alert("Erreur dans le formulaire, lle statut et la date de la tâche. La description doit faire au moins 10" +
        " caractères");
      return false;
    }
    return true;
  }

  updateTask(updatedTask: Maintenance) {
    if(this.checkInputData(updatedTask)){

      this.maintenancesService.updateMaintenanceTask(updatedTask).subscribe({
        next: () => {
          alert("Tâche modifiée avec succès")
        },
        error: (err) => alert("Erreur dans le formulaire, lle statut et la date de la tâche. La description doit faire au moins 10" +
        " caractères")
      });
    }

  }
}
