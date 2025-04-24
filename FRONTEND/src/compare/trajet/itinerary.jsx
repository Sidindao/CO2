import React from "react";
import { Link } from "react-router"; // Correction de l'import

import { useMutation } from "@tanstack/react-query";
import {  useState } from "react";
import {
  XAxis,
  YAxis,
  Tooltip,
  BarChart,
  Bar,
  ResponsiveContainer,
} from "recharts";
import { renderCustomYAxisTick } from "../transportIcon";
import AddressInput from  "./AdressInput"; // Correction de l'import
import NavigationMenu from "../../NavigationMenu";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const Itinerary = () => {
  const [departure, setDeparture] = useState("");
  const [arrival, setArrival] = useState("");
  const [roundTrip, setRoundTrip] = useState(false);
  const [data, setData] = useState(null);

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
        `${API_BASE_URL}/trajet/compare?adresse_depart=${departure}&adresse_arivee=${arrival}`,
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
            Comparaison des émissions de CO₂
          </h2>
          <h3 className="text-center font-semibold text-gray-700">
            <mark>distancer parcourue: {data[0]["distance_km"]} km</mark>
          </h3>

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
                  interval={0}
                  tick={renderCustomYAxisTick}
                />
                <Tooltip />
                <Bar dataKey="total_emission" fill="#4CAF50" />
                <Bar dataKey="equivalent_en_arbre" fill="#1e3a8a" />
                {roundTrip && <Bar dataKey="aller_retour" fill="#82ca9d" />}
              </BarChart>
            </ResponsiveContainer>
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

export default Itinerary;
