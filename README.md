# AI Health Compass

This project is a web-based, multi-screen flow where an employee can describe a health-related need in free text. An AI service classifies the need, recommends suitable benefits, and generates a step-by-step action plan for availing a selected benefit.

## 1. Project Setup & Demo

### Web

To run the application locally, clone the repository and run the following commands:

```bash
# Install all the necessary dependencies
npm install

# Start the local development server
npm start
```

The application will be available at `http://localhost:5173`.

### Demo

Here is a screen recording of the complete user flow:

** *(Note: For your actual submission, you would replace this text with a link to a screen recording or a hosted web link.)*

---

## 2. Problem Understanding

**Goal**: The primary objective is to create a user-friendly interface that simplifies the process of finding and understanding company health benefits. It should accept a natural language query from an employee, classify it into a relevant benefit category (e.g., Dental, Vision), display matching benefits, and provide a clear, actionable plan to use a chosen benefit.

**Assumptions**:
* The benefits data is loaded from a mock JSON file (`mockData.ts`) and not from a live backend API.
* The "AI" logic for classification and action plan generation is simulated in the frontend (`aiService.ts`) to mimic real-world API latency and behavior.

---

## 3. AI Prompts & Iterations

The quality of the AI output is critical. The following prompts were designed to get structured, predictable responses.

#### For Category Classification:

* **Initial Prompt**: `'Classify the following text into Dental, OPD, Vision, Mental Health.'`
    * **Issue**: This prompt often returned a verbose explanation, such as "Based on the text provided, the most relevant category is Dental." This is difficult to parse reliably.
* **Refined Prompt**: `'Return ONLY the category name from {Dental, OPD, Vision, Mental Health} that matches the text: {user_input}. Nothing else.'`
    * **Improvement**: This revised prompt is highly constrained. It explicitly asks for *only* the category name, making the output clean, predictable (e.g., just `"Dental"`), and easy to use directly in the application's logic.

#### For Action Plan Generation:

* **Initial Prompt**: `'How can I use the {benefit_title} benefit?'`
    * **Issue**: This was too open-ended and produced conversational, unstructured paragraphs of text.
* **Refined Prompt**: `'Generate a simple 3-step action plan for an employee to avail the '{benefit_title}' benefit. Return it as a JSON array of strings. For example: ["Step 1: ...", "Step 2: ...", "Step 3: ..."]'`
    * **Improvement**: This prompt requests a specific structure (a JSON array of strings), which can be directly parsed and rendered as a numbered list in the UI, ensuring consistency and a clean user experience.

---

## 4. Architecture & Code Structure

The application is built with **React** and **TypeScript** using **Vite**.

* **Navigation**: The flow between screens is managed in `App.tsx` using conditional rendering based on the `currentScreen` state. This approach is simple and effective for a linear flow without needing a full routing library.
* **Component Structure**: The UI is broken down into modular components:
    * `BenefitInputScreen.tsx`: The initial screen for user input.
    * `LoadingScreen.tsx`: A reusable loading indicator shown during async operations.
    * `BenefitListScreen.tsx`: Displays a grid of `BenefitCard` components.
    * `BenefitDetailsScreen.tsx`: Shows the final action plan.
* **AI Service Abstraction**: All simulated AI calls are handled in `aiService.ts`. This file contains the logic for `classifyNeed` and `generateActionPlan`. This modularity means we could easily swap out the mock logic for real API calls to a backend or a large language model (LLM) without changing the UI components.
* **State Management**: **React Context** (`AppContext.tsx`) is used to provide a centralized state for the entire application. A custom hook, `useAppContext`, offers a clean way for any component to access and update the state (e.g., `currentScreen`, `selectedBenefit`). This avoids "prop drilling" and keeps component logic focused.

---

## 5. Screenshots

**Screen 1: Free-Text Input**


**Screen 2: Benefits Recommendation List**


**Screen 3: Detailed Action Plan**


---

## 6. Known Issues / Improvements

* **Vague Input**: The current keyword-based classification in `aiService.ts` can fail if the user's input is too vague or uses synonyms not accounted for (e.g., "my head hurts" might not map to "OPD").
* **Next Improvement**: Implement a clarifying question fallback. If the AI service returns an `Unknown` category, the UI could ask the user to choose from a list of categories or rephrase their need. For example: "I'm not sure I understand. Are you looking for help with Dental, Vision, or something else?"

---

## 7. Bonus Work

* **Lottie Animation**: A `Lottie`-based loading animation (`LoadingScreen.tsx`) was added to provide a more polished and engaging user experience during the simulated AI processing delays.
* **Fallback/Error State**: An error screen is included for when the AI service cannot classify the user's input, guiding the user to try again. This improves the robustness of the flow.