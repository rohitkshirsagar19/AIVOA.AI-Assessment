import { createSlice, type PayloadAction } from '@reduxjs/toolkit';

export interface InteractionState {
  data: Record<string, unknown>;
}

const initialState: InteractionState = {
  data: {},
};

const interactionSlice = createSlice({
  name: 'interaction',
  initialState,
  reducers: {
    setInteraction(state, action: PayloadAction<Record<string, unknown>>) {
      state.data = action.payload;
    },
    patchInteraction(state, action: PayloadAction<Record<string, unknown>>) {
      state.data = {
        ...state.data,
        ...action.payload,
      };
    },
  },
});

export const { setInteraction, patchInteraction } = interactionSlice.actions;
export default interactionSlice.reducer;
