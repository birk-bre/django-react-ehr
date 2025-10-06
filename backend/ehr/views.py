from rest_framework import viewsets, filters
from .models import Patient, MedicalRecord, Medication, VitalSign, Appointment
from .serializers import (
    PatientSerializer, MedicalRecordSerializer, MedicationSerializer,
    VitalSignSerializer, AppointmentSerializer
)
from .mixins import PatientFilterMixin

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'medical_record_number', 'email']
    ordering_fields = ['created_at', 'last_name', 'first_name']

class MedicalRecordViewSet(PatientFilterMixin, viewsets.ModelViewSet):
    """
    ViewSet for MedicalRecord CRUD operations.
    
    Uses PatientFilterMixin to filter by patient ID.
    Example: GET /api/medical-records/?patient=1
    """
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['visit_date', 'created_at']
    
    # Old implementation (replaced by mixin):
    # def get_queryset(self):
    #     queryset = MedicalRecord.objects.all()
    #     patient_id = self.request.query_params.get('patient')
    #     if patient_id:
    #         queryset = queryset.filter(patient_id=patient_id)
    #     return queryset

class MedicationViewSet(PatientFilterMixin, viewsets.ModelViewSet):
    """
    ViewSet for Medication CRUD operations.
    
    Uses PatientFilterMixin to filter by patient ID.
    Supports additional filtering by active status.
    Examples:
        GET /api/medications/?patient=1
        GET /api/medications/?patient=1&is_active=true
    """
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['start_date', 'created_at']
    
    def get_queryset(self):
        # Call parent (mixin) to get patient-filtered queryset
        queryset = super().get_queryset()
        
        # Additional filtering by active status
        is_active = self.request.query_params.get('is_active')
        if is_active:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset

class VitalSignViewSet(PatientFilterMixin, viewsets.ModelViewSet):
    """
    ViewSet for VitalSign CRUD operations.
    
    Uses PatientFilterMixin to filter by patient ID.
    Example: GET /api/vital-signs/?patient=1
    """
    queryset = VitalSign.objects.all()
    serializer_class = VitalSignSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['recorded_at', 'created_at']
    
    # Old implementation (replaced by mixin):
    # def get_queryset(self):
    #     queryset = VitalSign.objects.all()
    #     patient_id = self.request.query_params.get('patient')
    #     if patient_id:
    #         queryset = queryset.filter(patient_id=patient_id)
    #     return queryset

class AppointmentViewSet(PatientFilterMixin, viewsets.ModelViewSet):
    """
    ViewSet for Appointment CRUD operations.
    
    Uses PatientFilterMixin to filter by patient ID.
    Supports additional filtering by appointment status.
    Examples:
        GET /api/appointments/?patient=1
        GET /api/appointments/?patient=1&status=scheduled
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['appointment_date', 'created_at']
    
    def get_queryset(self):
        # Call parent (mixin) to get patient-filtered queryset
        queryset = super().get_queryset()
        
        # Additional filtering by status
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
