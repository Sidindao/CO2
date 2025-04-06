import React, { useState } from "react";
import { XAxis, YAxis, Tooltip, BarChart, Bar, ResponsiveContainer } from "recharts";
import { Link } from "react-router"; // Correction ici
import { renderCustomYAxisTick } from "./transportIcon";
import { useQuery } from "@tanstack/react-query";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const fetchComparisonData = async (distance) => {
  const response = await fetch(`${API_BASE_URL}/compare?distance_km=${distance}`);
  if (!response.ok) {
    throw new Error("Erreur lors de la récupération des données");
  }
  return response.json();
};

const CompareEmissions = () => {
  const [distance, setDistance] = useState("");

  // Utilisation de React Query
  const { data, error, isLoading, refetch } = useQuery({
    queryKey: ["compareEmissions", distance], 
    queryFn: () => fetchComparisonData(distance),
    enabled: false, // Désactivé par défaut, on déclenchera `refetch` manuellement
  });

  // Gestion de la soumission du formulaire
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!distance || isNaN(distance) || distance <= 0) {
      alert("Veuillez entrer une distance valide.");
      return;
    }
    refetch(); // Déclenche la requête manuellement
  };

  return (
    <section className="bg-white p-6 shadow-lg rounded-lg max-w-3xl mx-auto border mt-6 mb-6">
      {/* Onglets de navigation */}
      <div className="flex">
        <Link
          to="/"
          className="flex-1 py-2 text-center text-gray-500 bg-green-200 font-medium transition-all"
        >
          Itinéraire
        </Link>
        <Link
          to="/distance"
          className="flex-1 py-2 text-center text-gray-500 bg-white font-medium transition-all"
        >
          Distance
        </Link>
      </div>

      {/* Formulaire de saisie */}
      <form onSubmit={handleSubmit} className="mt-4">
        <div className="flex flex-col">
          <label className="block text-gray-700 font-medium" htmlFor="distance">
            Distance (en km)
          </label>
          <input
            id="distance"
            type="number"
            value={distance}
            onChange={(e) => setDistance(e.target.value)}
            placeholder="Entrez la distance en kilomètres"
            className="w-full border p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            required
          />
        </div>

        {/* Bouton de soumission */}
        <button
          type="submit"
          className="mt-4 w-full bg-green-600 text-white py-2 rounded-md hover:bg-green-700 transition-all"
          disabled={isLoading}
        >
          {isLoading ? "Chargement..." : "Comparer les émissions de CO₂"}
        </button>
      </form>

      {/* Affichage des résultats */}
      {error && (
        <div className="mt-4 bg-red-100 text-red-700 p-4 rounded-lg">
          {error.message}
        </div>
      )}

      {data && data.length > 0 && (
        <div className="mt-4">
          <h2 className="text-center font-semibold text-gray-700">
            Comparaison des émissions de CO₂
          </h2>

          <div className="mt-4 p-4 bg-gray-100 rounded-lg">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart
                layout="vertical"
                data={data}
                margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
              >
                <XAxis
                  dataKey="total_emission"
                  type="number"
                  tickFormatter={(value) => `${value} kg`}
                />
                <YAxis
                  dataKey="mode_transport"
                  type="category"
                  width={120}
                  tick={renderCustomYAxisTick}
                />
                <Tooltip />
                <Bar dataKey="total_emission" fill="#4CAF50" barSize={30} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </section>
  );
};

export default CompareEmissions;
