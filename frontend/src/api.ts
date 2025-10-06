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

// A helper function to handle fetch requests and errors
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

  const response = await fetch(url, defaultOptions);

  if (!response.ok) {
    // Try to parse error response from the backend
    const errorData = await response.json().catch(() => ({}));
    const errorMessage =
      errorData.detail || `API Error: ${response.status} ${response.statusText}`;
    throw new Error(errorMessage);
  }

  // Handle responses with no content
  if (response.status === 204) {
    return null as T;
  }

  return response.json();
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

