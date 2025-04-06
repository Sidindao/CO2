import React, { Suspense, Component } from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, Navigate } from "react-router";
import App from "./App.jsx";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import Itinerary from "./compare/itinerary.jsx";
import Distance from "./compare/distance.jsx";
import Login from "./auth/login.jsx";
import PrivateRoute from "./auth/PrivateRoute.jsx";
import { AuthProvider } from "./auth/AuthContext.jsx";
import AdminPanel from "./admin/AdminPanel.jsx";


const queryClient = new QueryClient();

const root = document.getElementById("root");

ReactDOM.createRoot(root).render(
  <AuthProvider>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<App />}>
            <Route index element={<Itinerary />} />
            <Route path="distance" element={<Distance />} />
          </Route>
          <Route path="/login" element={<Login />} />
          {/* Routes Admin protégées */}
          <Route path="/admin/*" element={<PrivateRoute />}>
            <Route path="dashboard" element={<AdminPanel/>} />
            <Route
              path="settings"
              element={<h2>Page des paramètres admin</h2>}
            />
          </Route>
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  </AuthProvider>
);
