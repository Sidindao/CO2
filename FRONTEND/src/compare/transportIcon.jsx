

// Fonction pour personnaliser le rendu des ticks de l'axe Y
export const renderCustomYAxisTick = ({ x, y, payload }) => {

  return (
    <g transform={`translate(${x},${y})`}>
      <text fontSize={10} textAnchor="end" fill="#666">
        {payload.value}
      </text>
    </g>
  );
};
