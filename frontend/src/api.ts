import type {
  Patient,
  PatientFormData,
  MedicalRecord,
  Medication,
  VitalSign,
  Appointment,
  PaginatedResponse,
} from "./types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

/**
 * Custom error class for API errors
 * Provides structured error information
 */
export class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public details?: Record<string, any>
  ) {
    super(message);
    this.name = "APIError";
  }
}

/**
 * Generic fetch wrapper with error handling and type safety
 *
 * @param endpoint - API endpoint (e.g., "/patients/")
 * @param options - Fetch options (method, headers, body, etc.)
 * @returns Parsed JSON response
 * @throws APIError on HTTP errors
 */
const apiFetch = async <T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> => {
  const url = `${API_BASE_URL}${endpoint}`;

  const defaultOptions: RequestInit = {
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    ...options,
  };

  try {
    const response = await fetch(url, defaultOptions);

    if (!response.ok) {
      // Try to parse error response from the backend
      let errorDetails: Record<string, any> = {};
      try {
        errorDetails = await response.json();
      } catch {
        // If JSON parsing fails, use default error message
      }

      const errorMessage =
        errorDetails.detail ||
        errorDetails.message ||
        `HTTP ${response.status}: ${response.statusText}`;

      throw new APIError(errorMessage, response.status, errorDetails);
    }

    // Handle responses with no content (e.g., 204 No Content)
    if (response.status === 204) {
      return null as T;
    }

    return response.json();
  } catch (error) {
    // Re-throw APIError as-is
    if (error instanceof APIError) {
      throw error;
    }

    // Handle network errors, timeout, etc.
    if (error instanceof Error) {
      throw new APIError(`Network error: ${error.message}`, 0, {
        originalError: error,
      });
    }

    // Unknown error
    throw new APIError("An unknown error occurred", 0);
  }
};

export const patientAPI = {
  getAll: () => apiFetch<PaginatedResponse<Patient>>("/patients/"),
  getOne: (id: string | number) => apiFetch<Patient>(`/patients/${id}/`),
  create: (data: PatientFormData) =>
    apiFetch<Patient>("/patients/", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  update: (id: string | number, data: Partial<PatientFormData>) =>
    apiFetch<Patient>(`/patients/${id}/`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),
  delete: (id: string | number) =>
    apiFetch<null>(`/patients/${id}/`, {
      method: "DELETE",
    }),
};

export const medicalRecordAPI = {
  getAll: (patientId: string | number) =>
    apiFetch<PaginatedResponse<MedicalRecord>>(
      `/medical-records/?patient=${patientId}`
    ),
  create: (data: Partial<MedicalRecord>) =>
    apiFetch<MedicalRecord>("/medical-records/", {
      method: "POST",
      body: JSON.stringify(data),
    }),
};

export const medicationAPI = {
  getAll: (patientId: string | number) =>
    apiFetch<PaginatedResponse<Medication>>(
      `/medications/?patient=${patientId}`
    ),
  create: (data: Partial<Medication>) =>
    apiFetch<Medication>("/medications/", {
      method: "POST",
      body: JSON.stringify(data),
    }),
};

export const vitalSignAPI = {
  getAll: (patientId: string | number) =>
    apiFetch<PaginatedResponse<VitalSign>>(
      `/vital-signs/?patient=${patientId}`
    ),
  create: (data: Partial<VitalSign>) =>
    apiFetch<VitalSign>("/vital-signs/", {
      method: "POST",
      body: JSON.stringify(data),
    }),
};

export const appointmentAPI = {
  getAll: (patientId: string | number) =>
    apiFetch<PaginatedResponse<Appointment>>(
      `/appointments/?patient=${patientId}`
    ),
  create: (data: Partial<Appointment>) =>
    apiFetch<Appointment>("/appointments/", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  update: (id: string | number, data: Partial<Appointment>) =>
    apiFetch<Appointment>(`/appointments/${id}/`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),
};
