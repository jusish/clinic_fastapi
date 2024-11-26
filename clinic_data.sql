-- Reset sequences
TRUNCATE users, patients, medical_records, medicines, billing_records RESTART IDENTITY CASCADE;

-- Insert doctors with different specializations
INSERT INTO users (username, email, hashed_password, specialization, role, is_active) VALUES
('dr.smith', 'smith@clinic.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN9V3UF9T3HJGQZsuHhJi', 'cardiology', 'DOCTOR', true),
('dr.jones', 'jones@clinic.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN9V3UF9T3HJGQZsuHhJi', 'neurology', 'DOCTOR', true),
('dr.wilson', 'wilson@clinic.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN9V3UF9T3HJGQZsuHhJi', 'pediatrics', 'DOCTOR', true),
('dr.williams', 'williams@clinic.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN9V3UF9T3HJGQZsuHhJi', 'orthopedics', 'DOCTOR', true),
('admin', 'admin@clinic.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN9V3UF9T3HJGQZsuHhJi', 'cardiology', 'ADMIN', true);

-- Insert 200 patients
INSERT INTO patients (name, dob, contact_info, date_attended) 
SELECT 
    'Patient ' || generate_series,
    date '1950-01-01' + (random() * (date '2000-01-01' - date '1950-01-01'))::int * '1 day'::interval,
    '+1-' || trunc(random() * 900 + 100)::text || '-' || trunc(random() * 900 + 100)::text || '-' || trunc(random() * 9000 + 1000)::text,
    date '2023-01-01' + (random() * (date '2024-03-01' - date '2023-01-01'))::int * '1 day'::interval
FROM generate_series(1, 200);

-- Insert 200 medical records
INSERT INTO medical_records (patient_id, doctor_id, diagnosis, treatment, status, date)
SELECT 
    patient_id,
    doctor_id,
    diagnoses.diagnosis,
    treatments.treatment,
    status.status,
    timestamp '2023-01-01 00:00:00' + (random() * (timestamp '2024-03-01 00:00:00' - timestamp '2023-01-01 00:00:00'))
FROM (
    SELECT generate_series AS patient_id FROM generate_series(1, 200)
) AS patients
CROSS JOIN (
    SELECT id AS doctor_id FROM users WHERE role = 'DOCTOR' LIMIT 1
) AS doctors
CROSS JOIN (
    SELECT unnest(ARRAY['Common Cold', 'Hypertension', 'Diabetes', 'Arthritis', 'Migraine']) AS diagnosis
) AS diagnoses
CROSS JOIN (
    SELECT unnest(ARRAY['Rest and fluids', 'Medication prescribed', 'Diet and exercise', 'Physical therapy', 'Pain management']) AS treatment
) AS treatments
CROSS JOIN (
    SELECT unnest(ARRAY['OPEN', 'CLOSED', 'FOLLOW_UP']) AS status
) AS status
LIMIT 200;

-- Insert 200 medicines
INSERT INTO medicines (name, quantity)
SELECT 
    'Medicine ' || generate_series,
    trunc(random() * 100 + 1)::int
FROM generate_series(1, 200);

-- Insert 200 billing records
INSERT INTO billing_records (patient_id, total_cost, date)
SELECT 
    patient_id,
    (random() * 1000 + 100)::numeric(10,2),
    timestamp '2023-01-01 00:00:00' + (random() * (timestamp '2024-03-01 00:00:00' - timestamp '2023-01-01 00:00:00'))
FROM (
    SELECT generate_series AS patient_id FROM generate_series(1, 200)
) AS patients; 