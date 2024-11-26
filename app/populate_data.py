from sqlalchemy.orm import Session
from faker import Faker
from random import choice, randint
from .database import get_db
from .models.patient import Patient
from .models.medical_record import MedicalRecord
from .models.inventory import Medicine
from .models.billing import BillingRecord
from .models.user import User
from .config import settings
from werkzeug.security import generate_password_hash

fake = Faker()

def create_fake_patients(db: Session, num: int):
    for _ in range(num):
        patient = Patient(
            name=fake.name(),
            dob=fake.date_of_birth(minimum_age=18, maximum_age=90),
            contact_info=fake.phone_number(),
            date_attended=fake.date_this_decade()
        )
        db.add(patient)
    db.commit()

def create_fake_doctors(db: Session, num: int):
    existing_usernames = {user.username for user in db.query(User).all()}  # Get existing usernames
    for i in range(1, num + 1):
        username = f"doctor{i}"
        while username in existing_usernames:  # Ensure the username is unique
            username = f"doctor{i}_{randint(1, 100)}"  # Append a random number if duplicate
        doctor = User(
            username=username,
            email=f"doctor{i}@example.com",
            hashed_password=generate_password_hash("password123"),
            specialization="cardiology",
            role="DOCTOR"
        )
        db.add(doctor)
    db.commit()

def create_fake_medical_records(db: Session, num: int):
    patients = db.query(Patient).all()
    doctors = db.query(User).filter(User.role == "DOCTOR").all()
    if not doctors:
        raise ValueError("No doctors found in database. Please create doctors first.")
    
    for _ in range(num):
        record = MedicalRecord(
            patient_id=choice(patients).id,
            doctor_id=choice(doctors).id,  # Use actual doctor IDs
            diagnosis=fake.word(),
            treatment=fake.sentence(),
            status=choice(['OPEN', 'CLOSED', 'FOLLOW_UP']),
        )
        db.add(record)
    db.commit()

def create_fake_medicines(db: Session, num: int):
    for _ in range(num):
        medicine = Medicine(
            name=fake.word(),
            quantity=randint(1, 100)
        )
        db.add(medicine)
    db.commit()

def create_fake_billing_records(db: Session, num: int):
    patients = db.query(Patient).all()
    for _ in range(num):
        billing = BillingRecord(
            patient_id=choice(patients).id,
            total_cost=round(randint(100, 1000) + fake.random_number(digits=2) / 100, 2),
        )
        db.add(billing)
    db.commit()

def main():
    db = next(get_db())
    create_fake_doctors(db, 10)  # Create 10 doctors first
    create_fake_patients(db, 200)
    create_fake_medical_records(db, 200)
    create_fake_medicines(db, 200)
    create_fake_billing_records(db, 200)
    print("Data population complete.")

if __name__ == "__main__":
    main() 