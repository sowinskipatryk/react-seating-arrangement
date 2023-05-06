import { createSlice, configureStore } from "@reduxjs/toolkit";

const initialState = { isModalOpen: false };

const modalSlice = createSlice({
  name: "modal",
  initialState,
  reducers: {
    openModal(state) {
      state.isModalOpen = true;
    },
    closeModal(state) {
      state.isModalOpen = false;
    },
  },
});

const store = configureStore({
  reducer: modalSlice.reducer,
});

export const modalActions = modalSlice.actions;

export default store;
