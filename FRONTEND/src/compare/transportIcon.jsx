// src/utils/transportIcons.js
import { FaCar, FaTrain, FaPlane, FaBus, FaBicycle, FaSubway } from 'react-icons/fa';

const transportIcons = {
  'Car - Electric': <FaCar />,
  'Car - Plug-in Hybrid': <FaCar />,
  'Car - Mild Hybrid': <FaCar />,
  'Car - High-end Mild Hybrid': <FaCar />,
  'Bus': <FaBus />,
  'Metro': <FaSubway />,
  'Tramway': <FaTrain />,
  'RER': <FaTrain />,
  'TER': <FaTrain />,
  'Plane': <FaPlane />,
  'TGV': <FaTrain />,
  'Bike': <FaBicycle />,
};

// Fonction pour personnaliser le rendu des ticks de l'axe Y
export const renderCustomYAxisTick = ({ x, y, payload }) => {
  const icon = transportIcons[payload.value] || null;

  return (
    <g transform={`translate(${x},${y})`}>
      {icon && (
        <foreignObject  x={-30} y={-10} width={24} height={24}>
          {icon} 
        </foreignObject>
      )}
      <text x={-100} y={-4} dy={10} textAnchor="start" fill="#666">
        {payload.value}
      </text>
    </g>
  );
};
