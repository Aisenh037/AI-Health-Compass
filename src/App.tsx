import React, { useEffect } from 'react';
import { useAppStore } from './stores/appStore';
import BenefitInputScreen from './components/BenefitInputScreen';
import LoadingScreen from './components/LoadingScreen';
import BenefitListScreen from './components/BenefitListScreen';
import BenefitDetailsScreen from './components/BenefitDetailsScreen';
import { SpeedInsights } from '@vercel/speed-insights/react';
import './App.css';

const App = () => {
  const { currentScreen, reset, darkMode, toggleDarkMode } = useAppStore();

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  const renderScreen = () => {
    switch (currentScreen) {
      case 'input':
        return <BenefitInputScreen />;
      case 'loading':
        return <LoadingScreen />;
      case 'list':
        return <BenefitListScreen />;
      case 'details':
        return <BenefitDetailsScreen />;
      case 'error':
        return (
          <div className="container center-content">
            <h2 className="title">Sorry, we couldn't recognize that.</h2>
            <p className="subtitle">Please try describing your need differently.</p>
            <button onClick={reset} className="submit-button">Try Again</button>
          </div>
        );
      default:
        return <BenefitInputScreen />;
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>AI Health Compass</h1>
        <button
          onClick={toggleDarkMode}
          className="dark-mode-toggle"
        >
          {darkMode ? '☀️ Light' : '🌙 Dark'}
        </button>
      </header>
      <main>
        {renderScreen()}
      </main>
      <SpeedInsights />
    </div>
  );
}

export default App;
