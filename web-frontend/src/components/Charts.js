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

function Charts({ summary, data }) {
  if (!summary) {
    return <div className="no-data">No data available for charts.</div>;
  }

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
      },
    ],
  };

  const barOptions = {
    responsive: true,
    maintainAspectRatio: false,
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
    },
    scales: {
      y: {
        beginAtZero: true,
      },
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
      },
    ],
  };

  const pieOptions = {
    responsive: true,
    maintainAspectRatio: false,
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
  const lineData = data ? {
    labels: data.map((_, index) => index + 1),
    datasets: [
      {
        label: 'Flowrate',
        data: data.map(d => d.Flowrate),
        borderColor: 'rgba(46, 204, 113, 1)',
        backgroundColor: 'rgba(46, 204, 113, 0.2)',
        tension: 0.4,
        pointHoverRadius: 8,
        pointHitRadius: 20,
      },
      {
        label: 'Pressure',
        data: data.map(d => d.Pressure),
        borderColor: 'rgba(59, 130, 246, 1)',
        backgroundColor: 'rgba(59, 130, 246, 0.2)',
        tension: 0.4,
        pointHoverRadius: 8,
        pointHitRadius: 20,
      },
      {
        label: 'Temperature',
        data: data.map(d => d.Temperature),
        borderColor: 'rgba(239, 68, 68, 1)',
        backgroundColor: 'rgba(239, 68, 68, 0.2)',
        tension: 0.4,
        pointHoverRadius: 8,
        pointHitRadius: 20,
      },
    ],
  } : null;

  const lineOptions = {
    responsive: true,
    maintainAspectRatio: false,
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
        }
      },
      y: {
        display: true,
        title: {
          display: true,
          text: 'Value'
        }
      }
    }
  };

  return (
    <div className="charts-container">
      <div className="chart-wrapper">
        <div className="chart-box">
          <Bar data={barData} options={barOptions} />
        </div>
      </div>

      <div className="chart-wrapper">
        <div className="chart-box">
          <Pie data={pieData} options={pieOptions} />
        </div>
      </div>

      {lineData && (
        <div className="chart-wrapper" style={{ flexBasis: '100%', maxWidth: '100%' }}>
          <div className="chart-box">
            <Line data={lineData} options={lineOptions} />
          </div>
        </div>
      )}
    </div>
  );
}

export default Charts;
