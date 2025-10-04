// src/components/BenefitDetailsScreen.tsx
import { useAppStore } from '../stores/appStore';
import { generateActionPlan } from '../services/aiService';

const BenefitDetailsScreen = () => {
  const { selectedBenefit, actionPlan, setScreen, generatePlanSuccess } = useAppStore();

  const handleRegenerate = async () => {
    if (!selectedBenefit) return;
    // In a real app, you might add a flag to the prompt to get a different response
    console.log("Regenerating plan...");
    try {
      const newPlan = await generateActionPlan(selectedBenefit.title);
      generatePlanSuccess(newPlan);
    } catch (error) {
      console.error('Error regenerating plan:', error);
    }
  };

  if (!selectedBenefit) {
    return (
        <div className="container">
            <p>Something went wrong. Please start over.</p>
            <button onClick={() => setScreen('input')} className="back-button">Go Back</button>
        </div>
    );
  }

  return (
    <div className="container">
      <button onClick={() => setScreen('list')} className="back-button">&larr; Back to List</button>
      <h2 className="title">{selectedBenefit.title}</h2>
      <p className="coverage">Coverage: {selectedBenefit.coverage}</p>
      <p className="subtitle">{selectedBenefit.description}</p>

      <div className="action-plan">
        <h3>Your 3-Step Action Plan:</h3>
        {actionPlan.length > 0 ? (
            <ol className="plan-steps">
                {actionPlan.map((step, index) => (
                    <li key={index}>{step}</li>
                ))}
            </ol>
        ) : (
            <p>Generating your action plan...</p>
        )}
      </div>

      <button onClick={handleRegenerate} className="regenerate-button">
        Regenerate Plan
      </button>
    </div>
  );
};

export default BenefitDetailsScreen;