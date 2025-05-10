import { createFeatureSelector, createSelector } from '@ngrx/store';
import {Property} from '../services/properties.service';


export const selectPropertiesState = createFeatureSelector<ReadonlyArray<Property>>('properties');

export const selectAllProperties = createSelector(
  selectPropertiesState,
  (properties) => properties
);
