import { createSlice } from "@reduxjs/toolkit";

const TABLE_SIZES = [6, 20, 16, 16, 20, 20];
const GUESTS = [
  ];
const arrayWithEmptyValues = Array(8).fill('Empty');
const initialState = {sizes: TABLE_SIZES, guests: GUESTS.concat(arrayWithEmptyValues), probabilities: Array(TABLE_SIZES.reduce((acc, val) => acc + val, 0)).fill(0)};

const tablesSlice = createSlice({
  name: "tables",
  initialState,
  reducers: {
    setProbabilities(state, action) {
    return {      ...state,
      probabilities: action.payload,
    };

  },
    setGuests(state, action) {
      return {      ...state,
        guests: action.payload,
      };

    },
}});

export const tablesActions = tablesSlice.actions;

export default tablesSlice.reducer;