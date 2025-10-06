import React, { useState } from 'react';
import { useAppStore } from '../stores/appStore';
import { generateActionPlan, regenerateBenefits } from '../services/aiService';
import BenefitCard from './BenefitCard';
import type { Benefit } from '../services/mockData';

const BenefitListScreen = () => {
  const { category, benefits, selectBenefit, generatePlanSuccess, reset, regenerateBenefits: updateBenefits } = useAppStore();
  const [isRegenerating, setIsRegenerating] = useState(false);

  const handleSelectBenefit = async (benefit: Benefit) => {
    selectBenefit(benefit);

    try {
      const plan = await generateActionPlan(benefit.title);
      generatePlanSuccess(plan);
    } catch (error) {
      // Handle error - could add error state for plan generation
      console.error('Error generating action plan:', error);
    }
  };

  const handleRegenerate = async () => {
    setIsRegenerating(true);
    try {
      const newBenefits = await regenerateBenefits(category);
      updateBenefits(newBenefits);
    } catch (error) {
      console.error('Error regenerating benefits:', error);
    } finally {
      setIsRegenerating(false);
    }
  };

  return (
    <div className="container">
      <button onClick={reset} className="back-button">&larr; Start Over</button>
      <h2 className="title">Recommended for you</h2>
      <p className="subtitle">Based on your need, we found benefits in the <strong>{category}</strong> category.</p>
      <button onClick={handleRegenerate} disabled={isRegenerating} className="regenerate-button">
        {isRegenerating ? 'Regenerating...' : '🔄 Regenerate Benefits'}
      </button>
      <div className="card-grid">
        {benefits.map(benefit => (
          <BenefitCard key={benefit.id} benefit={benefit} onSelect={() => handleSelectBenefit(benefit)} />
        ))}
      </div>
    </div>
  );
};

export default BenefitListScreen;
