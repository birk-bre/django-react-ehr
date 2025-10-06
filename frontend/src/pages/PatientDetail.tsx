import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import {
  patientAPI,
  medicalRecordAPI,
  medicationAPI,
  vitalSignAPI,
  appointmentAPI,
} from "../api";
import type {
  Patient,
  MedicalRecord,
  Medication,
  VitalSign,
  Appointment,
} from "../types";

type TabType =
  | "medical-records"
  | "medications"
  | "vital-signs"
  | "appointments";

function PatientDetail() {
  const { id } = useParams<{ id: string }>();
  const [patient, setPatient] = useState<Patient | null>(null);
  const [medicalRecords, setMedicalRecords] = useState<MedicalRecord[]>([]);
  const [medications, setMedications] = useState<Medication[]>([]);
  const [vitalSigns, setVitalSigns] = useState<VitalSign[]>([]);
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [activeTab, setActiveTab] = useState<TabType>("medical-records");

  useEffect(() => {
    if (id) {
      loadPatientData();
    }
  }, [id]);

  const loadPatientData = async () => {
    if (!id) return;

    try {
      const [patientRes, medicalRes, medRes, vitalRes, apptRes] =
        await Promise.all([
          patientAPI.getOne(id),
          medicalRecordAPI.getAll(id),
          medicationAPI.getAll(id),
          vitalSignAPI.getAll(id),
          appointmentAPI.getAll(id),
        ]);

      console.log("Medications fetched:");
      setPatient(patientRes.data);
      setMedicalRecords(medicalRes.data);
      setMedications(medRes.data);
      setVitalSigns(vitalRes.data);
      setAppointments(apptRes.data);
    } catch (error) {
      console.error("Error loading patient data:", error);
    }
  };

  if (!patient) return <div className="loading">Loading...</div>;

  return (
    <div className="patient-detail">
      <Link to="/" className="back-link">
        ← Back to Patients
      </Link>

      <div className="patient-header">
        <h2>
          {patient.first_name} {patient.last_name}
        </h2>
        <div className="patient-info">
          <p>
            <strong>MRN:</strong> {patient.medical_record_number}
          </p>
          <p>
            <strong>DOB:</strong> {patient.date_of_birth}
          </p>
          <p>
            <strong>Gender:</strong> {patient.gender}
          </p>
          <p>
            <strong>Blood Type:</strong> {patient.blood_type || "N/A"}
          </p>
          <p>
            <strong>Phone:</strong> {patient.phone}
          </p>
          <p>
            <strong>Email:</strong> {patient.email || "N/A"}
          </p>
        </div>
      </div>

      <div className="tabs">
        <button
          className={activeTab === "medical-records" ? "active" : ""}
          onClick={() => setActiveTab("medical-records")}
        >
          Medical Records
        </button>
        <button
          className={activeTab === "medications" ? "active" : ""}
          onClick={() => setActiveTab("medications")}
        >
          Medications
        </button>
        <button
          className={activeTab === "vital-signs" ? "active" : ""}
          onClick={() => setActiveTab("vital-signs")}
        >
          Vital Signs
        </button>
        <button
          className={activeTab === "appointments" ? "active" : ""}
          onClick={() => setActiveTab("appointments")}
        >
          Appointments
        </button>
      </div>

      <div className="tab-content">
        {activeTab === "medical-records" && (
          <div className="medical-records">
            <h3>Medical Records</h3>
            {Array.isArray(medicalRecords) &&
              medicalRecords.length > 0 &&
              medicalRecords.map((record) => (
                <div key={record.id} className="record-card">
                  <p>
                    <strong>Date:</strong>{" "}
                    {new Date(record.visit_date).toLocaleDateString()}
                  </p>
                  <p>
                    <strong>Doctor:</strong> {record.doctor_name}
                  </p>
                  <p>
                    <strong>Chief Complaint:</strong> {record.chief_complaint}
                  </p>
                  <p>
                    <strong>Diagnosis:</strong> {record.diagnosis}
                  </p>
                  <p>
                    <strong>Treatment:</strong> {record.treatment_plan}
                  </p>
                </div>
              ))}
          </div>
        )}

        {activeTab === "medications" && (
          <div className="medications">
            <h3>Medications</h3>
            {medications.map((med) => (
              <div key={med.id} className="record-card">
                <p>
                  <strong>{med.medication_name}</strong> - {med.dosage}
                </p>
                <p>
                  <strong>Frequency:</strong> {med.frequency}
                </p>
                <p>
                  <strong>Prescribing Doctor:</strong> {med.prescribing_doctor}
                </p>
                <p>
                  <strong>Status:</strong>{" "}
                  {med.is_active ? "Active" : "Inactive"}
                </p>
              </div>
            ))}
          </div>
        )}

        {activeTab === "vital-signs" && (
          <div className="vital-signs">
            <h3>Vital Signs</h3>
            {vitalSigns.map((vital) => (
              <div key={vital.id} className="record-card">
                <p>
                  <strong>Date:</strong>{" "}
                  {new Date(vital.recorded_at).toLocaleString()}
                </p>
                <p>
                  <strong>BP:</strong> {vital.blood_pressure_systolic}/
                  {vital.blood_pressure_diastolic}
                </p>
                <p>
                  <strong>Heart Rate:</strong> {vital.heart_rate} bpm
                </p>
                <p>
                  <strong>Temperature:</strong> {vital.temperature}°F
                </p>
                <p>
                  <strong>Weight:</strong> {vital.weight} lbs
                </p>
              </div>
            ))}
          </div>
        )}

        {activeTab === "appointments" && (
          <div className="appointments">
            <h3>Appointments</h3>
            {appointments.map((appt) => (
              <div key={appt.id} className="record-card">
                <p>
                  <strong>Date:</strong>{" "}
                  {new Date(appt.appointment_date).toLocaleString()}
                </p>
                <p>
                  <strong>Doctor:</strong> {appt.doctor_name}
                </p>
                <p>
                  <strong>Department:</strong> {appt.department}
                </p>
                <p>
                  <strong>Reason:</strong> {appt.reason}
                </p>
                <p>
                  <strong>Status:</strong> {appt.status}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default PatientDetail;
