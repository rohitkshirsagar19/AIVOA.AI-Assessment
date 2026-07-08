import { createSlice, type PayloadAction } from '@reduxjs/toolkit';

export interface HcpProfile {
  id?: number;
  name?: string;
  specialty?: string;
  location?: string;
  affiliation?: string;
  preferred_channel?: string;
  last_interaction_summary?: string;
}

interface HcpState {
  profile: HcpProfile | null;
}

const initialState: HcpState = {
  profile: null,
};

const hcpSlice = createSlice({
  name: 'hcp',
  initialState,
  reducers: {
    setHcpProfile(state, action: PayloadAction<HcpProfile | null>) {
      state.profile = action.payload;
    },
  },
});

export const { setHcpProfile } = hcpSlice.actions;
export default hcpSlice.reducer;
