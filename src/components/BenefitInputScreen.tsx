// src/components/BenefitInputScreen.tsx
import { useState } from 'react';
import { useAppStore } from '../stores/appStore';
import { classifyNeed, getBenefitsByCategory } from '../services/aiService';

const BenefitInputScreen = () => {
  const [inputValue, setInputValue] = useState('');
  const { startClassification, classificationSuccess, classificationError } = useAppStore();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    startClassification(inputValue);

    try {
      const category = await classifyNeed(inputValue);

      if (category === 'Unknown') {
        classificationError('We couldn\'t classify your input. Please try describing your need differently.');
      } else {
        const recommendedBenefits = getBenefitsByCategory(category);
        classificationSuccess(category, recommendedBenefits);
      }
    } catch {
      classificationError('An error occurred while processing your request. Please try again.');
    }
  };

  return (
    <div className="container">
      <h1 className="title">How can we help you today?</h1>
      <p className="subtitle">Describe your health need, and we'll find the right benefits for you.</p>
      <form onSubmit={handleSubmit} className="input-form">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          className="text-input"
          placeholder="e.g., 'I have tooth pain, what can I do?'"
        />
        <button type="submit" className="submit-button" disabled={!inputValue.trim()}>
          Find Benefits
        </button>
      </form>
    </div>
  );
};

export default BenefitInputScreen;