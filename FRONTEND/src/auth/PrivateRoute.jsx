import { useContext } from "react";
import { AuthContext } from "./AuthContext";
import { Navigate, Outlet } from "react-router";

const PrivateRoute = () => {
  const { user } = useContext(AuthContext);

  return !user ? <Outlet /> : <Navigate to="/login" />;
};

export default PrivateRoute;
