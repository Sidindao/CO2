import React from "react";
import { render,  screen } from "@testing-library/react";
import { BrowserRouter } from "react-router";
import Itinerary from "../src/compare/trajet/itinerary";
import { useMutation, useQuery } from "@tanstack/react-query";
import { describe, it, expect, vi, beforeEach } from "vitest";

globalThis.ResizeObserver = class {
  observe() {}
  unobserve() {}
  disconnect() {}
};

// Mocker useMutation de react-query
vi.mock("@tanstack/react-query", () => ({
  useMutation: vi.fn(),
  useQuery: vi.fn(),
}));

describe("Itinerary", () => {
  beforeEach(() => {
    // Définir le comportement mocké pour useMutation
    useMutation.mockReturnValue({
      mutate: vi.fn(),
      isPending: false,
      isSuccess: false,
      isError: false,
      data: {},
    });
  });
  useQuery.mockReturnValue({
    data: [], // Retourne une liste vide par défaut
    isLoading: false,
    isError: false,
  });

  it("should render the form correctly", () => {
    render(
      <BrowserRouter>
        {" "}
        {/* Envelopper dans BrowserRouter */}
        <Itinerary />
      </BrowserRouter>
    );
    expect(
      screen.getByRole("button", { name: /Calculer les émissions de CO₂/i })
    ).toBeInTheDocument();
  });
});
