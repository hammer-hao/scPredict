import React, { useEffect, useRef } from 'react';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

const LineChart = ({ winRates }) => {
  const chartRef = useRef(null);
  const chartInstanceRef = useRef(null);

  const formatTime = (index) => {
    const totalSeconds = index * 5;
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  useEffect(() => {
    if (chartInstanceRef.current) {
      chartInstanceRef.current.destroy();
    }

    const ctx = chartRef.current.getContext('2d');
    chartInstanceRef.current = new Chart(ctx, {
      type: 'line',
      data: {
        labels: winRates.map((_, index) => formatTime(index)),
        datasets: [
          {
            label: 'Win Rates For Player 1',
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
    <div style={{ width: '80%', height: '480px', margin: 'auto' }}>
      <canvas ref={chartRef} />
    </div>
  );
};

export default LineChart;