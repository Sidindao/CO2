import React, { useState, useEffect } from "react";
import { usePhotonSearch } from "./usePhotonSearch"; // Assurez-vous que le chemin est correct   

const useDebounce = (value, delay = 300) => {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const handler = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(handler);
  }, [value, delay]);
  return debounced;
};

const AddressInput = ({ label, value, onChange }) => {
  const [query, setQuery] = useState(value);
  const [isFocused, setIsFocused] = useState(false);
  const debouncedQuery = useDebounce(query);
  const { data: suggestions = [], isFetching } = usePhotonSearch(debouncedQuery);

  const handleSelect = (suggestion) => {
    const name = suggestion?.properties?.name || '';
    const city = suggestion?.properties?.city || '';
    const country = suggestion?.properties?.country || '';
    
    const full = [name, city, country].filter(Boolean).join(', ');
    setQuery(full);
    onChange(full); // met à jour le parent
    setIsFocused(false);
  };
  

  return (
    <div className="relative">
      <label className="block text-gray-700 font-medium mb-1">
        {label}
      </label>
      <input
        type="text"
        className="w-full border p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
        placeholder={`Entrer ${label.toLowerCase()}`}
        value={query}
        onChange={(e) => {
          setQuery(e.target.value);
          onChange(e.target.value);
        }}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setTimeout(() => setIsFocused(false), 150)}
      />
      {isFocused && debouncedQuery.length > 2 && (
        <ul className="absolute bg-white border border-gray-200 rounded-md shadow-md w-full max-h-60 overflow-auto z-10">
          {isFetching && <li className="p-2 text-sm italic text-gray-400">Chargement...</li>}
          {!isFetching && suggestions.length === 0 && <li className="p-2 text-sm text-gray-400">Aucune suggestion</li>}
          {suggestions.map((s, index) => (
            <li
              key={index}
              onClick={() => handleSelect(s)}
              className="p-2 cursor-pointer hover:bg-green-100"
            >
              {s.properties.name} {s.properties.name && ','} {s.properties.city}{s.properties.city && ','} {s.properties.country}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default AddressInput;
