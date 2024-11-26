from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .models import user, patient, medical_record, billing, inventory as inventory_model
from .routers import auth, patients, medical_records, billing as billing_router, inventory

# Create database tables
user.Base.metadata.create_all(bind=engine)
patient.Base.metadata.create_all(bind=engine)
medical_record.Base.metadata.create_all(bind=engine)
billing.Base.metadata.create_all(bind=engine)
inventory_model.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Clinic API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, tags=["Authentication"])
app.include_router(patients.router, prefix="/patients", tags=["Patients"])
app.include_router(medical_records.router, prefix="/records", tags=["Medical Records"])
app.include_router(billing_router.router, prefix="/billing", tags=["Billing"])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])

@app.get("/")
async def root():
    return {"message": "Welcome to Clinic API"}