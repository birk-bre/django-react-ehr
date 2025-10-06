import axios, { AxiosInstance } from "axios";
import type {
  Patient,
  PatientFormData,
  MedicalRecord,
  Medication,
  VitalSign,
  Appointment,
  PaginatedResponse,
} from "./types";

const getBackendURL = (): string => {
  if (window.location.hostname === "localhost") {
    return "http://localhost:8000/api";
  }
  const domain = window.location.hostname;
  const backendDomain = domain.replace(/^([^.]+)/, "$1-8000");
  return `https://${backendDomain}/api`;
};

const API_BASE_URL = getBackendURL();

const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const patientAPI = {
  getAll: () => api.get<PaginatedResponse<Patient>>("/patients/"),
  getOne: (id: string | number) => api.get<Patient>(`/patients/${id}/`),
  create: (data: PatientFormData) => api.post<Patient>("/patients/", data),
  update: (id: string | number, data: Partial<PatientFormData>) =>
    api.put<Patient>(`/patients/${id}/`, data),
  delete: (id: string | number) => api.delete(`/patients/${id}/`),
};

export const medicalRecordAPI = {
  getAll: (patientId: string | number) =>
    api.get<MedicalRecord[]>("/medical-records/", {
      params: { patient: patientId },
    }),
  create: (data: Partial<MedicalRecord>) =>
    api.post<MedicalRecord>("/medical-records/", data),
};

export const medicationAPI = {
  getAll: (patientId: string | number) =>
    api.get<Medication[]>("/medications/", { params: { patient: patientId } }),
  create: (data: Partial<Medication>) =>
    api.post<Medication>("/medications/", data),
};

export const vitalSignAPI = {
  getAll: (patientId: string | number) =>
    api.get<VitalSign[]>("/vital-signs/", { params: { patient: patientId } }),
  create: (data: Partial<VitalSign>) =>
    api.post<VitalSign>("/vital-signs/", data),
};

export const appointmentAPI = {
  getAll: (patientId: string | number) =>
    api.get<Appointment[]>("/appointments/", {
      params: { patient: patientId },
    }),
  create: (data: Partial<Appointment>) =>
    api.post<Appointment>("/appointments/", data),
  update: (id: string | number, data: Partial<Appointment>) =>
    api.patch<Appointment>(`/appointments/${id}/`, data),
};

export default api;
