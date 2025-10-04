import { benefitsData } from './mockData';
import type { Benefit } from './mockData';

// A simple delay to simulate network latency
const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

/**
 * AI Prompt (Refined):
 * "Return ONLY the category name from {Dental, OPD, Vision, Mental Health} that matches the text: {user_input}. Nothing else."
 */
export const classifyNeed = async (userInput: string): Promise<string> => {
  console.log(`Classifying user input: "${userInput}"`);
  await sleep(2000); // Simulate AI processing time

  const lowerInput = userInput.toLowerCase();

  if (/\b(tooth|teeth|dental|gums|cavity|root canal|dentist)\b/.test(lowerInput)) {
    return 'Dental';
  }
  if (/\b(stress|anxiety|depressed|sad|mental|therapy|counseling|depression|panic)\b/.test(lowerInput)) {
    return 'Mental Health';
  }
  if (/\b(eye|vision|glasses|blurry|contact lens|optometrist|sight)\b/.test(lowerInput)) {
    return 'Vision';
  }
  if (/\b(doctor|fever|cold|flu|checkup|sick|general practitioner|gp)\b/.test(lowerInput)) {
    return 'OPD';
  }
  if (/\b(diet|nutrition|food|eat|weight|obesity|calories)\b/.test(lowerInput)) {
    return 'Nutrition';
  }
  if (/\b(gym|fitness|exercise|workout|running|swimming|health club)\b/.test(lowerInput)) {
    return 'Fitness';
  }
  if (/\b(diabetes|hypertension|chronic|heart disease|asthma|arthritis)\b/.test(lowerInput)) {
    return 'Chronic Diseases';
  }
  if (/\b(pregnancy|maternity|prenatal|gynecology|women|female)\b/.test(lowerInput)) {
    return "Women's Health";
  }
  if (/\b(prostate|men|male|testosterone)\b/.test(lowerInput)) {
    return "Men's Health";
  }
  if (/\b(child|kid|baby|pediatric|infant|vaccination)\b/.test(lowerInput)) {
    return 'Pediatrics';
  }
  if (/\b(elderly|senior|aging|geriatric|osteoporosis)\b/.test(lowerInput)) {
    return 'Geriatrics';
  }
  if (/\b(emergency|accident|urgent|ambulance|hospital)\b/.test(lowerInput)) {
    return 'Emergency Care';
  }

  // Fallback for unrecognized input
  return 'Unknown';
};

export const getBenefitsByCategory = (category: string): Benefit[] => {
  return benefitsData.filter(b => b.category === category);
};


/**
 * AI Prompt for Action Plan:
 * "Generate a simple 3-step action plan for an employee to avail the '{benefit_title}' benefit. Return it as a JSON array of strings. For example: ["Step 1: ...", "Step 2: ...", "Step 3: ..."]"
 */
export const generateActionPlan = async (benefitTitle: string): Promise<string[]> => {
    console.log(`Generating action plan for: "${benefitTitle}"`);
    await sleep(1500); // Simulate AI processing time

    // Mocked responses based on the benefit title
    const plans: { [key: string]: string[] } = {
        'Comprehensive Dental Care': [
            'Find a network dentist on the company portal.',
            'Schedule an appointment and mention your insurance plan.',
            'The clinic will handle direct billing for covered services.'
        ],
        'Therapy & Counseling': [
            'Visit the employee wellness portal to see our therapy partners.',
            'Request a session directly through the portal.',
            'Your first 10 sessions are fully covered automatically.'
        ],
        'Annual Eye Exam': [
            'Locate an in-network optometrist using our provider search tool.',
            'Book your annual exam.',
            'Present your employee ID at the appointment for 100% coverage.'
        ],
        'General Physician Consultation': [
            'Use our telehealth app to book a virtual appointment.',
            'Consult with the doctor online.',
            'Submit the digital receipt on the portal for reimbursement.'
        ]
    };

    // Return a specific plan or a generic one as a fallback
    return plans[benefitTitle] || [
        'Log in to the main benefits portal.',
        'Search for this specific benefit to see the providers.',
        'Follow the instructions listed on the provider\'s page.'
    ];
};
