"""
Django management command to seed the database with sample data.
Usage: python manage.py seed_db
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from datetime import datetime, date, timedelta
import random

from backend.ehr.models import Patient, MedicalRecord, Medication, VitalSign, Appointment


class Command(BaseCommand):
    help = 'Seed the database with sample patient data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )
        parser.add_argument(
            '--patients',
            type=int,
            default=5,
            help='Number of patients to create (default: 5)',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Starting database seeding...')
        )

        if options['clear']:
            self.clear_existing_data()

        with transaction.atomic():
            patients = self.create_sample_patients(options['patients'])
            self.create_sample_medical_records(patients)
            self.create_sample_medications(patients)
            self.create_sample_vital_signs(patients)
            self.create_sample_appointments(patients)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(patients)} patients with associated records!'
            )
        )

    def clear_existing_data(self):
        """Clear all existing patient data"""
        self.stdout.write('Clearing existing data...')
        
        # Delete in proper order to avoid foreign key constraints
        Appointment.objects.all().delete()
        VitalSign.objects.all().delete()
        Medication.objects.all().delete()
        MedicalRecord.objects.all().delete()
        Patient.objects.all().delete()
        
        self.stdout.write(
            self.style.WARNING('✓ Existing data cleared')
        )

    def create_sample_patients(self, num_patients=5):
        """Create sample patients"""
        self.stdout.write('Creating sample patients...')
        
        # Base patient data - we'll modify this for additional patients
        base_patients_data = [
            {
                'medical_record_number': 'MRN001',
                'first_name': 'John',
                'last_name': 'Doe',
                'date_of_birth': date(1985, 3, 15),
                'gender': 'M',
                'blood_type': 'A+',
                'phone': '555-0101',
                'email': 'john.doe@email.com',
                'address': '123 Main St, Anytown, ST 12345',
                'emergency_contact_name': 'Jane Doe',
                'emergency_contact_phone': '555-0102'
            },
            {
                'medical_record_number': 'MRN002',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'date_of_birth': date(1990, 7, 22),
                'gender': 'F',
                'blood_type': 'B+',
                'phone': '555-0201',
                'email': 'sarah.johnson@email.com',
                'address': '456 Oak Ave, Somewhere, ST 67890',
                'emergency_contact_name': 'Michael Johnson',
                'emergency_contact_phone': '555-0202'
            },
            {
                'medical_record_number': 'MRN003',
                'first_name': 'Robert',
                'last_name': 'Smith',
                'date_of_birth': date(1978, 11, 8),
                'gender': 'M',
                'blood_type': 'O-',
                'phone': '555-0301',
                'email': 'robert.smith@email.com',
                'address': '789 Pine Rd, Elsewhere, ST 13579',
                'emergency_contact_name': 'Mary Smith',
                'emergency_contact_phone': '555-0302'
            },
            {
                'medical_record_number': 'MRN004',
                'first_name': 'Emily',
                'last_name': 'Davis',
                'date_of_birth': date(1995, 12, 3),
                'gender': 'F',
                'blood_type': 'AB+',
                'phone': '555-0401',
                'email': 'emily.davis@email.com',
                'address': '321 Elm St, Nowhere, ST 24680',
                'emergency_contact_name': 'James Davis',
                'emergency_contact_phone': '555-0402'
            },
            {
                'medical_record_number': 'MRN005',
                'first_name': 'Michael',
                'last_name': 'Wilson',
                'date_of_birth': date(1982, 5, 17),
                'gender': 'M',
                'blood_type': 'A-',
                'phone': '555-0501',
                'email': 'michael.wilson@email.com',
                'address': '654 Maple Dr, Anywhere, ST 97531',
                'emergency_contact_name': 'Lisa Wilson',
                'emergency_contact_phone': '555-0502'
            }
        ]

        # Additional names for generating more patients
        first_names = {
            'M': ['James', 'William', 'Benjamin', 'Lucas', 'Henry', 'Alexander', 'Mason', 'Ethan', 'Daniel', 'Matthew'],
            'F': ['Emma', 'Olivia', 'Ava', 'Isabella', 'Sophia', 'Charlotte', 'Mia', 'Amelia', 'Harper', 'Evelyn']
        }
        last_names = ['Anderson', 'Taylor', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin', 'Garcia', 'Martinez', 'Robinson']
        blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

        patients = []
        
        # Create the specified number of patients
        for i in range(num_patients):
            if i < len(base_patients_data):
                # Use predefined data for first 5 patients
                data = base_patients_data[i].copy()
            else:
                # Generate additional patients
                gender = random.choice(['M', 'F'])
                first_name = random.choice(first_names[gender])
                last_name = random.choice(last_names)
                
                data = {
                    'medical_record_number': f'MRN{i+1:03d}',
                    'first_name': first_name,
                    'last_name': last_name,
                    'date_of_birth': date(
                        random.randint(1950, 2010),
                        random.randint(1, 12),
                        random.randint(1, 28)
                    ),
                    'gender': gender,
                    'blood_type': random.choice(blood_types),
                    'phone': f'555-{random.randint(1000, 9999)}',
                    'email': f'{first_name.lower()}.{last_name.lower()}@email.com',
                    'address': f'{random.randint(100, 9999)} {random.choice(["Main", "Oak", "Pine", "Elm", "Maple"])} {random.choice(["St", "Ave", "Rd", "Dr"])}, {random.choice(["Anytown", "Somewhere", "Elsewhere"])}, ST {random.randint(10000, 99999)}',
                    'emergency_contact_name': f'{random.choice(first_names[gender])} {last_name}',
                    'emergency_contact_phone': f'555-{random.randint(1000, 9999)}'
                }

            patient, created = Patient.objects.get_or_create(
                medical_record_number=data['medical_record_number'],
                defaults=data
            )
            patients.append(patient)
            
            if created:
                self.stdout.write(f'✓ Created patient: {patient}')
            else:
                self.stdout.write(f'  Patient already exists: {patient}')

        return patients

    def create_sample_medical_records(self, patients):
        """Create sample medical records"""
        self.stdout.write('Creating sample medical records...')
        
        conditions = [
            ("Hypertension", "Regular monitoring of blood pressure", "Continue medication and lifestyle changes"),
            ("Type 2 Diabetes", "Blood sugar management", "Metformin 500mg twice daily, diet modification"),
            ("Annual Physical", "Routine health check", "All vitals normal, continue current health practices"),
            ("Common Cold", "Upper respiratory symptoms", "Rest, fluids, symptomatic treatment"),
            ("Allergic Reaction", "Seasonal allergies", "Antihistamine as needed, avoid known triggers"),
            ("Back Pain", "Lower back strain", "Physical therapy, pain management"),
            ("Migraine", "Severe headaches", "Preventive medication, lifestyle modifications"),
            ("Anxiety", "Generalized anxiety symptoms", "Counseling, stress management techniques")
        ]

        doctors = ["Dr. Smith", "Dr. Johnson", "Dr. Williams", "Dr. Brown", "Dr. Davis", "Dr. Miller", "Dr. Wilson"]

        for patient in patients:
            # Create 1-3 medical records per patient
            num_records = random.randint(1, 3)
            for i in range(num_records):
                condition = random.choice(conditions)
                doctor = random.choice(doctors)
                visit_date = timezone.now() - timedelta(days=random.randint(1, 180))

                record = MedicalRecord.objects.create(
                    patient=patient,
                    visit_date=visit_date,
                    chief_complaint=condition[0],
                    diagnosis=condition[1],
                    treatment_plan=condition[2],
                    doctor_name=doctor,
                    notes=f"Follow-up recommended in {random.randint(1, 6)} months"
                )
                self.stdout.write(f'  ✓ Created medical record for {patient.first_name} {patient.last_name}')

    def create_sample_medications(self, patients):
        """Create sample medications"""
        self.stdout.write('Creating sample medications...')
        
        medications = [
            ("Lisinopril", "10mg", "Once daily"),
            ("Metformin", "500mg", "Twice daily"),
            ("Ibuprofen", "200mg", "As needed for pain"),
            ("Vitamin D3", "1000 IU", "Once daily"),
            ("Omeprazole", "20mg", "Once daily before breakfast"),
            ("Atorvastatin", "20mg", "Once daily at bedtime"),
            ("Amoxicillin", "500mg", "Three times daily"),
            ("Aspirin", "81mg", "Once daily")
        ]

        doctors = ["Dr. Smith", "Dr. Johnson", "Dr. Williams", "Dr. Brown", "Dr. Davis", "Dr. Miller", "Dr. Wilson"]

        for patient in patients:
            # Create 0-2 medications per patient
            num_meds = random.randint(0, 2)
            for i in range(num_meds):
                med_data = random.choice(medications)
                doctor = random.choice(doctors)
                start_date = date.today() - timedelta(days=random.randint(1, 90))

                medication = Medication.objects.create(
                    patient=patient,
                    medication_name=med_data[0],
                    dosage=med_data[1],
                    frequency=med_data[2],
                    start_date=start_date,
                    prescribing_doctor=doctor,
                    is_active=random.choice([True, True, True, False])  # 75% active
                )
                self.stdout.write(f'  ✓ Created medication {med_data[0]} for {patient.first_name} {patient.last_name}')

    def create_sample_vital_signs(self, patients):
        """Create sample vital signs"""
        self.stdout.write('Creating sample vital signs...')
        
        for patient in patients:
            # Create 2-5 vital sign records per patient
            num_vitals = random.randint(2, 5)
            for i in range(num_vitals):
                recorded_at = timezone.now() - timedelta(days=random.randint(1, 180))

                vital = VitalSign.objects.create(
                    patient=patient,
                    recorded_at=recorded_at,
                    blood_pressure_systolic=random.randint(110, 140),
                    blood_pressure_diastolic=random.randint(70, 90),
                    heart_rate=random.randint(60, 100),
                    temperature=round(random.uniform(97.0, 99.5), 1),
                    weight=round(random.uniform(120, 220), 2),
                    height=round(random.uniform(60, 75), 2) if random.choice([True, False]) else None,
                    oxygen_saturation=random.randint(95, 100) if random.choice([True, False]) else None
                )
                self.stdout.write(f'  ✓ Created vital signs for {patient.first_name} {patient.last_name}')

    def create_sample_appointments(self, patients):
        """Create sample appointments"""
        self.stdout.write('Creating sample appointments...')
        
        departments = ["Cardiology", "Internal Medicine", "Family Practice", "Dermatology", "Orthopedics", "Neurology", "Psychiatry"]
        doctors = ["Dr. Smith", "Dr. Johnson", "Dr. Williams", "Dr. Brown", "Dr. Davis", "Dr. Miller", "Dr. Wilson"]
        reasons = [
            "Annual physical exam",
            "Follow-up visit",
            "Blood pressure check",
            "Medication review",
            "Consultation",
            "Routine checkup",
            "Lab results review",
            "Specialist referral"
        ]

        for patient in patients:
            # Create 1-3 appointments per patient (past and future)
            num_appointments = random.randint(1, 3)
            for i in range(num_appointments):
                # Mix of past and future appointments
                if random.choice([True, False]):
                    # Past appointment
                    appointment_date = timezone.now() - timedelta(days=random.randint(1, 90))
                    status = random.choice(['completed', 'completed', 'no_show'])
                else:
                    # Future appointment
                    appointment_date = timezone.now() + timedelta(days=random.randint(1, 60))
                    status = random.choice(['scheduled', 'confirmed'])

                appointment = Appointment.objects.create(
                    patient=patient,
                    appointment_date=appointment_date,
                    doctor_name=random.choice(doctors),
                    department=random.choice(departments),
                    reason=random.choice(reasons),
                    status=status
                )
                self.stdout.write(f'  ✓ Created appointment for {patient.first_name} {patient.last_name}')