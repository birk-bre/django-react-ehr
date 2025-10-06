from rest_framework import serializers
from .models import Patient, MedicalRecord, Medication, VitalSign, Appointment

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            'id', 'medical_record_number', 'first_name', 'last_name', 
            'date_of_birth', 'gender', 'blood_type', 'phone', 'email', 
            'address', 'emergency_contact_name', 'emergency_contact_phone', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = [
            'id', 'patient', 'visit_date', 'chief_complaint', 'diagnosis', 
            'treatment_plan', 'notes', 'doctor_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = [
            'id', 'patient', 'medication_name', 'dosage', 'frequency', 
            'start_date', 'end_date', 'prescribing_doctor', 'notes', 
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class VitalSignSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitalSign
        fields = [
            'id', 'patient', 'recorded_at', 'blood_pressure_systolic', 
            'blood_pressure_diastolic', 'heart_rate', 'temperature', 'weight', 
            'height', 'oxygen_saturation', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'appointment_date', 'doctor_name', 'department', 
            'reason', 'status', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
