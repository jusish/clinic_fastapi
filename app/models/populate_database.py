import random
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy.orm import Session
from models import Patient, BillingRecord, MedicalRecord, Medicine
from database import engine, SessionLocal

fake = Faker()

def generate_patients(n=100000):
    patients = []
    for _ in range(n):
        patient = Patient(
            name=fake.name(),
            dob=fake.date_of_birth(minimum_age=0, maximum_age=100),
            contact_info=fake.phone_number(),
            date_attended=fake.date_between(start_date='-2y', end_date='today')
        )
        patients.append(patient)
    return patients

def generate_billing_records(n=100000, patient_ids=None):
    billing_records = []
    for _ in range(n):
        record = BillingRecord(
            patient_id=random.choice(patient_ids),
            total_cost=round(random.uniform(50, 1000), 2),
            date=fake.date_time_this_year()
        )
        billing_records.append(record)
    return billing_records

def generate_medical_records(n=100000, patient_ids=None, doctor_ids=None):
    medical_records = []
    statuses = ["OPEN", "CLOSED", "FOLLOW_UP"]
    for _ in range(n):
        record = MedicalRecord(
            patient_id=random.choice(patient_ids),
            doctor_id=random.choice(doctor_ids),
            diagnosis=fake.sentence(nb_words=5),
            treatment=fake.sentence(nb_words=10),
            status=random.choice(statuses),
            date=fake.date_time_this_year()
        )
        medical_records.append(record)
    return medical_records

def generate_medicines(n=1000):
    medicines = []
    for _ in range(n):
        medicine = Medicine(
            name=fake.word(),
            quantity=random.randint(1, 500)
        )
        medicines.append(medicine)
    return medicines

def populate_database():
    with Session(engine) as session:
        # Generate and add patients
        patients = generate_patients(100000)
        session.bulk_save_objects(patients)
        session.commit()

        # Generate and add billing records
        patient_ids = [p.id for p in session.query(Patient.id).all()]
        billing_records = generate_billing_records(100000, patient_ids)
        session.bulk_save_objects(billing_records)
        session.commit()

        # Generate and add medical records
        doctor_ids = [1, 2, 3, 4, 5]  # Example doctor IDs
        medical_records = generate_medical_records(100000, patient_ids, doctor_ids)
        session.bulk_save_objects(medical_records)
        session.commit()

        # Generate and add medicines
        medicines = generate_medicines(1000)
        session.bulk_save_objects(medicines)
        session.commit()

populate_database()
