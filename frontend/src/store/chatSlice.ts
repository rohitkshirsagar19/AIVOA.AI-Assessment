import { createSlice, type PayloadAction } from '@reduxjs/toolkit';

export type ChatRole = 'user' | 'assistant';

export interface ChatMessage {
  id: string;
  role: ChatRole;
  content: string;
}

interface ChatState {
  messages: ChatMessage[];
}

const initialState: ChatState = {
  messages: [],
};

const createMessage = (role: ChatRole, content: string): ChatMessage => ({
  id: `${role}-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
  role,
  content,
});

const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    addUserMessage(state, action: PayloadAction<string>) {
      state.messages.push(createMessage('user', action.payload));
    },
    addAssistantMessage(state, action: PayloadAction<string>) {
      state.messages.push(createMessage('assistant', action.payload));
    },
  },
});

export const { addUserMessage, addAssistantMessage } = chatSlice.actions;
export default chatSlice.reducer;
