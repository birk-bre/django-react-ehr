export interface Patient {
  id: number;
  medical_record_number: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: "M" | "F" | "O";
  blood_type: string;
  phone: string;
  email: string;
  address: string;
  emergency_contact_name: string;
  emergency_contact_phone: string;
  created_at: string;
  updated_at: string;
}

export interface PatientFormData {
  medical_record_number: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: "M" | "F" | "O";
  blood_type: string;
  phone: string;
  email: string;
  address: string;
  emergency_contact_name: string;
  emergency_contact_phone: string;
}

export interface MedicalRecord {
  id: number;
  patient: number;
  visit_date: string;
  doctor_name: string;
  chief_complaint: string;
  diagnosis: string;
  treatment_plan: string;
  notes: string;
  created_at: string;
}

export interface Medication {
  id: number;
  patient: number;
  medication_name: string;
  dosage: string;
  frequency: string;
  prescribing_doctor: string;
  start_date: string;
  end_date: string | null;
  is_active: boolean;
}

export interface VitalSign {
  id: number;
  patient: number;
  recorded_at: string;
  blood_pressure_systolic: number;
  blood_pressure_diastolic: number;
  heart_rate: number;
  temperature: number;
  weight: number;
  height: number | null;
  oxygen_saturation: number | null;
  notes: string;
  created_at: string;
}

export interface Appointment {
  id: number;
  patient: number;
  appointment_date: string;
  doctor_name: string;
  department: string;
  reason: string;
  status: "scheduled" | "completed" | "cancelled" | "no_show";
  notes: string;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}
