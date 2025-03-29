import React from "react";
import { Link } from "react-router";

import { useMutation } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import {  XAxis, YAxis, Tooltip, BarChart, Bar, ResponsiveContainer } from 'recharts';
import { renderCustomYAxisTick } from "./transportIcon";


const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;



const Itinerary = () => {
  const [departure, setDeparture] = useState("");
  const [arrival, setArrival] = useState("");
  const [roundTrip, setRoundTrip] = useState(false);
  const [data, setData] = useState([]);

  useEffect(() => {
    // Données de test pour le graphique
    setData([
      { mode: 'Voiture', co2:12 },
      { mode: 'Train', co2: 50 },
      { mode: 'Avion', co2: 250 },
      { mode: 'Bateau', co2: 75 },
      { mode: 'Bus', co2: 40 },
    ]);
  }, []);

  // Fonction de soumission
  const handleSubmit = (e) => {
    e.preventDefault();
    mutation.mutate(); // Envoie les données au serveur
  };

  const mutation = useMutation({
    mutationFn: async () => {
      const response = await fetch(`${API_BASE_URL}/itinerary`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ departure, arrival, roundTrip }),
      });

      if (!response.ok) {
        throw new Error("Erreur lors de la requête");
      }

      return response.json();
    },
  });

  return (
    <section className="bg-white p-6 shadow-lg rounded-lg max-w-3xl mx-auto border mt-6 mb-6">
      {/* Onglets de navigation avec Link */}
      <div className="flex">
        <Link
          to="/"
          className="flex-1 py-2 text-center text-gray-500 bg-white  font-medium transition-all"
        >
          Itinéraire
        </Link>
        <Link
          to="/distance"
          className="flex-1 py-2 text-center text-gray-500 bg-green-200 font-medium transition-all"
        >
          Distance
        </Link>
      </div>

      {/* Formulaire de saisie */}
      <form onSubmit={handleSubmit} className="mt-4">
        <div className="flex gap-4">
          <div className="flex-1">
            <label className="block text-gray-700 font-medium"  htmlFor="departure">Départ</label>
            <input
              id="departure"
              type="text"
              value={departure}
              onChange={(e) => setDeparture(e.target.value)}
              placeholder="Entrer le point de départ"
              className="w-full border p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
          <div className="flex-1">
            <label className="block text-gray-700 font-medium" htmlFor="arrival" >Arrivée</label>
            <input
              id="arrival"
              type="text" 
              value={arrival}
              onChange={(e) => setArrival(e.target.value)}
              placeholder="Entrer le point d’arrivée"
              className="w-full border p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
        </div>

        {/* Checkbox Aller/Retour */}
        <div className="mt-4 flex items-center">
          <input
            type="checkbox"
            id="roundTrip"
            checked={roundTrip}
            onChange={() => setRoundTrip(!roundTrip)}
            className="mr-2"
          />
          <label htmlFor="roundTrip" className="text-gray-700">
            Aller/Retour
          </label>
        </div>

        {/* Bouton de soumission */}
        <button
          type="submit"
          className="mt-4 w-full bg-green-600 text-white py-2 rounded-md hover:bg-green-700 transition-all"
          disabled={mutation.isPending}
        >
          {mutation.isPending
            ? "Calcul en cours..."
            : "Calculer les émissions de CO₂"}
        </button>
      </form>

      {/* Affichage des résultats */}
      {mutation.isSuccess || (
        <div className="mt-4">
        <h2 className="text-center font-semibold text-gray-700">
          Comparaison des émissions de CO₂
        </h2>

        <div className="mt-4 p-4 bg-gray-100 rounded-lg">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart
              layout="vertical"
              data={data} // Données du backend
              margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
            >
              <XAxis dataKey="co2" type="number" tickFormatter={(value) => `${value} kg`} />
              <YAxis 
                dataKey="mode" 
                type="category" 
                width={120} 
                tick={renderCustomYAxisTick}
              />
              <Tooltip />
              <Bar dataKey="co2" fill="#4CAF50" barSize={30} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
      )}

      {mutation.isError && (
        <div className="mt-4 bg-red-100 text-red-700 p-4 rounded-lg">
          error
          </div>
      )}
    </section>
  );
};

export default Itinerary;
