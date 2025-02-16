CREATE DATABASE ai;
USE ai;

CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    disease VARCHAR(100)
);

CREATE TABLE doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    clinic_name VARCHAR(100),
    doctor_name VARCHAR(100),
    specialty VARCHAR(100),
    experience INT,
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255)
);

CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    status ENUM('Pending', 'Approved', 'Cancelled') DEFAULT 'Pending',
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

SELECT * FROM information_schema.KEY_COLUMN_USAGE 
WHERE TABLE_NAME = 'appointments';


INSERT INTO doctors (clinic_name, doctor_name, specialty, experience, address, phone, email, password) 
VALUES 
('Apollo Clinic', 'Dr. Raju Sharma', 'Stuttering', 15, '123, MG Road, Amravati, Maharashtra', '9876543210', 'shreyash080204@gmail.com', 'password123'),
('Fortis Clinic', 'Dr. Anjali  verma', 'Stuttering', 10, '456, Station Road, Amravati, Maharashtra', '9876543211', 'anjalii.mehta@example.com', 'password456'),
('Max Healthcare', 'Dr. Vikramakaur Singh', 'Dyslexia', 20, '789, College Road, Amravati, Maharashtra', '9876543212', 'vikrami.singh@example.com', 'password789'),
('Medanta Clinic', 'Dr. Priya khan Iyer', 'Dyslexia', 12, '101, Airport Road, Amravati, Maharashtra', '9876543213', 'priyai.iyer@example.com', 'password101');




ALTER TABLE doctors 
ADD COLUMN age INT AFTER doctor_name,
ADD COLUMN gender ENUM('Male', 'Female', 'Other') AFTER age,
ADD COLUMN license_certificate_no VARCHAR(100) AFTER experience;
SET @num = 1000;

UPDATE doctors  
SET license_certificate_no = CONCAT('TEMP-', @num + id)  
WHERE id > 0;

SET SQL_SAFE_UPDATES = 0;
SET SQL_SAFE_UPDATES = 1;
ALTER TABLE doctors 
MODIFY COLUMN license_certificate_no VARCHAR(100)  UNIQUE;
ALTER TABLE patients 
DROP COLUMN name,
DROP COLUMN email,
DROP COLUMN password,
DROP COLUMN disease;
ALTER TABLE patients 
ADD COLUMN patient_name VARCHAR(100) NOT NULL,
ADD COLUMN age INT NOT NULL,
ADD COLUMN gender ENUM('Male', 'Female', 'Other') NOT NULL,
ADD COLUMN parents_name VARCHAR(100) NOT NULL,
ADD COLUMN contact_no VARCHAR(20) NOT NULL,
ADD COLUMN email VARCHAR(100) UNIQUE NOT NULL,
ADD COLUMN password VARCHAR(255) NOT NULL,
ADD COLUMN address TEXT NOT NULL,
ADD COLUMN disorder VARCHAR(100) NOT NULL;
select * from doctors;

ALTER TABLE patients 

add COLUMN patient_name varchar(100) not null after id;




select * from patients;

show TABLES;