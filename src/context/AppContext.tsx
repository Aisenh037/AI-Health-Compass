// src/context/AppContext.tsx
import React, { useReducer } from 'react';
import type { ReactNode } from 'react';
import { AppContext, initialState, appReducer, useAppContext } from './AppContextBase';

export const AppProvider = ({ children }: { children: ReactNode }) => {
  const [state, dispatch] = useReducer(appReducer, initialState);

  return <AppContext.Provider value={{ state, dispatch }}>{children}</AppContext.Provider>;
};

export { useAppContext };
