import { createReducer, on } from '@ngrx/store';
import {addProperty, removeProperty, setProperties, updateProperty} from './properties.actions';
import {Property} from '../services/properties.service';

export const initialState: Property[] = [];

export const PropertiesReducer = createReducer(
  initialState,
  on(setProperties, (_, { properties }) => properties),
  on(addProperty, (state, { property }) => [...state, property]),
  on(removeProperty, (state, { id }) => state.filter(p => p.id !== id)),
  on(updateProperty, (state, { property }) =>
    state.map(p => (p.id === property.id ? { ...p, ...property } : p))
  )
);
