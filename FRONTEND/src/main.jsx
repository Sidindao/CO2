import React, { Suspense, Component } from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, Navigate } from "react-router";
import App from "./App.jsx";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import Itinerary from "./compare/trajet/itinerary.jsx";
import Distance from "./compare/distance/distance.jsx";
import DistanceCalculator from "./compare/distance/distanceCalculate.jsx";
import Login from "./auth/login.jsx";
import PrivateRoute from "./auth/PrivateRoute.jsx";
import { AuthProvider } from "./auth/AuthProvider.jsx";
import AdminPanel from "./admin/AdminPanel.jsx";
import TransportCO2Calculator from "./compare/transport/emission.jsx";
import TrajetCalculate from "./compare/trajet/TrajetCalculate.jsx";

const queryClient = new QueryClient();

const root = document.getElementById("root");

ReactDOM.createRoot(root).render(
  <AuthProvider>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/trajet" element={<App />}>
            <Route path="itinerary" element={<Itinerary />} />
            <Route path="calculate" element={<TrajetCalculate />} />
          </Route>
          <Route path="/transport" element={<App />}>
            <Route path="list" element={<TransportCO2Calculator />} />
          </Route>
          <Route path="/distance" element={<App />}>
            <Route path="compare" element={<Distance />} />
            <Route path="calculate" element={<DistanceCalculator />} />
          </Route>

          <Route path="/login" element={<Login />} />
          {/* Routes Admin protégées */}
          <Route path="/admin/*" element={<PrivateRoute />}>
            <Route path="dashboard" element={<AdminPanel />} />
            <Route
              path="settings"
              element={<h2>Page des paramètres admin</h2>}
            />
          </Route>
          <Route path="*" element={<Navigate to="/trajet/itinerary" replace />} />
        </Routes>
      </BrowserRouter>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  </AuthProvider>
);
