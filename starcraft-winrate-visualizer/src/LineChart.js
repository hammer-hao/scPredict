import React, { useEffect, useRef } from 'react';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

const LineChart = ({ winRates, playerName, onPointClick }) => {
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
            label: `Predicted Win Probability: ${playerName}`,
            data: winRates,
            fill: false,
            borderColor: 'rgba(75,192,192,1)',
            pointBackgroundColor: 'rgba(75,192,192,1)',
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            type: 'category',
          },
          y: {
            type: 'linear',
            min: 0,
            max: 1,
            beginAtZero: true,
          },
        },
        onClick: (event) => {
          const points = chartInstanceRef.current.getElementsAtEventForMode(event, 'nearest', { intersect: true }, true);
          if (points.length) {
            const index = points[0].index;
            onPointClick(index);
          }
        },
      },
    });
  }, [winRates, playerName]);

  return (
    <div style={{ width: '100%', height: '480px' }}>
      <canvas ref={chartRef} />
    </div>
  );
};

export default LineChart;
