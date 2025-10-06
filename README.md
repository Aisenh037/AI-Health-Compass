### **Project: AI-Powered Benefits Discovery Flow (Frontend)**

**Problem Statement 4**

#### **1. Project Setup & Demo**

  * **Technology Stack:** React, TypeScript, Vite, Zustand, Lottie, Axios
  * **Setup Instructions:** To run this project locally, please follow these steps:
    1.  Clone the repository: `git clone <your-github-repo-link>`
    2.  Navigate to the project directory: `cd ai-benefits-discovery-flow`
    3.  Install dependencies: `npm install`
    4.  Start the development server: `npm run dev`
  * **Hosted Demo Link:** http://localhost:5173
  * **GitHub Repository Link:** [Link to your GitHub repository]

#### **2. Problem Understanding**

The goal of this project is to create a seamless, multi-screen experience for an employee to discover company health benefits. The flow allows a user to input a health-related need in free text, which is then classified by an AI into a relevant benefit category. The app then displays suitable benefits and generates a simple, step-by-step action plan for the user's chosen benefit.

  * **Assumptions:**
      * Benefit data (e.g., titles, coverage, descriptions) is loaded from a mock JSON file, and no real backend API calls are made for this data.
      * AI service calls are handled by a dedicated service/module within the frontend.

#### **3. AI Prompts & Iterations**

Crafting precise prompts was essential for getting structured, predictable responses from the AI.

  * **Prompt 1: Benefit Classification**

      * **Initial Prompt:** `'Classify the following text into Dental, OPD, Vision, Mental Health.'`
      * **Issue Encountered:** The model's response was often conversational (e.g., "The category for that would be Dental."), which required extra parsing logic.
      * **Refined Prompt:** `'Return ONLY the category name from {Dental, OPD, Vision, Mental Health} that matches the text: {user_input}. Nothing else.'`

  * **Prompt 2: Action Plan Generation**

      * **Initial Prompt:** `'How can I use the {benefit_title} benefit?'`
      * **Issue Encountered:** The response was unstructured, often a long paragraph that was difficult to format into clear steps.
      * **Refined Prompt:** `'Generate a simple 3-step action plan for an employee to avail the '{benefit_title}' benefit. Return it as a JSON array of strings. For example: ["Step 1: ...", "Step 2: ...", "Step 3: ..."]'`

  * **Fallback & Regeneration Logic**

      * **Fallback:** If the user's input is not recognized, a fallback prompt is used to ask the user to try again.
      * **Regenerate Option:** A "Regenerate" button is available on the action plan screen, which re-sends the refined Action Plan prompt to the AI to get a new set of steps.

#### **4. Architecture & State Management**

  * **Component Structure:** The application is divided into four main screens/components:
      * `BenefitInputScreen`: Contains the initial text input field.
      * `LoadingScreen`: Shows a loading indicator while the AI classifies the input.
      * `BenefitListScreen`: Displays the benefit cards that match the classified category.
      * `BenefitDetailsScreen`: Displays the final AI-generated 3-step action plan.
  * **Navigation:** The flow between screens is managed in `App.tsx` using conditional rendering based on the `currentScreen` state. This approach is simple and effective for a linear flow without needing a full routing library.
  * **AI Service:** All simulated AI calls are managed within a dedicated service file (`src/services/aiService.ts`). This centralizes the logic for making requests, handling responses, and managing errors.
  * **State Management:** Zustand (`appStore.ts`) is used for centralized state management with persistence and devtools support. It provides a clean store with actions for updating state (e.g., `setScreen`, `startClassification`, `selectBenefit`). This avoids prop drilling and includes middleware for debugging and local storage persistence.

#### **5. Screenshots / Screen Recording**

*[Reminder: Embed your actual screenshots in the README/DOC file. If you made a mobile app, replace this section with a link to your screen recording.]*

**Screen 1: Free-Text Input**

**Screen 2: AI Classification & Loading**

**Screen 3: Benefit Cards Display**

**Screen 4: Generated Action Plan**

#### **6. Known Issues & Potential Improvements**

  * **Known Issues:**
      * The AI can occasionally misclassify vague or multi-faceted inputs (e.g., "my head hurts" might not map to "OPD").
      * There is no persistent state; refreshing the page resets the entire flow.
  * **Potential Improvements:**
      * Introduce a clarifying question step. If the AI's confidence in a category is low, it could ask the user a follow-up question.
      * Add `localStorage` to persist the user's journey so they can continue where they left off after a page refresh.
      * Implement user feedback (e.g., a "thumbs up/down" on the action plan) to help refine prompts over time.

#### **7. Bonus Work**

  * Added sleek loading animations using the Lottie library to improve the user experience during wait times.
  * Implemented a fallback/error state for when the AI service cannot classify the user's input, guiding the user to try again. This improves the robustness of the flow.
