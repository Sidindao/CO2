import React from "react";
import { Link } from "react-router"; // Correction de l'import
import { useQuery } from "@tanstack/react-query";

import { useMutation } from "@tanstack/react-query";
import {  useState } from "react";
import { RadialBarChart, RadialBar, Legend, ResponsiveContainer, Tooltip } from 'recharts';
import AddressInput from  "./AdressInput"; // Correction de l'import
import NavigationMenu from "../../NavigationMenu";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const fetchTransports = async () => {
    const response = await fetch(`${API_BASE_URL}/transport/list`);
    if (!response.ok) {
      throw new Error("Erreur lors de la récupération des modes de transport");
    }
    return response.json();
  };

const TrajetCalculate = () => {
  const [departure, setDeparture] = useState("");
  const [arrival, setArrival] = useState("");
  const [roundTrip, setRoundTrip] = useState(false);
  const [data, setData] = useState(null);
  const [modeTransport, setModeTransport] = useState("");

  // Fetch de la liste des transports
  const { data: transportsData, isLoading: loadingTransports } = useQuery({
    queryKey: ["transportList"],
    queryFn: fetchTransports,
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    mutation.mutate(); // Envoie les données au serveur
  };
  const processData = (apiData) => {
    // Si aller-retour est coché, on double les émissions et la distance
    if (roundTrip) {
      return apiData.map((item) => ({
        ...item,
        aller_retour: item.total_emission * 2,
      }));
    }
    // Sinon, on retourne les données telles quelles
    return apiData;
  };

  const mutation = useMutation({
    mutationFn: async () => {
      const response = await fetch(
        `${API_BASE_URL}/trajet/calculate?mode_transport=${modeTransport}&adresse_depart=${departure}&adresse_arivee=${arrival}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error("Erreur lors de la requête");
      }
      return await response.json();
    },
    onSuccess: (data) => {
      // Mettre à jour les données du graphique avec la réponse de l'API
      setData(processData(data));
    },
    onError: (error) => {
      console.error("Erreur:", error);
    },
  });

  return (
    <section className="bg-white p-6 shadow-lg rounded-lg max-w-3xl mx-auto border mt-6 mb-6">
      {/* Onglets de navigation avec Link */}
      <NavigationMenu />

      {/* Formulaire de saisie */}
      <form onSubmit={handleSubmit} className="mt-4">
        <div className="flex gap-4">
          <div className="flex-1">
            <AddressInput
              label="Départ"
              value={departure}
              onChange={setDeparture}
            />
          </div>
          <div className="flex-1">
            <AddressInput
              label="Arrivée"
              value={arrival}
              onChange={setArrival}
            />
          </div>
        </div>
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
      {mutation.isSuccess && (
        <div className="mt-4">
          <h2 className="text-center font-semibold text-gray-700">
          {`Émissions de CO₂ pour le transport  ${modeTransport} :`}
          </h2>
          <h3 className="text-center font-semibold text-gray-700">
            <mark>distancer parcourue: {data["distance_km"]} km</mark>
          </h3>

          <div className="mt-6 bg-gray-100 p-4 rounded-md text-center">
          <div className="flex justify-center items-center p-4">
          <ResponsiveContainer width="100%" height={300}>
        <RadialBarChart
          width={730} 
          height={250} 
          innerRadius="10%" 
          outerRadius="80%" 
          data={[{ name: 'Émissions CO₂', value: data.total_emission, fill: '#3b82f6' },{ name: 'Équiv. en arbres', value: data.equivalent_en_arbre, fill: '#4CAF50' }]}
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
        </div>
      )}

      {mutation.isError && (
        <div className="mt-4 bg-red-100 text-red-700 p-4 rounded-lg">
          Erreur lors du calcul des émissions
        </div>
      )}
    </section>
  );
};

export default TrajetCalculate;
