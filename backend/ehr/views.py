from rest_framework import viewsets, filters
from .models import Patient, MedicalRecord, Medication, VitalSign, Appointment
from .serializers import (
    PatientSerializer, MedicalRecordSerializer, MedicationSerializer,
    VitalSignSerializer, AppointmentSerializer
)

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'medical_record_number', 'email']
    ordering_fields = ['created_at', 'last_name', 'first_name']

class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['visit_date', 'created_at']
    
    def get_queryset(self):
        queryset = MedicalRecord.objects.all()
        patient_id = self.request.query_params.get('patient')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        return queryset

class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['start_date', 'created_at']
    
    def get_queryset(self):
        queryset = Medication.objects.all()
        patient_id = self.request.query_params.get('patient')
        is_active = self.request.query_params.get('is_active')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        if is_active:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        return queryset

class VitalSignViewSet(viewsets.ModelViewSet):
    queryset = VitalSign.objects.all()
    serializer_class = VitalSignSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['recorded_at', 'created_at']
    
    def get_queryset(self):
        queryset = VitalSign.objects.all()
        patient_id = self.request.query_params.get('patient')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        return queryset

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['appointment_date', 'created_at']
    
    def get_queryset(self):
        queryset = Appointment.objects.all()
        patient_id = self.request.query_params.get('patient')
        status = self.request.query_params.get('status')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        if status:
            queryset = queryset.filter(status=status)
        return queryset
