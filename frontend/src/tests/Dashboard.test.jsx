import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import Dashboard from "../pages/Dashboard.jsx";

// ✅ MOCK AXIOS PROPERLY
vi.mock("axios", () => {
  const mockAxiosInstance = {
    get: vi.fn(),
    post: vi.fn(),
    patch: vi.fn(),
    delete: vi.fn(),
    interceptors: {
      request: { use: vi.fn() },
      response: { use: vi.fn() },
    },
  };

  return {
    default: {
      create: vi.fn(() => mockAxiosInstance),
    },
  };
});

// 🔽 IMPORT AFTER MOCK
import api from "../api/axios";

beforeEach(() => {
  api.get.mockImplementation((url) => {
    if (url === "/tasks") {
      return Promise.resolve({ data: [] });
    }

    if (url === "/tasks/progress") {
      return Promise.resolve({
        data: {
          total_tasks: 0,
          completed_tasks: 0,
          pending: 0,
          completion_percentage: 0,
        },
      });
    }

    return Promise.reject(new Error("Unknown API call"));
  });
});

describe("Dashboard", () => {
  it("renders dashboard UI without crashing", async () => {
    render(<Dashboard />);

    expect(await screen.findByText("My Tasks")).toBeInTheDocument();
    expect(screen.getByText("Create Task")).toBeInTheDocument();
    expect(screen.getByText("Filters")).toBeInTheDocument();
  });
});
