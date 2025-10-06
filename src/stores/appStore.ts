import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import type { Benefit } from '../services/mockData';

interface AppState {
  currentScreen: 'input' | 'loading' | 'list' | 'details' | 'error' | 'chat';
  userInput: string;
  category: string;
  benefits: Benefit[];
  selectedBenefit: Benefit | null;
  actionPlan: string[];
  error: string | null;
  isLoading: boolean;
  chatMessages: { role: 'user' | 'ai'; content: string }[];
}

interface AppActions {
  setScreen: (screen: AppState['currentScreen']) => void;
  setUserInput: (input: string) => void;
  setCategory: (category: string) => void;
  setBenefits: (benefits: Benefit[]) => void;
  setSelectedBenefit: (benefit: Benefit | null) => void;
  setActionPlan: (plan: string[]) => void;
  setError: (error: string | null) => void;
  setLoading: (loading: boolean) => void;
  startClassification: (input: string) => void;
  classificationSuccess: (category: string, benefits: Benefit[]) => void;
  classificationError: (error: string) => void;
  selectBenefit: (benefit: Benefit) => void;
  generatePlanSuccess: (plan: string[]) => void;
  reset: () => void;
}

const initialState: AppState = {
  currentScreen: 'input',
  userInput: '',
  category: '',
  benefits: [],
  selectedBenefit: null,
  actionPlan: [],
  error: null,
  isLoading: false,
  chatMessages: [],
};

export const useAppStore = create<AppState & AppActions>()(
  devtools(
    persist(
      (set) => ({
        ...initialState,

        setScreen: (screen) => set({ currentScreen: screen }),
        setUserInput: (input) => set({ userInput: input }),
        setCategory: (category) => set({ category }),
        setBenefits: (benefits) => set({ benefits }),
        setSelectedBenefit: (benefit) => set({ selectedBenefit: benefit }),
        setActionPlan: (plan) => set({ actionPlan: plan }),
        setError: (error) => set({ error, currentScreen: 'error' }),
        setLoading: (loading) => set({ isLoading: loading }),

        startClassification: (input) => set({
          currentScreen: 'loading',
          userInput: input,
          isLoading: true,
          error: null
        }),

        classificationSuccess: (category, benefits) => set({
          currentScreen: 'list',
          category,
          benefits,
          isLoading: false,
          error: null
        }),

        classificationError: (error) => set({
          currentScreen: 'error',
          error,
          isLoading: false
        }),

        selectBenefit: (benefit) => set({
          currentScreen: 'loading',
          selectedBenefit: benefit,
          isLoading: true
        }),

        generatePlanSuccess: (plan) => set({
          currentScreen: 'details',
          actionPlan: plan,
          isLoading: false
        }),

        reset: () => set(initialState),
      }),
      {
        name: 'ai-benefits-store',
        partialize: (state) => ({
          userInput: state.userInput,
          category: state.category,
          // Persist user preferences but not sensitive data
        }),
      }
    ),
    {
      name: 'app-store',
    }
  )
);
