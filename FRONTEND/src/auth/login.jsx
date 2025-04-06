import { useState } from "react";
import logo from "./../assets/logo.png";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const Login = ({ onLogin }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const response = await fetch(`${API_BASE_URL}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    const data = await response.json();
    if (response.ok) {
      localStorage.setItem("token", data.token);
      onLogin();
    } else {
      alert("Erreur d'authentification");
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-green-500">
      <div className="bg-white p-8 rounded-2xl shadow-xl w-96">
        {/* Logo */}
        <div className="flex justify-center">
          <img src={logo} alt="Logo" className="h-20 mb-4" />
        </div>

        {/* Titre */}
        <h2 className="text-center text-2xl font-semibold text-gray-800">Connexion</h2>

        {/* Formulaire */}
        <form onSubmit={handleSubmit} className="mt-6">
          <div className="mb-4">
            <label className="block text-green-600 text-sm mb-2">Votre email</label>
            <input
              type="email"
              className="w-full px-4 py-2 border border-green-500 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder="Votre email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="mb-6">
            <label className="block text-green-600 text-sm mb-2">Votre mot de passe</label>
            <input
              type="password"
              className="w-full px-4 py-2 border border-green-500 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder="Votre mot de passe"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button
            type="submit"
            className="w-full py-2 text-white bg-green-300 rounded-md hover:bg-green-400 transition flex items-center justify-center"
            disabled={loading} // Désactive le bouton pendant le chargement
          >
            {loading ? (
              <svg className="animate-spin h-5 w-5 mr-2 text-white" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
              </svg>
            ) : null}
            {loading ? "Connexion..." : "Se connecter"}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;
