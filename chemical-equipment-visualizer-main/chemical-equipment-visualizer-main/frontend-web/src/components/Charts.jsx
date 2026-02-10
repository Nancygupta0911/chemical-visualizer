import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';
import './Charts.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

function Charts({ data, summary }) {
  // Equipment Type Distribution Chart
  const typeLabels = Object.keys(summary.type_distribution);
  const typeCounts = Object.values(summary.type_distribution);

  const typeDistributionData = {
    labels: typeLabels,
    datasets: [
      {
        label: 'Equipment Count',
        data: typeCounts,
        backgroundColor: [
          'rgba(255, 99, 132, 0.7)',
          'rgba(54, 162, 235, 0.7)',
          'rgba(255, 206, 86, 0.7)',
          'rgba(75, 192, 192, 0.7)',
          'rgba(153, 102, 255, 0.7)',
          'rgba(255, 159, 64, 0.7)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)',
        ],
        borderWidth: 2,
      },
    ],
  };

  // Average Parameters Chart
  const averageParamsData = {
    labels: ['Flowrate', 'Pressure', 'Temperature'],
    datasets: [
      {
        label: 'Average Values',
        data: [
          summary.avg_flowrate,
          summary.avg_pressure,
          summary.avg_temperature,
        ],
        backgroundColor: [
          'rgba(54, 162, 235, 0.7)',
          'rgba(255, 99, 132, 0.7)',
          'rgba(255, 206, 86, 0.7)',
        ],
        borderColor: [
          'rgba(54, 162, 235, 1)',
          'rgba(255, 99, 132, 1)',
          'rgba(255, 206, 86, 1)',
        ],
        borderWidth: 2,
      },
    ],
  };

  // Parameter Ranges Chart
  const rangesData = {
    labels: ['Flowrate', 'Pressure', 'Temperature'],
    datasets: [
      {
        label: 'Minimum',
        data: [
          summary.min_flowrate,
          summary.min_pressure,
          summary.min_temperature,
        ],
        backgroundColor: 'rgba(75, 192, 192, 0.7)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 2,
      },
      {
        label: 'Maximum',
        data: [
          summary.max_flowrate,
          summary.max_pressure,
          summary.max_temperature,
        ],
        backgroundColor: 'rgba(255, 99, 132, 0.7)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 2,
      },
    ],
  };

  const barOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: false,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  const pieOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'right',
      },
      title: {
        display: false,
      },
    },
  };

  return (
    <div className="charts-container">
      <h2>Data Visualization</h2>
      
      <div className="charts-grid">
        <div className="chart-box">
          <h3>Equipment Type Distribution</h3>
          <div className="chart-wrapper">
            <Pie data={typeDistributionData} options={pieOptions} />
          </div>
        </div>

        <div className="chart-box">
          <h3>Average Parameters</h3>
          <div className="chart-wrapper">
            <Bar data={averageParamsData} options={barOptions} />
          </div>
        </div>

        <div className="chart-box full-width">
          <h3>Parameter Ranges (Min vs Max)</h3>
          <div className="chart-wrapper">
            <Bar data={rangesData} options={barOptions} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Charts;