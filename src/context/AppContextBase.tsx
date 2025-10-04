import React, { createContext, useContext } from 'react';
import type { Benefit } from '../services/mockData';

// 1. Define the shape of our state
interface AppState {
  currentScreen: 'input' | 'loading' | 'list' | 'details' | 'error';
  userInput: string;
  category: string;
  benefits: Benefit[];
  selectedBenefit: Benefit | null;
  actionPlan: string[];
}

// 2. Define the actions
type AppAction =
  | { type: 'START_CLASSIFICATION'; payload: string }
  | { type: 'CLASSIFICATION_SUCCESS'; payload: { category: string; benefits: Benefit[] } }
  | { type: 'CLASSIFICATION_ERROR' }
  | { type: 'SELECT_BENEFIT'; payload: Benefit }
  | { type: 'GENERATE_PLAN_SUCCESS'; payload: string[] }
  | { type: 'GO_TO_SCREEN'; payload: AppState['currentScreen'] }
  | { type: 'RESET' };

// 3. Create the reducer
export const appReducer = (state: AppState, action: AppAction): AppState => {
  switch (action.type) {
    case 'START_CLASSIFICATION':
      return { ...state, currentScreen: 'loading', userInput: action.payload };
    case 'CLASSIFICATION_SUCCESS':
      return { ...state, currentScreen: 'list', category: action.payload.category, benefits: action.payload.benefits };
    case 'CLASSIFICATION_ERROR':
        return { ...state, currentScreen: 'error' };
    case 'SELECT_BENEFIT':
        return { ...state, currentScreen: 'loading', selectedBenefit: action.payload };
    case 'GENERATE_PLAN_SUCCESS':
        return { ...state, currentScreen: 'details', actionPlan: action.payload };
    case 'GO_TO_SCREEN':
        return { ...state, currentScreen: action.payload };
    case 'RESET':
      return initialState;
    default:
      return state;
  }
};

// initialState
export const initialState: AppState = {
  currentScreen: 'input',
  userInput: '',
  category: '',
  benefits: [],
  selectedBenefit: null,
  actionPlan: [],
};

// 4. Context
interface AppContextType {
  state: AppState;
  dispatch: React.Dispatch<AppAction>;
}

export const AppContext = createContext<AppContextType | undefined>(undefined);

// Hook
export const useAppContext = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppContext must be used within AppProvider');
  }
  const { state, dispatch } = context;
  return {
    ...state,
    setScreen: (screen: AppState['currentScreen']) => dispatch({ type: 'GO_TO_SCREEN', payload: screen }),
    setUserInput: (input: string) => dispatch({ type: 'START_CLASSIFICATION', payload: input }),
    setCategory: (category: string) => dispatch({ type: 'CLASSIFICATION_SUCCESS', payload: { category, benefits: state.benefits } }),
    setBenefits: (benefits: Benefit[]) => dispatch({ type: 'CLASSIFICATION_SUCCESS', payload: { category: state.category, benefits } }),
    setSelectedBenefit: (benefit: Benefit) => dispatch({ type: 'SELECT_BENEFIT', payload: benefit }),
    setActionPlan: (plan: string[]) => dispatch({ type: 'GENERATE_PLAN_SUCCESS', payload: plan }),
    resetFlow: () => dispatch({ type: 'RESET' }),
  };
};
