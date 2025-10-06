
# Mixins for ViewSets
# Mixins provide reusable functionality that can be shared across multiple ViewSets.

class PatientFilterMixin:
    """
    Mixin to add patient filtering to ViewSets.
    
    Allows filtering resources by patient ID via query parameter:
    GET /api/resource/?patient=1
    
    Usage:
        class MedicalRecordViewSet(PatientFilterMixin, viewsets.ModelViewSet):
            queryset = MedicalRecord.objects.all()
            serializer_class = MedicalRecordSerializer
    """
    
    def get_queryset(self):
        queryset = super().get_queryset()
        patient_id = self.request.query_params.get('patient')
        
        if patient_id is not None:
            queryset = queryset.filter(patient_id=patient_id)
        
        return queryset
