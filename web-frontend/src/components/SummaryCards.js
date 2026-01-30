import React, { useState, useEffect } from 'react';

const CountUp = ({ end, duration = 1000, decimals = 0, enabled = true }) => {
  const [count, setCount] = useState(0);

  useEffect(() => {
    if (!enabled) {
      setCount(end);
      return;
    }

    let startTimestamp = null;
    const step = (timestamp) => {
      if (!startTimestamp) startTimestamp = timestamp;
      const progress = Math.min((timestamp - startTimestamp) / duration, 1);
      // Ease out quart
      const easeProgress = 1 - Math.pow(1 - progress, 4);

      setCount(easeProgress * end);
      if (progress < 1) {
        window.requestAnimationFrame(step);
      }
    };
    window.requestAnimationFrame(step);
  }, [end, duration, enabled]);

  return <>{count.toFixed(decimals)}</>;
};

function SummaryCards({ summary, enableAnimations = true }) {
  if (!summary) {
    return <div className="no-data">No data available. Please upload a CSV file.</div>;
  }

  const cards = [
    {
      title: 'Total Equipment',
      value: summary.total_equipment,
      unit: '',
      decimals: 0,
      icon: '📊',
      color: '#1a5490',
      bgColor: 'rgba(26, 84, 144, 0.1)',
      tooltip: 'Total number of equipment items in the dataset'
    },
    {
      title: 'Avg Flowrate',
      value: summary.average_flowrate,
      unit: 'm³/h',
      decimals: 2,
      icon: '💧',
      color: '#2ecc71',
      bgColor: 'rgba(46, 204, 113, 0.1)',
      tooltip: 'Average flowrate across all equipment'
    },
    {
      title: 'Avg Pressure',
      value: summary.average_pressure,
      unit: 'bar',
      decimals: 2,
      icon: '⚙️',
      color: '#3B82F6',
      bgColor: 'rgba(59, 130, 246, 0.1)',
      tooltip: 'Average pressure across all equipment'
    },
    {
      title: 'Avg Temperature',
      value: summary.average_temperature,
      unit: '°C',
      decimals: 2,
      icon: '🌡️',
      color: '#EF4444',
      bgColor: 'rgba(239, 68, 68, 0.1)',
      tooltip: 'Average temperature across all equipment'
    }
  ];

  return (
    <div className="summary-cards">
      {cards.map((card, index) => (
        <div
          key={index}
          className="summary-card slide-in-up"
          style={{ borderLeft: `5px solid ${card.color}`, animationDelay: `${index * 0.1}s` }}
          title={card.tooltip}
        >
          <div className="card-icon" style={{ backgroundColor: card.bgColor, color: card.color }}>
            {card.icon}
          </div>
          <div className="card-content">
            <h3 className="card-title" style={{ color: '#6B7280', fontSize: '0.875rem' }}>{card.title}</h3>
            <p className="card-value" style={{ color: '#111827', fontWeight: 'bold' }}>
              <CountUp end={card.value} decimals={card.decimals} enabled={enableAnimations} />
            </p>
            {card.unit && <p className="card-unit" style={{ fontSize: '0.8rem', color: '#9CA3AF', marginTop: '2px' }}>{card.unit}</p>}
          </div>
        </div>
      ))}
    </div>
  );
}

export default SummaryCards;
