import { createSlice, type PayloadAction } from '@reduxjs/toolkit';

interface UiState {
  loading: boolean;
  error: string | null;
  lastToolUsed: string | null;
}

const initialState: UiState = {
  loading: false,
  error: null,
  lastToolUsed: null,
};

const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    setLoading(state, action: PayloadAction<boolean>) {
      state.loading = action.payload;
    },
    setError(state, action: PayloadAction<string | null>) {
      state.error = action.payload;
    },
    setLastToolUsed(state, action: PayloadAction<string | null>) {
      state.lastToolUsed = action.payload;
    },
  },
});

export const { setLoading, setError, setLastToolUsed } = uiSlice.actions;
export default uiSlice.reducer;
