import { createSlice } from "@reduxjs/toolkit";
import guestMapping from '../assets/guest_mapping.json';

const tableSizes = [6, 20, 16, 16, 20, 20];
const guestsNum = Object.values(guestMapping).length;
const seatsNum = tableSizes.reduce((acc, val) => acc + val, 0);

for (let i = guestsNum; i <= seatsNum; i++) {
  guestMapping[i] = 'Free Seat';
}

const initialState = {iteration: 0, arrangement: Array.from({ length: seatsNum }, (_, index) => index + 1), seatCosts: Array(seatsNum).fill(0), score: 0, guestMapping, tableSizes};

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