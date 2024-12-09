-- Create a new database
CREATE DATABASE IF NOT EXISTS Insurance;
USE Insurance;

-- Create a table for patients information
CREATE TABLE Patients (
    PatientID INT AUTO_INCREMENT PRIMARY KEY,         -- Unique Patient ID
    FirstName VARCHAR(100) NOT NULL,                   -- Patient's first name
    LastName VARCHAR(100) NOT NULL,                    -- Patient's last name
    DateOfBirth DATE NOT NULL,                         -- Patient's date of birth
    Address VARCHAR(255),                              -- Patient's address
    PhoneNumber VARCHAR(20),                           -- Patient's phone number
    Email VARCHAR(100)                                 -- Patient's email address
);

-- Create a table for storing Insurance Information
CREATE TABLE InsuranceInformation (
    InsuranceID INT AUTO_INCREMENT PRIMARY KEY,       -- Unique ID for each insurance entry
    PatientID INT NOT NULL,                           -- Reference to Patient (Foreign Key)
    InsuranceProvider VARCHAR(255) NOT NULL,          -- Insurance provider name
    PolicyNumber VARCHAR(255) NOT NULL,               -- Insurance policy number
    Copay DECIMAL(10, 2),                             -- Copay amount
    Deductible DECIMAL(10, 2),                        -- Deductible amount
    CoveredServices TEXT,                             -- List of covered services
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- Timestamp when updated
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID) -- References the Patients table
);

-- Create a table for storing Copay/Deductible information
CREATE TABLE CopayDeductible (
    CopayDeductibleID INT AUTO_INCREMENT PRIMARY KEY,  -- Unique ID for each entry
    InsuranceID INT NOT NULL,                          -- Foreign Key to InsuranceInformation
    PatientID INT NOT NULL,                            -- Foreign Key to Patients table
    CopayAmount DECIMAL(10, 2),                        -- Copay amount for the patient
    DeductibleAmount DECIMAL(10, 2),                   -- Deductible amount for the patient
    RemainingDeductible DECIMAL(10, 2),                -- Remaining deductible for the patient
    FOREIGN KEY (InsuranceID) REFERENCES InsuranceInformation(InsuranceID), -- Links to Insurance Information
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID) -- Links to Patients table
);

-- Create a table for storing Bill information (Bill Remaining to Patient)
CREATE TABLE Bills (
    BillID INT AUTO_INCREMENT PRIMARY KEY,            -- Unique Bill ID
    PatientID INT NOT NULL,                            -- Foreign Key to Patients table
    TotalAmount DECIMAL(10, 2) NOT NULL,               -- Total amount of the bill
    InsurancePaid DECIMAL(10, 2) DEFAULT 0.00,         -- Amount paid by insurance
    AmountOwed DECIMAL(10, 2),                         -- Remaining balance owed by patient (regular column)
    BillDate DATE NOT NULL,                            -- Date of the bill
    BillStatus VARCHAR(50) DEFAULT 'Pending',          -- Bill status: Pending, Paid, Partial
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID) -- Links to Patients table
);

-- Create a table for storing Payments
CREATE TABLE Payments (
    PaymentID INT AUTO_INCREMENT PRIMARY KEY,          -- Unique Payment ID
    PatientID INT NOT NULL,                            -- Foreign Key to Patients table
    BillID INT NOT NULL,                               -- Foreign Key to Bills table
    PaymentAmount DECIMAL(10, 2) NOT NULL,             -- Amount paid by the patient
    PaymentMethod VARCHAR(50),                         -- Payment method (e.g., Credit Card, Cash, Insurance)
    PaymentDate DATE NOT NULL,                         -- Date of the payment
    PaymentStatus VARCHAR(50) DEFAULT 'Pending',       -- Status of the payment: Pending, Completed, Failed
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID), -- Links to Patients table
    FOREIGN KEY (BillID) REFERENCES Bills(BillID)      -- Links to Bills table
);

-- Insert sample patient data
INSERT INTO Patients (FirstName, LastName, DateOfBirth, Address, PhoneNumber, Email)
VALUES
('John', 'Doe', '1985-04-12', '123 Elm St, Springfield, IL', '555-1234', 'john.doe@example.com'),
('Jane', 'Smith', '1990-08-22', '456 Oak St, Springfield, IL', '555-5678', 'jane.smith@example.com');

-- Insert sample insurance information
INSERT INTO InsuranceInformation (PatientID, InsuranceProvider, PolicyNumber, Copay, Deductible, CoveredServices)
VALUES
(1, 'Blue Cross', 'BC12345', 20.00, 500.00, 'General Checkups, Emergency Services'),
(2, 'Aetna', 'AE98765', 15.00, 300.00, 'General Checkups, Lab Tests');

-- Insert sample copay and deductible information
INSERT INTO CopayDeductible (InsuranceID, PatientID, CopayAmount, DeductibleAmount, RemainingDeductible)
VALUES
(1, 1, 20.00, 500.00, 300.00),
(2, 2, 15.00, 300.00, 150.00);

-- Insert sample bill data
INSERT INTO Bills (PatientID, TotalAmount, InsurancePaid, AmountOwed, BillDate, BillStatus)
VALUES
(1, 500.00, 200.00, 300.00, '2024-12-01', 'Pending'),
(2, 300.00, 150.00, 150.00, '2024-12-02', 'Pending');

-- Insert sample payment data
INSERT INTO Payments (PatientID, BillID, PaymentAmount, PaymentMethod, PaymentDate, PaymentStatus)
VALUES
(1, 1, 200.00, 'Credit Card', '2024-12-03', 'Completed'),
(2, 2, 150.00, 'Cash', '2024-12-04', 'Completed');
