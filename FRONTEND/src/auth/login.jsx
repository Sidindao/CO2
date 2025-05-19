import { useState } from "react";
import logo from "./../assets/logo.png";
import { useNavigate } from "react-router";



const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate(); 

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    try {
      const response = await fetch(`${API_BASE_URL}/admin/login`, {
        method: "POST",
        body: formData,
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.detail || "Erreur d'authentification");
      }
      
      localStorage.setItem("token", data.access_token);
      navigate("/admin/dashboard"); 
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
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
        <h2 className="text-center text-2xl font-semibold text-gray-800">Connexion Admin</h2>

        {/* Message d'erreur */}
        {error && (
          <div className="mt-4 p-2 bg-red-100 text-red-700 rounded-md text-sm">
            {error}
          </div>
        )}

        {/* Formulaire */}
        <form onSubmit={handleSubmit} className="mt-6">
          <div className="mb-4">
            <label className="block text-green-600 text-sm mb-2">Nom d'utilisateur</label>
            <input
              type="text"
              className="w-full px-4 py-2 border border-green-500 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder="Nom d'utilisateur"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          <div className="mb-6">
            <label className="block text-green-600 text-sm mb-2">Mot de passe</label>
            <input
              type="password"
              className="w-full px-4 py-2 border border-green-500 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder="Mot de passe"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button
            type="submit"
            className="w-full py-2 text-white bg-green-300 rounded-md hover:bg-green-400 transition flex items-center justify-center"
            disabled={loading}
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