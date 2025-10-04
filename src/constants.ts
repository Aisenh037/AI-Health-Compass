// src/constants.ts

export const BENEFIT_CATEGORIES = {
  DENTAL: 'Dental',
  MENTAL_HEALTH: 'Mental Health',
  VISION: 'Vision',
  OPD: 'OPD',
  NUTRITION: 'Nutrition',
  FITNESS: 'Fitness',
  CHRONIC_DISEASES: 'Chronic Diseases',
  WOMENS_HEALTH: "Women's Health",
  MENS_HEALTH: "Men's Health",
  PEDIATRICS: 'Pediatrics',
  GERIATRICS: 'Geriatrics',
  EMERGENCY_CARE: 'Emergency Care',
} as const; // 'as const' makes the values readonly and specific

// We can also create a Type from these values to use in our interfaces
type ObjectValues<T> = T[keyof T];
export type BenefitCategory = ObjectValues<typeof BENEFIT_CATEGORIES>;