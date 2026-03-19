-- Student Grades Database Structure
-- Create database first: CREATE DATABASE student_grades;
-- USE student_grades;

-- Students table
CREATE TABLE students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    enrollment_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Courses table
CREATE TABLE courses (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    course_code VARCHAR(20) UNIQUE NOT NULL,
    course_name VARCHAR(100) NOT NULL,
    credits INT NOT NULL DEFAULT 3,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Grades table
CREATE TABLE grades (
    grade_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    grade DECIMAL(5,2) NOT NULL,
    semester VARCHAR(20) NOT NULL,
    year INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    UNIQUE KEY unique_student_course_semester (student_id, course_id, semester, year)
);

-- Sample data (optional)
INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
('John', 'Smith', 'john.smith@email.com', '2023-09-01'),
('Jane', 'Doe', 'jane.doe@email.com', '2023-09-01'),
('Mike', 'Johnson', 'mike.johnson@email.com', '2023-09-01');

INSERT INTO courses (course_code, course_name, credits) VALUES
('CS101', 'Introduction to Computer Science', 3),
('MATH201', 'Calculus II', 4),
('ENG102', 'English Composition', 3);

INSERT INTO grades (student_id, course_id, grade, semester, year) VALUES
(1, 1, 85.5, 'Fall', 2023),
(1, 2, 78.0, 'Fall', 2023),
(2, 1, 92.0, 'Fall', 2023),
(2, 3, 88.5, 'Fall', 2023),
(3, 2, 76.5, 'Fall', 2023);
