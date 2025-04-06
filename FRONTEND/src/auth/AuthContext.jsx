import { createContext, useState, useEffect } from "react";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  // useEffect(() => {
  //   const token = localStorage.getItem("token");
  //   if (token) {
  //     fetch("http://backend-url/api/me", {
  //       headers: { Authorization: `Bearer ${token}` },
  //     })
  //       .then((res) => res.json())
  //       .then((data) => setUser(data));
  //   }
  // }, []);

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
  };

  return <AuthContext.Provider value={{ user, setUser, logout }}>{children}</AuthContext.Provider>;
};
