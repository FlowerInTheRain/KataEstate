import { createAction, props } from '@ngrx/store';
import {Property} from '../services/properties.service';

export const setProperties = createAction(
  '[Property] Set Properties',
  props<{ properties: Property[] }>()
);

export const addProperty = createAction(
  '[Property] Add Property',
  props<{ property: Property }>()
);

export const removeProperty = createAction(
  '[Property] Remove Property',
  props<{ id: number }>()
);

export const updateProperty = createAction(
  '[Property] Update Property',
  props<{ property: Property }>()
);
