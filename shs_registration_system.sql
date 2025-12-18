-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 18, 2025 at 08:50 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `shs_registration_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `academic`
--

CREATE TABLE `academic` (
  `StudentID` varchar(16) NOT NULL,
  `GradeLevel` enum('Grade 11','Grade 12') DEFAULT NULL,
  `Track` enum('Academic','TVL') DEFAULT NULL,
  `Strand` enum('STEM','HUMSS','ABM','ICT','HE','IA','GAS') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `academic`
--

INSERT INTO `academic` (`StudentID`, `GradeLevel`, `Track`, `Strand`) VALUES
('S1', 'Grade 11', 'Academic', 'STEM'),
('S2', 'Grade 11', 'Academic', 'HUMSS'),
('S3', 'Grade 12', 'Academic', 'ABM'),
('S4', 'Grade 11', 'TVL', 'ICT'),
('S5', 'Grade 12', 'TVL', 'HE'),
('S6', 'Grade 11', 'TVL', 'IA'),
('S7', 'Grade 11', 'Academic', 'STEM');

-- --------------------------------------------------------

--
-- Table structure for table `accounts`
--

CREATE TABLE `accounts` (
  `AccountID` varchar(16) NOT NULL,
  `Username` varchar(50) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `SecurityQuestion` varchar(100) DEFAULT NULL,
  `SecurityAnswer` varchar(100) DEFAULT NULL,
  `Role` enum('student','registrar','admin') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts`
--

INSERT INTO `accounts` (`AccountID`, `Username`, `Password`, `SecurityQuestion`, `SecurityAnswer`, `Role`) VALUES
('A1', 'student1', 'password123', 'What is your favorite color?', 'Blue', 'student'),
('A10', 'admin1', 'password123', 'What is your favorite color?', 'Purple', 'admin'),
('A11', '1', '1', 'What is your favorite color?', '1', 'student'),
('A2', 'student2', 'password123', 'What is your favorite food?', 'Pizza', 'student'),
('A3', 'student3', 'password123', 'What is your favorite animal', 'Dog', 'student'),
('A4', 'student4', 'password123', 'What is your favorite color?', 'Red', 'student'),
('A5', 'student5', 'password123', 'What is your favorite food?', 'Burger', 'student'),
('A6', 'student6', 'password123', 'What is your favorite animal', 'Cat', 'student'),
('A7', 'registrar1', 'password123', 'What is your favorite color?', 'Green', 'registrar'),
('A8', 'registrar2', 'password123', 'What is your favorite food?', 'Pasta', 'registrar'),
('A9', 'registrar3', 'password123', 'What is your favorite animal', 'Bird', 'registrar');

-- --------------------------------------------------------

--
-- Table structure for table `address`
--

CREATE TABLE `address` (
  `StudentID` varchar(16) NOT NULL,
  `HouseNum` varchar(50) DEFAULT NULL,
  `Barangay` varchar(100) DEFAULT NULL,
  `City` varchar(100) DEFAULT NULL,
  `Province` varchar(100) DEFAULT NULL,
  `ZIP` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `address`
--

INSERT INTO `address` (`StudentID`, `HouseNum`, `Barangay`, `City`, `Province`, `ZIP`) VALUES
('S1', '123', 'Barangay 1', 'Davao City', 'Davao Del Sur', '8000'),
('S2', '456', 'Barangay 2', 'Davao City', 'Davao Del Sur', '8000'),
('S3', '789', 'Barangay 3', 'Davao City', 'Davao Del Sur', '8000'),
('S4', '321', 'Barangay 4', 'Davao City', 'Davao Del Sur', '8000'),
('S5', '654', 'Barangay 5', 'Davao City', 'Davao Del Sur', '8000'),
('S6', '987', 'Barangay 6', 'Davao City', 'Davao Del Sur', '8000'),
('S7', '1', '1', '1', '1', '1');

-- --------------------------------------------------------

--
-- Table structure for table `documents`
--

CREATE TABLE `documents` (
  `DocumentID` varchar(16) NOT NULL,
  `StudentID` varchar(16) DEFAULT NULL,
  `RegistrationID` varchar(16) DEFAULT NULL,
  `DocumentType` varchar(50) DEFAULT NULL,
  `FilePath` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `documents`
--

INSERT INTO `documents` (`DocumentID`, `StudentID`, `RegistrationID`, `DocumentType`, `FilePath`) VALUES
('D1', 'S1', 'R1', 'Form 137', 'files/Form137.txt'),
('D10', 'S3', 'R3', 'Birth Certificate', 'files/Birth Certificate.txt'),
('D11', 'S4', 'R4', 'Form 137', 'files/Form137.txt'),
('D12', 'S4', 'R4', 'Birth Certificate', 'files/Birth Certificate.txt'),
('D13', 'S5', 'R5', 'Form 137', 'files/Form137.txt'),
('D14', 'S5', 'R5', 'Birth Certificate', 'files/Birth Certificate.txt'),
('D15', 'S5', 'R5', 'Report Card', 'files/Report Card.txt'),
('D16', 'S5', 'R5', 'Good Moral', 'files/Good Moral.txt'),
('D17', 'S6', 'R6', 'Form 137', 'files/Form137.txt'),
('D18', 'S6', 'R6', 'Birth Certificate', 'files/Birth Certificate.txt'),
('D19', 'S7', 'R7', 'Form 137', 'D:/Applications/Productivity/PyCharm/Projects/IT5 Final Project/SHS_Student_Registration_System/files/Form137.txt'),
('D2', 'S1', 'R1', 'Birth Certificate', 'files/Birth Certificate.txt'),
('D20', 'S7', 'R7', 'Birth Certificate', 'D:/Applications/Productivity/PyCharm/Projects/IT5 Final Project/SHS_Student_Registration_System/files/Birth Certificate.txt'),
('D21', 'S7', 'R7', 'Report Card', 'D:/Applications/Productivity/PyCharm/Projects/IT5 Final Project/SHS_Student_Registration_System/files/Report Card.txt'),
('D22', 'S7', 'R7', 'Good Moral', 'D:/Applications/Productivity/PyCharm/Projects/IT5 Final Project/SHS_Student_Registration_System/files/Good Moral.txt'),
('D3', 'S1', 'R1', 'Report Card', 'files/Report Card.txt'),
('D4', 'S1', 'R1', 'Good Moral', 'files/Good Moral.txt'),
('D5', 'S2', 'R2', 'Form 137', 'files/Form137.txt'),
('D6', 'S2', 'R2', 'Birth Certificate', 'files/Birth Certificate.txt'),
('D7', 'S2', 'R2', 'Report Card', 'files/Report Card.txt'),
('D8', 'S2', 'R2', 'Good Moral', 'files/Good Moral.txt'),
('D9', 'S3', 'R3', 'Form 137', 'files/Form137.txt');

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

CREATE TABLE `employee` (
  `EmployeeID` varchar(16) NOT NULL,
  `AccountID` varchar(16) DEFAULT NULL,
  `FullName` varchar(100) DEFAULT NULL,
  `ContactNum` varchar(20) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employee`
--

INSERT INTO `employee` (`EmployeeID`, `AccountID`, `FullName`, `ContactNum`, `Email`) VALUES
('E1', 'A7', 'Registrar One', '09123456795', 'registrar1@school.edu'),
('E2', 'A8', 'Registrar Two', '09123456796', 'registrar2@school.edu'),
('E3', 'A9', 'Registrar Three', '09123456797', 'registrar3@school.edu'),
('E4', 'A10', 'Admin One', '09123456798', 'admin1@school.edu');

-- --------------------------------------------------------

--
-- Table structure for table `parent_guardian`
--

CREATE TABLE `parent_guardian` (
  `StudentID` varchar(16) NOT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `Relationship` varchar(50) DEFAULT NULL,
  `Occupation` varchar(100) DEFAULT NULL,
  `Address` varchar(200) DEFAULT NULL,
  `ContactNum` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `parent_guardian`
--

INSERT INTO `parent_guardian` (`StudentID`, `Name`, `Relationship`, `Occupation`, `Address`, `ContactNum`) VALUES
('S1', 'Pedro Dela Cruz', 'Father', 'Engineer', '123 Barangay 1, Davao City, Davao Del Sur, 8000', '09123456788'),
('S2', 'Rosa Garcia', 'Mother', 'Teacher', '456 Barangay 2, Davao City, Davao Del Sur, 8000', '09123456789'),
('S3', 'Miguel Lopez', 'Father', 'Doctor', '789 Barangay 3, Davao City, Davao Del Sur, 8000', '09123456790'),
('S4', 'Carmen Torres', 'Mother', 'Nurse', '321 Barangay 4, Davao City, Davao Del Sur, 8000', '09123456791'),
('S5', 'Roberto Ramos', 'Father', 'Lawyer', '654 Barangay 5, Davao City, Davao Del Sur, 8000', '09123456792'),
('S6', 'Elena Aquino', 'Mother', 'Accountant', '987 Barangay 6, Davao City, Davao Del Sur, 8000', '09123456793'),
('S7', '1', '1', '1', '1, 1, 1, 1, 1', '1');

-- --------------------------------------------------------

--
-- Table structure for table `registration_record`
--

CREATE TABLE `registration_record` (
  `RegistrationID` varchar(16) NOT NULL,
  `StudentID` varchar(16) NOT NULL,
  `GradeLevel` enum('Grade 11','Grade 12') DEFAULT NULL,
  `Track` enum('Academic','TVL') DEFAULT NULL,
  `Strand` enum('STEM','HUMSS','ABM','ICT','HE','IA','GAS') DEFAULT NULL,
  `SchoolYear` varchar(20) DEFAULT NULL,
  `Status` enum('Pending','Approved','Rejected') DEFAULT 'Pending',
  `SubmittedAt` datetime DEFAULT current_timestamp(),
  `ValidatedBy` varchar(16) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `registration_record`
--

INSERT INTO `registration_record` (`RegistrationID`, `StudentID`, `GradeLevel`, `Track`, `Strand`, `SchoolYear`, `Status`, `SubmittedAt`, `ValidatedBy`) VALUES
('R1', 'S1', 'Grade 11', 'Academic', 'STEM', '2024-2025', 'Pending', '2025-12-18 00:58:13', NULL),
('R2', 'S2', 'Grade 11', 'Academic', 'HUMSS', '2024-2025', 'Approved', '2025-12-18 00:58:13', 'E1'),
('R3', 'S3', 'Grade 12', 'Academic', 'ABM', '2024-2025', 'Pending', '2025-12-18 00:58:13', NULL),
('R4', 'S4', 'Grade 11', 'TVL', 'ICT', '2024-2025', 'Rejected', '2025-12-18 00:58:13', 'E2'),
('R5', 'S5', 'Grade 12', 'TVL', 'HE', '2024-2025', 'Approved', '2025-12-18 00:58:13', 'E1'),
('R6', 'S6', 'Grade 11', 'TVL', 'IA', '2024-2025', 'Rejected', '2025-12-18 00:58:13', 'E1'),
('R7', 'S7', 'Grade 11', 'Academic', 'STEM', '2025-2026', 'Pending', '2025-12-18 05:30:29', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `StudentID` varchar(16) NOT NULL,
  `AccountID` varchar(16) NOT NULL,
  `LRN` varchar(12) DEFAULT NULL,
  `FirstName` varchar(50) DEFAULT NULL,
  `MiddleName` varchar(50) DEFAULT NULL,
  `LastName` varchar(50) DEFAULT NULL,
  `Gender` enum('Male','Female') DEFAULT NULL,
  `Birthdate` date DEFAULT NULL,
  `Age` int(11) DEFAULT NULL,
  `Nationality` varchar(50) DEFAULT NULL,
  `Religion` varchar(50) DEFAULT NULL,
  `CivilStatus` varchar(20) DEFAULT NULL,
  `ContactNum` varchar(20) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`StudentID`, `AccountID`, `LRN`, `FirstName`, `MiddleName`, `LastName`, `Gender`, `Birthdate`, `Age`, `Nationality`, `Religion`, `CivilStatus`, `ContactNum`, `Email`) VALUES
('S1', 'A1', '123456789012', 'Juan', 'Cruz', 'Dela Cruz', 'Male', '2008-05-15', 16, 'Filipino', 'Catholic', 'Single', '09123456789', 'juan.delacruz@email.com'),
('S2', 'A2', '123456789013', 'Maria', 'Santos', 'Garcia', 'Female', '2008-08-20', 16, 'Filipino', 'Catholic', 'Single', '09123456790', 'maria.garcia@email.com'),
('S3', 'A3', '123456789014', 'Jose', 'Reyes', 'Lopez', 'Male', '2007-12-10', 17, 'Filipino', 'Catholic', 'Single', '09123456791', 'jose.lopez@email.com'),
('S4', 'A4', '123456789015', 'Ana', 'Villanueva', 'Torres', 'Female', '2008-03-25', 16, 'Filipino', 'Catholic', 'Single', '09123456792', 'ana.torres@email.com'),
('S5', 'A5', '123456789016', 'Carlos', 'Fernandez', 'Ramos', 'Male', '2007-09-30', 17, 'Filipino', 'Catholic', 'Single', '09123456793', 'carlos.ramos@email.com'),
('S6', 'A6', '123456789017', 'Sofia', 'Martinez', 'Aquino', 'Female', '2008-07-12', 16, 'Filipino', 'Catholic', 'Single', '09123456794', 'sofia.aquino@email.com'),
('S7', 'A11', '1', '1', '1', '1', 'Male', '2025-12-18', 1, '1', '1', '1', '1', 'redpajela@gmail.com');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `academic`
--
ALTER TABLE `academic`
  ADD PRIMARY KEY (`StudentID`);

--
-- Indexes for table `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`AccountID`),
  ADD UNIQUE KEY `Username` (`Username`);

--
-- Indexes for table `address`
--
ALTER TABLE `address`
  ADD PRIMARY KEY (`StudentID`);

--
-- Indexes for table `documents`
--
ALTER TABLE `documents`
  ADD PRIMARY KEY (`DocumentID`),
  ADD KEY `fk_documents_student` (`StudentID`),
  ADD KEY `fk_documents_registration` (`RegistrationID`);

--
-- Indexes for table `employee`
--
ALTER TABLE `employee`
  ADD PRIMARY KEY (`EmployeeID`),
  ADD UNIQUE KEY `AccountID` (`AccountID`);

--
-- Indexes for table `parent_guardian`
--
ALTER TABLE `parent_guardian`
  ADD PRIMARY KEY (`StudentID`);

--
-- Indexes for table `registration_record`
--
ALTER TABLE `registration_record`
  ADD PRIMARY KEY (`RegistrationID`),
  ADD KEY `fk_registration_student` (`StudentID`),
  ADD KEY `fk_registration_employee` (`ValidatedBy`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`StudentID`),
  ADD UNIQUE KEY `LRN` (`LRN`),
  ADD KEY `fk_students_account` (`AccountID`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `academic`
--
ALTER TABLE `academic`
  ADD CONSTRAINT `fk_academic_student` FOREIGN KEY (`StudentID`) REFERENCES `students` (`StudentID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `address`
--
ALTER TABLE `address`
  ADD CONSTRAINT `fk_address_student` FOREIGN KEY (`StudentID`) REFERENCES `students` (`StudentID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `documents`
--
ALTER TABLE `documents`
  ADD CONSTRAINT `fk_documents_registration` FOREIGN KEY (`RegistrationID`) REFERENCES `registration_record` (`RegistrationID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_documents_student` FOREIGN KEY (`StudentID`) REFERENCES `students` (`StudentID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `employee`
--
ALTER TABLE `employee`
  ADD CONSTRAINT `fk_employee_account` FOREIGN KEY (`AccountID`) REFERENCES `accounts` (`AccountID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `parent_guardian`
--
ALTER TABLE `parent_guardian`
  ADD CONSTRAINT `fk_parent_student` FOREIGN KEY (`StudentID`) REFERENCES `students` (`StudentID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `registration_record`
--
ALTER TABLE `registration_record`
  ADD CONSTRAINT `fk_registration_employee` FOREIGN KEY (`ValidatedBy`) REFERENCES `employee` (`EmployeeID`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_registration_student` FOREIGN KEY (`StudentID`) REFERENCES `students` (`StudentID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `students`
--
ALTER TABLE `students`
  ADD CONSTRAINT `fk_students_account` FOREIGN KEY (`AccountID`) REFERENCES `accounts` (`AccountID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
