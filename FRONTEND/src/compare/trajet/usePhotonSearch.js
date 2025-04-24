import { useQuery } from "@tanstack/react-query";

const fetchSuggestions = async (query) => {
  const res = await fetch(`https://photon.komoot.io/api/?q=${encodeURIComponent(query)}&limit=5`);

  if (!res.ok) {
    throw new Error("Erreur lors de la récupération des suggestions");
  }

  const data = await res.json();
  return data.features;
};

export const usePhotonSearch = (query) => {
  return useQuery({
    queryKey: ["photon", query],
    queryFn: () => fetchSuggestions(query),
    enabled: !!query && query.length > 2,
    staleTime: 1000 * 60,
  });
};
