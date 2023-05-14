import { combineReducers, configureStore } from "@reduxjs/toolkit";
import modalReducer from "./modalSlice";
import tablesReducer from './tablesSlice';

const rootReducer = combineReducers({
  modal: modalReducer,
  tables: tablesReducer,
});

const store = configureStore({
  reducer: rootReducer,
});

export default store;