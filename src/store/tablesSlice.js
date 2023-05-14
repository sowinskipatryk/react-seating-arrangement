import { createSlice } from "@reduxjs/toolkit";

const TABLE_SIZES = [6, 22, 17, 17, 22, 22];
const initialState = {sizes: TABLE_SIZES, probabilities: Array(TABLE_SIZES.reduce((acc, val) => acc + val, 0)).fill(0)};

const tablesSlice = createSlice({
  name: "tables",
  initialState,
  reducers: {
    setProbabilities(state, action) {
    return {      ...state,
      probabilities: action.payload,
    };

  },
}});

export const tablesActions = tablesSlice.actions;

export default tablesSlice.reducer;