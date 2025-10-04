import { BENEFIT_CATEGORIES } from '../constants';
import type { BenefitCategory } from '../constants';

export interface Benefit {
  id: string;
  category: BenefitCategory;
  title: string;
  coverage: string;
  description: string;
}

export const benefitsData: Benefit[] = [
  {
    id: 'dental1',
    category: BENEFIT_CATEGORIES.DENTAL,
    title: 'Comprehensive Dental Care',
    coverage: '100% coverage',
    description: 'Full coverage for dental checkups, cleanings, and treatments.',
  },
  {
    id: 'mental1',
    category: BENEFIT_CATEGORIES.MENTAL_HEALTH,
    title: 'Therapy & Counseling',
    coverage: '10 sessions covered',
    description: 'Access to mental health professionals for therapy sessions.',
  },
  {
    id: 'vision1',
    category: BENEFIT_CATEGORIES.VISION,
    title: 'Annual Eye Exam',
    coverage: '100% coverage',
    description: 'Yearly eye examination with coverage for glasses or contacts.',
  },
  {
    id: 'opd1',
    category: BENEFIT_CATEGORIES.OPD,
    title: 'General Physician Consultation',
    coverage: 'Reimbursement up to $100',
    description: 'Consultations with general physicians for routine health issues.',
  },
];
