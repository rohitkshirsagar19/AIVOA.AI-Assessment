import { configureStore } from '@reduxjs/toolkit';

import chatReducer from '../store/chatSlice';
import hcpReducer from '../store/hcpSlice';
import interactionReducer from '../store/interactionSlice';
import uiReducer from '../store/uiSlice';

export const store = configureStore({
  reducer: {
    chat: chatReducer,
    interaction: interactionReducer,
    hcp: hcpReducer,
    ui: uiReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
