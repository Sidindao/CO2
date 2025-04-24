import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import NavigationMenu from "../../NavigationMenu";
import { RadialBarChart, RadialBar, Legend, ResponsiveContainer, Tooltip } from 'recharts';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const fetchTransports = async () => {
  const response = await fetch(`${API_BASE_URL}/transport/list`);
  if (!response.ok) {
    throw new Error("Erreur lors de la récupération des modes de transport");
  }
  return response.json();
};

const fetchEmission = async ({ mode_transport, distance_km }) => {
  const response = await fetch(
    `${API_BASE_URL}/distance/calculate?mode_transport=${mode_transport}&distance_km=${distance_km}`
  );
  if (!response.ok) {
    throw new Error("Erreur lors du calcul des émissions");
  }
  return response.json();
};

const DistanceCalculator = () => {
  const [modeTransport, setModeTransport] = useState("");
  const [distance, setDistance] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  // Fetch de la liste des transports
  const { data: transportsData, isLoading: loadingTransports } = useQuery({
    queryKey: ["transportList"],
    queryFn: fetchTransports,
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);

    if (!modeTransport || !distance || distance <= 0) {
      setError("Veuillez sélectionner un mode de transport et entrer une distance valide.");
      return;
    }

    try {
      const emissionData = await fetchEmission({
        mode_transport: modeTransport,
        distance_km: distance,
      });
      setResult(emissionData);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <section className="bg-white p-6 shadow-lg rounded-lg max-w-3xl mx-auto border mt-6 mb-6">
      <NavigationMenu />

      <form onSubmit={handleSubmit} className="mt-4 space-y-4">
        <div>
          <label htmlFor="mode" className="block text-gray-700 font-medium mb-1">
            Mode de transport
          </label>
          <select
            id="mode"
            value={modeTransport}
            onChange={(e) => setModeTransport(e.target.value)}
            className="w-full border p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            required
          >
            <option value="">-- Sélectionner --</option>
            {loadingTransports ? (
              <option disabled>Chargement...</option>
            ) : (
              transportsData?.modes_transports.map((mode) => (
                <option key={mode} value={mode}>
                  {mode}
                </option>
              ))
            )}
          </select>
        </div>

        <div>
          <label htmlFor="distance" className="block text-gray-700 font-medium mb-1">
            Distance (en km)
          </label>
          <input
            id="distance"
            type="number"
            value={distance}
            onChange={(e) => setDistance(e.target.value)}
            placeholder="Entrez la distance"
            className="w-full border p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            required
          />
        </div>

        <button
          type="submit"
          className="w-full bg-green-600 text-white py-2 rounded-md hover:bg-green-700 transition-all"
        >
          Calculer les émissions
        </button>
      </form>

      {error && (
        <div className="mt-4 bg-red-100 text-red-700 p-4 rounded-lg">{error}</div>
      )}

      {result && (
        <div className="mt-6 bg-gray-100 p-4 rounded-md text-center">
          <p className="text-lg text-gray-700 font-semibold">
            {`Émissions de CO₂ pour ${distance} km en ${modeTransport} :`}
          </p>
          <div className="flex justify-center items-center p-4">
      <ResponsiveContainer width="100%" height={300}>
        <RadialBarChart
          width={730} 
          height={250} 
          innerRadius="10%" 
          outerRadius="80%" 
          data={[{ name: 'Émissions CO₂', value: result.total_emission, fill: '#3b82f6' },{ name: 'Équiv. en arbres', value: result.equivalent_en_arbre, fill: '#4CAF50' }]}
          startAngle={180} 
          endAngle={0}
        >
          <RadialBar
            minAngle={15}
            background
            clockWise={true}
            label={{ fill: '#666', position: 'insideMiddle' }}
            dataKey="value"
            fill="#4CAF50"
          />
          <Legend iconSize={10} width={120} height={140} layout='vertical' verticalAlign='middle' align="right" />
          <Tooltip />
        </RadialBarChart>
      </ResponsiveContainer>
    </div>
        </div>
      )}
    </section>
  );
};

export default DistanceCalculator;
