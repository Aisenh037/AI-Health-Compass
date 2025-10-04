import React from 'react';
import type { Benefit } from '../services/mockData';

interface Props {
  benefit: Benefit;
  onSelect: () => void;
}

const BenefitCard = ({ benefit, onSelect }: Props) => {
  return (
    <div className="card" onClick={onSelect}>
      <h3 className="card-title">{benefit.title}</h3>
      <p className="card-coverage">{benefit.coverage}</p>
      <p className="card-description">{benefit.description}</p>
    </div>
  );
};

export default BenefitCard;
