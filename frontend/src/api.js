import axios from 'axios'

const getBackendURL = () => {
  if (window.location.hostname === 'localhost') {
    return 'http://localhost:8000/api'
  }
  const domain = window.location.hostname
  const backendDomain = domain.replace(/^([^.]+)/, '$1-8000')
  return `https://${backendDomain}/api`
}

const API_BASE_URL = getBackendURL()

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const patientAPI = {
  getAll: () => api.get('/patients/'),
  getOne: (id) => api.get(`/patients/${id}/`),
  create: (data) => api.post('/patients/', data),
  update: (id, data) => api.put(`/patients/${id}/`, data),
  delete: (id) => api.delete(`/patients/${id}/`),
}

export const medicalRecordAPI = {
  getAll: (patientId) => api.get('/medical-records/', { params: { patient: patientId } }),
  create: (data) => api.post('/medical-records/', data),
}

export const medicationAPI = {
  getAll: (patientId) => api.get('/medications/', { params: { patient: patientId } }),
  create: (data) => api.post('/medications/', data),
}

export const vitalSignAPI = {
  getAll: (patientId) => api.get('/vital-signs/', { params: { patient: patientId } }),
  create: (data) => api.post('/vital-signs/', data),
}

export const appointmentAPI = {
  getAll: (patientId) => api.get('/appointments/', { params: { patient: patientId } }),
  create: (data) => api.post('/appointments/', data),
  update: (id, data) => api.patch(`/appointments/${id}/`, data),
}

export default api
