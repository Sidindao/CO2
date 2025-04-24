import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import NavigationMenu from "../../NavigationMenu";
import { RadialBarChart, RadialBar, Legend, ResponsiveContainer } from 'recharts';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const fetchTransports = async () => {
  const response = await fetch(`${API_BASE_URL}/transport/list`);
  if (!response.ok) {
    throw new Error("Erreur lors de la récupération des modes de transport");
  }
  return response.json();
};

const fetchEmission = async ({ mode_transport }) => {
  const response = await fetch(
    `${API_BASE_URL}/transport/${mode_transport}`
  );
  if (!response.ok) {
    throw new Error("Erreur lors du calcul des émissions");
  }
  return response.json();
};

const TransportCO2Calculator = () => {
  const [modeTransport, setModeTransport] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  // Fetch de la liste des transports
  const { data: transportsData, isLoading: loadingTransports } = useQuery({
    queryKey: ["transportList"],
    queryFn: fetchTransports,
  });

  const handleModeChange = async (e) => {
    const selectedMode = e.target.value;
    setModeTransport(selectedMode);
    setError("");
    setResult(null);

    if (selectedMode) {
      try {
        const emissionData = await fetchEmission({
          mode_transport: selectedMode,
        });
        setResult(emissionData);
      } catch (err) {
        setError(err.message);
      }
    }
  };

  return (
    <section className="bg-white p-6 shadow-lg rounded-lg max-w-3xl mx-auto border mt-6 mb-6">
      <NavigationMenu />

      <div className="mt-4 space-y-4">
        <div>
          <label htmlFor="mode" className="block text-gray-700 font-medium mb-1">
            Mode de transport
          </label>
          <select
            id="mode"
            value={modeTransport}
            onChange={handleModeChange}
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
      </div>

      {error && (
        <div className="mt-4 bg-red-100 text-red-700 p-4 rounded-lg">{error}</div>
      )}

      {result && (
        <div className="mt-6 bg-gray-100 p-4 rounded-md text-center">
          <p className="text-lg text-gray-700 font-semibold">
            {`Émissions de CO₂ par km en ${modeTransport} :`}
          </p>
          <div className="flex justify-center items-center p-4">
            <ResponsiveContainer width="100%" height={300}>
              <RadialBarChart
                innerRadius="70%"
                outerRadius="100%"
                data={[{ name: modeTransport, value: result.emission_par_km }]}
                startAngle={90}
                endAngle={-270}
              >
                <RadialBar
                  minAngle={15}
                  background
                  clockWise
                  dataKey="value"
                  fill="#4CAF50"
                />
                <Legend
                  iconSize={10}
                  layout="vertical"
                  verticalAlign="middle"
                  align="center"
                  content={() => (
                    <div className="flex justify-center items-center text-center">
                      <span className="text-lg font-semibold text-gray-800">
                        {`${modeTransport} : ${result.emission_par_km.toFixed(2)} kg CO₂`}
                      </span>
                    </div>
                  )}
                />
              </RadialBarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </section>
  );
};

export default TransportCO2Calculator;
