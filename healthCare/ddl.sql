-- Create a new database
CREATE DATABASE IF NOT EXISTS healthcaremanagement;
USE healthcaremanagement;


-- Table for storing patient details (Patient Profile)
CREATE TABLE patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    contact_info VARCHAR(150),
    address VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for storing physician details
CREATE TABLE physicians (
    physician_id INT AUTO_INCREMENT PRIMARY KEY,
    physician_name VARCHAR(255) NOT NULL,
    specialty VARCHAR(100),
    contact_info VARCHAR(150),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for storing appointments
CREATE TABLE appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    physician_id INT NOT NULL,
    appointment_datetime DATETIME NOT NULL,
    notes TEXT,
    status ENUM('Scheduled', 'Rescheduled', 'Cancelled', 'Completed') DEFAULT 'Scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (physician_id) REFERENCES physicians(physician_id)
);

-- Table for managing SOAP Records
CREATE TABLE soap_records (
    soap_record_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    physician_id INT NOT NULL,
    visit_datetime DATETIME NOT NULL,
    subjective_observations TEXT,
    objective_data JSON,
    diagnosis TEXT,
    treatment_plan TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (physician_id) REFERENCES physicians(physician_id)
);

-- Table for managing visits (Visit Management)
CREATE TABLE visits (
    visit_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    physician_id INT NOT NULL,
    visit_type ENUM('Office', 'ER', 'Inpatient') NOT NULL,
    admission_date DATE,
    discharge_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (physician_id) REFERENCES physicians(physician_id)
);

-- Table for After Visit Summary
CREATE TABLE after_visit_summary (
    summary_id INT AUTO_INCREMENT PRIMARY KEY,
    visit_id INT NOT NULL,
    notes_on_care TEXT,
    patient_instructions TEXT,
    follow_up_details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (visit_id) REFERENCES visits(visit_id)
);

/*
-- Insert sample patients
INSERT INTO patients (patient_name, date_of_birth, contact_info, address) VALUES
('John Doe', '1980-01-01', 'john@example.com', '123 Elm St'),
('Jane Smith', '1990-06-15', 'jane@example.com', '456 Oak St');

-- Insert sample physicians
INSERT INTO physicians (physician_name, specialty, contact_info) VALUES
('Dr. Smith', 'Cardiology', 'smith@example.com'),
('Dr. Johnson', 'Pediatrics', 'johnson@example.com'),
('Dr. Lee', 'Orthopedics', 'lee@example.com');

-- Insert sample appointments
INSERT INTO appointments (patient_id, physician_id, appointment_datetime, notes, status) VALUES
(1, 1, '2024-12-05 10:30:00', 'Routine check-up', 'Scheduled'),
(2, 2, '2024-12-10 15:00:00', 'Annual physical exam', 'Scheduled');

-- Insert sample SOAP records
INSERT INTO soap_records (patient_id, physician_id, visit_datetime, subjective_observations, objective_data, diagnosis, treatment_plan) VALUES
(1, 1, '2024-12-05 10:30:00', 'Patient complains of fatigue', '{"BP": "120/80", "HR": "72"}', 'Mild anemia', 'Prescribe iron supplements'),
(2, 2, '2024-12-10 15:00:00', 'Patient reports fever', '{"Temp": "101F"}', 'Viral fever', 'Prescribe antipyretics');

-- Insert sample visits
INSERT INTO visits (patient_id, physician_id, visit_type, admission_date, discharge_date, notes) VALUES
(1, 1, 'Office', '2024-12-05', NULL, 'Routine consultation'),
(2, 2, 'Office', '2024-12-10', NULL, 'Follow-up for annual exam');

-- Insert sample after visit summaries
INSERT INTO after_visit_summary (visit_id, notes_on_care, patient_instructions, follow_up_details) VALUES
(1, 'Routine check-up completed', 'Increase physical activity and improve diet', 'Follow up in 6 months'),
(2, 'Fever resolved', 'Continue medication for 2 more days', 'No further follow-up needed'); */



