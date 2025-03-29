import React from "react";
import logo from "./assets/logo.png";

function Header() {
  return (
    <header className="bg-white shadow-md py-4  flex items-center w-full">
      <img src={logo} alt="Logo" className="h-12 max-w-2/12" />

      <h1 className="text-green-700  font-bold absolute left-1/2 transform -translate-x-1/2">
        Comparateur de CO₂
      </h1>
    </header>
  );
}

export default Header;
