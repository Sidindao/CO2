import Header from "./header";
import Footer from "./footer";
import effet from "./assets/effet.jpg";

import "./App.css";
import { Outlet } from "react-router";

function App() {

  return (
    <>
      <Header></Header>

      <div  className="sm:absolute  sm:top-2/12   sm:right-1/12 sm:left-1/12 relative  bg-white px-6   rounded-lg shadow-lg  text-center">
        <h2 className="text-green font-bold">
          COMPAREZ L’IMPACT DE CARBONE DE VOS TRAJETS
        </h2>
        <p className="text-gray w-full  ">
          Vous vous demandez quel mode de transport émet le moins de CO₂ ? Ce
          calculateur compare l’émission de différents moyens de transport
          (vélo, voiture, train...) en fonction du point de départ et d’arrivée.
        </p>
      </div>
      <section className="flex  sm:pt-15 pt-0 w-full">
        {/* Image de fond */}
        {/* Contenu textuel */}
        <img
          src={effet}
          alt="CO2 Impact"
          className="mx-auto  sm:h-40 inset-0 w-full"
        />
      </section>
      <Outlet></Outlet>
      <Footer></Footer>
    </>
  );
}

export default App;
