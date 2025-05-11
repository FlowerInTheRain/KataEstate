import {Component} from '@angular/core';
import {RouterOutlet} from '@angular/router';
import {CommonModule} from '@angular/common';
import {PropertiesComponent} from './properties/properties.component';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, CommonModule, PropertiesComponent],
  templateUrl: './app.component.html',
  standalone: true,
  styleUrl: './app.component.scss'
})
export class AppComponent{
  title = 'kata-aubay';
}
