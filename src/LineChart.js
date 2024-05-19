import React, { useEffect, useRef } from 'react';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

const LineChart = ({ winRates }) => {
  const chartRef = useRef(null);
  const chartInstanceRef = useRef(null);

  useEffect(() => {
    if (chartInstanceRef.current) {
      chartInstanceRef.current.destroy();
    }

    const ctx = chartRef.current.getContext('2d');
    chartInstanceRef.current = new Chart(ctx, {
      type: 'line',
      data: {
        labels: winRates.map((_, index) => `Time ${index}`),
        datasets: [
          {
            label: 'Win Rate Over Time',
            data: winRates,
            fill: false,
            borderColor: 'rgba(75,192,192,1)',
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false, // Allow custom sizing
        scales: {
          x: {
            type: 'category',
          },
          y: {
            type: 'linear',
            min: 0,
            max: 1, // Set Y-axis range from 0 to 1
            beginAtZero: true,
          },
        },
      },
    });
  }, [winRates]);

  return (
    <div style={{ width: '80%', height: '400px', margin: 'auto' }}>
      <canvas ref={chartRef} />
    </div>
  );
};

export default LineChart;