import { createSlice } from "@reduxjs/toolkit";

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

export const modalActions = modalSlice.actions;

export default modalSlice.reducer;