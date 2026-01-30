import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { Bar, Pie, Line } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

function Charts({ summary, data, enableAnimations = true }) {
  if (!summary) {
    return <div className="no-data">No data available for charts.</div>;
  }

  // Animation configuration
  const animationOptions = {
    duration: enableAnimations ? 1000 : 0,
    easing: 'easeInOutQuart',
  };

  // Bar chart data - Average Parameters
  const barData = {
    labels: ['Flowrate', 'Pressure', 'Temperature'],
    datasets: [
      {
        label: 'Average Values',
        data: [
          summary.average_flowrate,
          summary.average_pressure,
          summary.average_temperature,
        ],
        backgroundColor: [
          'rgba(46, 204, 113, 0.8)', // Flowrate (Green)
          'rgba(59, 130, 246, 0.8)', // Pressure (Blue)
          'rgba(239, 68, 68, 0.8)',  // Temperature (Red)
        ],
        borderColor: [
          'rgba(46, 204, 113, 1)',
          'rgba(59, 130, 246, 1)',
          'rgba(239, 68, 68, 1)',
        ],
        borderWidth: 2,
        borderRadius: 8, // Pseudo-3D effect: rounded corners
        borderSkipped: false,
        hoverBackgroundColor: [
          'rgba(46, 204, 113, 1)',
          'rgba(59, 130, 246, 1)',
          'rgba(239, 68, 68, 1)',
        ],
        hoverBorderWidth: 3,
        hoverOffset: 4,
      },
    ],
  };

  const barOptions = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      ...animationOptions,
      y: {
        from: 0,
      }
    },
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: 'Average Equipment Parameters',
        font: {
          size: 16,
          weight: 'bold',
        },
      },
      tooltip: {
        callbacks: {
          label: (context) => `Value: ${context.parsed.y.toFixed(2)}`
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
        }
      },
      x: {
        grid: {
          display: false,
        }
      }
    },
  };

  // Pie chart data - Equipment Type Distribution
  const typeLabels = Object.keys(summary.type_distribution);
  const typeValues = Object.values(summary.type_distribution);

  const pieData = {
    labels: typeLabels,
    datasets: [
      {
        label: 'Equipment Count',
        data: typeValues,
        backgroundColor: [
          'rgba(26, 84, 144, 0.8)',
          'rgba(46, 204, 113, 0.8)',
          'rgba(239, 68, 68, 0.8)',
          'rgba(243, 156, 18, 0.8)',
          'rgba(155, 89, 182, 0.8)',
          'rgba(52, 152, 219, 0.8)',
        ],
        borderColor: [
          'rgba(26, 84, 144, 1)',
          'rgba(46, 204, 113, 1)',
          'rgba(239, 68, 68, 1)',
          'rgba(243, 156, 18, 1)',
          'rgba(155, 89, 182, 1)',
          'rgba(52, 152, 219, 1)',
        ],
        borderWidth: 2,
        hoverOffset: 15, // Pie expansion effect
      },
    ],
  };

  const pieOptions = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      ...animationOptions,
      animateRotate: true,
      animateScale: true,
    },
    plugins: {
      legend: {
        position: 'right',
      },
      title: {
        display: true,
        text: 'Equipment Type Distribution',
        font: {
          size: 16,
          weight: 'bold',
        },
      },
    },
  };

  // Line chart data - Trends
  // Downsample data for readability (show every 10th point if > 100 points)
  const step = data && data.length > 100 ? 10 : 1;
  const filteredData = data ? data.filter((_, i) => i % step === 0) : [];

  const lineData = data ? {
    labels: filteredData.map((_, index) => (index * step) + 1),
    datasets: [
      {
        label: 'Flowrate',
        data: filteredData.map(d => d.Flowrate),
        borderColor: 'rgba(46, 204, 113, 0.8)', // Slight transparency
        backgroundColor: 'rgba(46, 204, 113, 0.1)', // Lower opacity
        tension: 0.4,
        pointRadius: 2, // Smaller points
        pointHoverRadius: 6,
        fill: true,
      },
      {
        label: 'Pressure',
        data: filteredData.map(d => d.Pressure),
        borderColor: 'rgba(59, 130, 246, 0.8)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4,
        pointRadius: 2,
        pointHoverRadius: 6,
        fill: true,
      },
      {
        label: 'Temperature',
        data: filteredData.map(d => d.Temperature),
        borderColor: 'rgba(239, 68, 68, 0.8)',
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        tension: 0.4,
        pointRadius: 2,
        pointHoverRadius: 6,
        fill: true,
      },
    ],
  } : null;

  const lineOptions = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      ...animationOptions,
      x: {
        type: 'number',
        easing: 'linear',
        duration: enableAnimations ? 2000 : 0, // Slower drawing for line
        from: NaN,
        delay: (ctx) => {
          if (ctx.type !== 'data' || ctx.xStarted) {
            return 0;
          }
          ctx.xStarted = true;
          return ctx.index * 5;
        }
      },
    },
    plugins: {
      title: {
        display: true,
        text: 'Parameter Trends',
        font: {
          size: 16,
          weight: 'bold',
        },
      },
      tooltip: {
        mode: 'index',
        intersect: false,
      },
    },
    hover: {
      mode: 'nearest',
      intersect: true
    },
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: 'Equipment Index'
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
        }
      },
      y: {
        display: true,
        title: {
          display: true,
          text: 'Value'
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
        }
      }
    }
  };

  return (
    <div className="charts-container">
      <div className="chart-wrapper slide-in-up" style={{ animationDelay: '0.1s' }}>
        <div className="chart-box">
          <Bar data={barData} options={barOptions} />
        </div>
      </div>

      <div className="chart-wrapper slide-in-up" style={{ animationDelay: '0.2s' }}>
        <div className="chart-box">
          <Pie data={pieData} options={pieOptions} />
        </div>
      </div>

      {lineData ? (
        <div className="chart-wrapper slide-in-up" style={{ flexBasis: '100%', maxWidth: '100%', animationDelay: '0.3s' }}>
          <div className="chart-box">
            <Line data={lineData} options={lineOptions} />
          </div>
        </div>
      ) : (
        <div className="chart-wrapper slide-in-up" style={{ flexBasis: '100%', maxWidth: '100%', animationDelay: '0.3s' }}>
          <div className="chart-box loading-chart">
            <p>Loading chart data...</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default Charts;
