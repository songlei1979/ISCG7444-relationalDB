# Student Grades Management System

A simple web application for managing student grades using Flask and MySQL.

## Database Setup

1. **Create the database:**
   ```sql
   CREATE DATABASE student_grades;
   USE student_grades;
   ```

2. **Run the database structure script:**
   ```bash
   mysql -u lei -p -h 192.168.31.228 < database_structure.sql
   ```
   Enter password: `Unitec123`

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

## Features

- **Student Management:** Add and view students
- **Course Management:** Add and view courses  
- **Grade Management:** Add and view student grades
- **Responsive Design:** Works on desktop and mobile devices

## Database Structure

The application uses three main tables:

- **students:** Stores student information (ID, name, email, enrollment date)
- **courses:** Stores course information (ID, code, name, credits)
- **grades:** Stores grade information linking students to courses with grades, semester, and year

## Configuration

Database connection settings are configured in `app.py`:
- Host: host_ip
- Username: username
- Password: password
- Database: student_grades

## Usage

1. Start by adding students and courses
2. Then add grades for students in specific courses
3. View all data through the web interface
