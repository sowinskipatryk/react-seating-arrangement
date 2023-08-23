import { createSlice } from "@reduxjs/toolkit";

const TABLE_SIZES = [6, 20, 20, 16, 16, 20];
const seatsNum = TABLE_SIZES.reduce((acc, val) => acc + val, 0);
const initialState = {iteration: 0, arrangement: Array.from({ length: seatsNum }, (_, index) => index + index), seatCosts: Array(seatsNum).fill(0), score: 0};

const tablesSlice = createSlice({
  name: "tables",
  initialState,
  reducers: {
    setSeatCosts(state, action) {
    return {      ...state,
      seatCosts: action.payload,
    };

  },
    setIteration(state, action) {
      return {      ...state,
        iteration: action.payload,
      };

    },
    setArrangement(state, action) {
      return {      ...state,
        arrangement: action.payload,
      };

    },
    setScore(state, action) {
      return {      ...state,
        score: action.payload,
      };

    },
}});

export const tablesActions = tablesSlice.actions;

export default tablesSlice.reducer;