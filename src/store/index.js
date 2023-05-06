import { createSlice, configureStore } from "@reduxjs/toolkit";

const initialState = { modalOpen: null };

const modalSlice = createSlice({
  name: "modal",
  initialState,
  reducers: {
    openModal(state, action) {
      state.modalOpen = action.payload;
    },
    closeModal(state) {
      state.modalOpen = null;
    },
  },
});

const store = configureStore({
  reducer: modalSlice.reducer,
});

export const modalActions = modalSlice.actions;

export default store;
