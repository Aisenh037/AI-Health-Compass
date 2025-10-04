// src/components/LoadingScreen.tsx
import Lottie from 'lottie-react';
import loadingAnimation from '../assets/loading-animation.json';

const LoadingScreen = () => {
  return (
    <div className="container center-content">
      <div style={{ width: 200 }}>
        <Lottie animationData={loadingAnimation} loop={true} />
      </div>
      <p className="loading-text">Analyzing your needs...</p>
    </div>
  );
};

export default LoadingScreen;