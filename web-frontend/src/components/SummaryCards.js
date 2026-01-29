import React from 'react';

function SummaryCards({ summary }) {
  if (!summary) {
    return <div className="no-data">No data available. Please upload a CSV file.</div>;
  }

  const cards = [
    {
      title: 'Total Equipment',
      value: summary.total_equipment,
      icon: '📊',
      color: '#1a5490',
      bgColor: 'rgba(26, 84, 144, 0.1)'
    },
    {
      title: 'Avg Flowrate',
      value: summary.average_flowrate.toFixed(2),
      icon: '💧',
      color: '#2ecc71',
      bgColor: 'rgba(46, 204, 113, 0.1)'
    },
    {
      title: 'Avg Pressure',
      value: summary.average_pressure.toFixed(2),
      icon: '⚙️',
      color: '#3B82F6',
      bgColor: 'rgba(59, 130, 246, 0.1)'
    },
    {
      title: 'Avg Temperature',
      value: summary.average_temperature.toFixed(2),
      icon: '🌡️',
      color: '#EF4444',
      bgColor: 'rgba(239, 68, 68, 0.1)'
    }
  ];

  return (
    <div className="summary-cards">
      {cards.map((card, index) => (
        <div key={index} className="summary-card" style={{ borderTop: `4px solid ${card.color}` }}>
          <div className="card-icon" style={{ backgroundColor: card.bgColor, color: card.color }}>
            {card.icon}
          </div>
          <div className="card-content">
            <h3 className="card-title" style={{ color: '#6B7280', fontSize: '0.875rem' }}>{card.title}</h3>
            <p className="card-value" style={{ color: '#111827', fontWeight: 'bold' }}>
              {card.value}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}

export default SummaryCards;
