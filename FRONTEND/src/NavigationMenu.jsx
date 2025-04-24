import { Link } from "react-router";
import { useState, useRef, useEffect } from "react";

export default function NavigationMenu() {
  const [openMenu, setOpenMenu] = useState(null);
  const menuRefs = {
    transport: useRef(null),
    distance: useRef(null),
    trajet: useRef(null)
  };

  const handleMouseEnter = (menu) => {
    setOpenMenu(menu);
  };

  const handleClickOutside = (event) => {
    if (openMenu && 
        !menuRefs[openMenu].current.contains(event.target) && 
        !event.target.closest(`.menu-${openMenu}`)) {
      setOpenMenu(null);
    }
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  });

  return (
    <nav className="bg-green-100 shadow">
      <ul className="flex justify-center space-x-6 py-3">
        {/* Emissions CO2 d'un transport */}
        <li 
          className="relative group"
          ref={menuRefs.transport}
          onMouseEnter={() => handleMouseEnter('transport')}
        >
          <button 
            className="cursor-pointer text-gray-700 font-medium hover:text-green-700 focus:outline-none"
            onClick={() => setOpenMenu(openMenu === 'transport' ? null : 'transport')}
            aria-expanded={openMenu === 'transport'}
            aria-haspopup="true"
          >
            Emissions CO₂ d'un transport
          </button>
          <ul 
            className={`absolute top-full left-0 ${openMenu === 'transport' ? 'block' : 'hidden'} bg-white shadow-lg rounded-lg mt-1 min-w-max z-50 menu-transport`}
          >
            <li>
              <Link
                to="/transport/list"
                className="block px-4 py-2 text-sm text-gray-700 hover:bg-green-100"
                onClick={() => setOpenMenu(null)}
              >
                Liste des modes de transport
              </Link>
            </li>
          </ul>
        </li>

        {/* Emissions CO2 pour une distance */}
        <li 
          className="relative group"
          ref={menuRefs.distance}
          onMouseEnter={() => handleMouseEnter('distance')}
        >
          <button 
            className="cursor-pointer text-gray-700 font-medium hover:text-green-700 focus:outline-none"
            onClick={() => setOpenMenu(openMenu === 'distance' ? null : 'distance')}
            aria-expanded={openMenu === 'distance'}
            aria-haspopup="true"
          >
            Emissions CO₂ pour une distance
          </button>
          <ul 
            className={`absolute top-full left-0 ${openMenu === 'distance' ? 'block' : 'hidden'} bg-white shadow-lg rounded-lg mt-1 min-w-max z-50 menu-distance`}
          >
            <li>
              <Link
                to="/distance/compare"
                className="block px-4 py-2 text-sm text-gray-700 hover:bg-green-100"
                onClick={() => setOpenMenu(null)}
              >
                Comparaison
              </Link>
            </li>
            <li>
              <Link
                to="/distance/calculate"
                className="block px-4 py-2 text-sm text-gray-700 hover:bg-green-100"
                onClick={() => setOpenMenu(null)}
              >
                Calcul
              </Link>
            </li>
          </ul>
        </li>

        {/* Emissions CO2 pour un trajet */}
        <li 
          className="relative group"
          ref={menuRefs.trajet}
          onMouseEnter={() => handleMouseEnter('trajet')}
        >
          <button 
            className="cursor-pointer text-gray-700 font-medium hover:text-green-700 focus:outline-none"
            onClick={() => setOpenMenu(openMenu === 'trajet' ? null : 'trajet')}
            aria-expanded={openMenu === 'trajet'}
            aria-haspopup="true"
          >
            Emissions CO₂ pour un trajet
          </button>
          <ul 
            className={`absolute top-full left-0 ${openMenu === 'trajet' ? 'block' : 'hidden'} bg-white shadow-lg rounded-lg mt-1 min-w-max z-50 menu-trajet`}
          >
            <li>
              <Link
                to="/trajet/itinerary"
                className="block px-4 py-2 text-sm text-gray-700 hover:bg-green-100"
                onClick={() => setOpenMenu(null)}
              >
                Comparaison
              </Link>
            </li>
            <li>
              <Link
                to="/trajet/calculate"
                className="block px-4 py-2 text-sm text-gray-700 hover:bg-green-100"
                onClick={() => setOpenMenu(null)}
              >
                Calcul
              </Link>
            </li>
          </ul>
        </li>
      </ul>
    </nav>
  );
}