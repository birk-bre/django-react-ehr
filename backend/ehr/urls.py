from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PatientViewSet, MedicalRecordViewSet, MedicationViewSet,
    VitalSignViewSet, AppointmentViewSet
)

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'medical-records', MedicalRecordViewSet)
router.register(r'medications', MedicationViewSet)
router.register(r'vital-signs', VitalSignViewSet)
router.register(r'appointments', AppointmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
