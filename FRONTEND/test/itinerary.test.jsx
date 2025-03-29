import React from "react";
import { render, fireEvent, screen, waitFor } from "@testing-library/react";
import { BrowserRouter } from "react-router";
import Itinerary from "../src/compare/itinerary";
import { useMutation } from "@tanstack/react-query";
import { describe, it, expect, vi, beforeEach } from "vitest";

globalThis.ResizeObserver = class {
  observe() {}
  unobserve() {}
  disconnect() {}
};

// Mocker useMutation de react-query
vi.mock("@tanstack/react-query", () => ({
  useMutation: vi.fn(),
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

  it("should render the form correctly", () => {
    render(
      <BrowserRouter>
        {" "}
        {/* Envelopper dans BrowserRouter */}
        <Itinerary />
      </BrowserRouter>
    );

    expect(screen.getByLabelText(/Départ/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Arrivée/i)).toBeInTheDocument();
    expect(
      screen.getByRole("checkbox", { name: /Aller\/Retour/i })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /Calculer les émissions de CO₂/i })
    ).toBeInTheDocument();
  });

it("should call handleSubmit when the form is submitted", async () => {
    render(
      <BrowserRouter>
        {" "}
        {/* Envelopper dans BrowserRouter */}
        <Itinerary />
      </BrowserRouter>
    );

    const departureInput = screen.getByLabelText(/Départ/i);
    const arrivalInput = screen.getByLabelText(/Arrivée/i);
    const submitButton = screen.getByRole("button", {
      name: /Calculer les émissions de CO₂/i,
    });

    fireEvent.change(departureInput, { target: { value: "Paris" } });
    fireEvent.change(arrivalInput, { target: { value: "Lyon" } });

    fireEvent.click(submitButton);

    await waitFor(() => expect(useMutation().mutate).toHaveBeenCalled());
  });
});
