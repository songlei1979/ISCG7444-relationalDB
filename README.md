# Student Grades Management API

A RESTful API for managing student grades using Flask and MySQL. This application provides endpoints for student, course, and grade management with automatic database initialization.

## Features

- **Automatic Database Setup:** Creates database and tables automatically on first run
- **RESTful API:** JSON-based endpoints for all operations
- **Student Management:** Add and retrieve students
- **Course Management:** Add and retrieve courses  
- **Grade Management:** Add and retrieve student grades
- **Error Handling:** Comprehensive error responses with proper HTTP status codes

## Prerequisites

- Python 3.7+
- MySQL Server (running locally or accessible)
- Required Python packages (see Installation section)

## Installation

### Option 1: Local Development

1. **Install dependencies:**
   ```bash
   pip install flask mysql-connector-python
   ```

2. **Ensure MySQL server is running:**
   - On macOS: `brew services start mysql` or use MySQL Workbench
   - On Windows: Start MySQL service from Services panel
   - On Linux: `sudo systemctl start mysql`

3. **Configure database connection (if needed):**
   - Edit `app.py` and modify the `DB_CONFIG` dictionary if your MySQL setup differs:
   ```python
   DB_CONFIG = {
       'host': 'localhost',      # MySQL server host
       'user': 'root',           # MySQL username
       'password': 'Unitec123'   # MySQL password
   }
   ```

### Option 2: Docker

1. **Install Docker** if not already installed

2. **Build the Docker image:**
   ```bash
   docker build -t student-grades-api .
   ```

3. **Run the container:**
   ```bash
   docker run -p 5000:5000 --name student-grades-api student-grades-api
   ```

4. **To run in the background:**
   ```bash
   docker run -d -p 5000:5000 --name student-grades-api student-grades-api
   ```

5. **To stop the container:**
   ```bash
   docker stop student-grades-api
   ```

6. **To view logs:**
   ```bash
   docker logs student-grades-api
   ```

7. **To remove the container:**
   ```bash
   docker rm student-grades-api
   ```

## Running the Application

### Local Development

1. **Start the API server:**
   ```bash
   python app.py
   ```

2. **The application will:**
   - Automatically check if the `student_grades` database exists
   - Create the database if it doesn't exist
   - Set up tables and insert sample data from `database_structure.sql`
   - Start the Flask API server on port 5000

3. **Access the API:**
   - Base URL: `http://localhost:5000`
   - API endpoints are listed below

### Docker

1. **Run the container:**
   ```bash
   docker run -p 5000:5000 --name student-grades-api student-grades-api
   ```

2. **The application will:**
   - Start the Flask API server
   - Attempt to connect to MySQL database (must be running separately)
   - Initialize database with sample data if needed

3. **Access the API:**
   - Base URL: `http://localhost:5000`
   - API endpoints are listed below

4. **Note:** Docker container expects MySQL to be running separately on localhost:3306 with the configured credentials

## API Endpoints

### Base Endpoint
- **GET** `/`
  - Returns API information and available endpoints
  - Example response:
  ```json
  {
    "message": "Student Grades API",
    "database_status": "connected",
    "database_name": "student_grades",
    "endpoints": {
      "students": "/students",
      "courses": "/courses",
      "grades": "/grades",
      "add_student": "/add_student",
      "add_course": "/add_course",
      "add_grade": "/add_grade",
      "add_grade_options": "/add_grade_options"
    }
  }
  ```

### Students
- **GET** `/students`
  - Retrieves all students
  - Response: `{"success": true, "data": [...], "count": 3}`

- **POST** `/add_student`
  - Adds a new student
  - Request body:
  ```json
  {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@email.com",
    "enrollment_date": "2023-09-01"
  }
  ```
  - Response: `{"success": true, "message": "Student added successfully!"}`

### Courses
- **GET** `/courses`
  - Retrieves all courses
  - Response: `{"success": true, "data": [...], "count": 3}`

- **POST** `/add_course`
  - Adds a new course
  - Request body:
  ```json
  {
    "course_code": "CS101",
    "course_name": "Introduction to Computer Science",
    "credits": 3
  }
  ```
  - Response: `{"success": true, "message": "Course added successfully!"}`

### Grades
- **GET** `/grades`
  - Retrieves all grades with student and course information
  - Response: `{"success": true, "data": [...], "count": 5}`

- **POST** `/add_grade`
  - Adds a new grade
  - Request body:
  ```json
  {
    "student_id": 1,
    "course_id": 1,
    "grade": 85.5,
    "semester": "Fall",
    "year": 2023
  }
  ```
  - Response: `{"success": true, "message": "Grade added successfully!"}`

- **GET** `/add_grade_options`
  - Retrieves available students and courses for grade creation
  - Response: `{"success": true, "students": [...], "courses": [...]}`

## Database Structure

The application uses three main tables:

- **students:** Stores student information (ID, name, email, enrollment date)
- **courses:** Stores course information (ID, code, name, credits)
- **grades:** Stores grade information linking students to courses with grades, semester, and year

## Sample Data

The application automatically populates the database with sample data on first run:

**Students:**
- John Smith (john.smith@email.com)
- Jane Doe (jane.doe@email.com)
- Mike Johnson (mike.johnson@email.com)

**Courses:**
- CS101: Introduction to Computer Science (3 credits)
- MATH201: Calculus II (4 credits)
- ENG102: English Composition (3 credits)

**Grades:**
- Multiple sample grade records linking students to courses

## Usage Examples

### Using curl

1. **Get all students:**
   ```bash
   curl http://localhost:5000/students
   ```

2. **Add a new student:**
   ```bash
   curl -X POST http://localhost:5000/add_student \
        -H "Content-Type: application/json" \
        -d '{"first_name": "Alice", "last_name": "Wilson", "email": "alice.wilson@email.com", "enrollment_date": "2023-09-01"}'
   ```

3. **Get all courses:**
   ```bash
   curl http://localhost:5000/courses
   ```

4. **Add a new course:**
   ```bash
   curl -X POST http://localhost:5000/add_course \
        -H "Content-Type: application/json" \
        -d '{"course_code": "PHYS101", "course_name": "Physics I", "credits": 4}'
   ```

5. **Get all grades:**
   ```bash
   curl http://localhost:5000/grades
   ```

6. **Add a new grade:**
   ```bash
   curl -X POST http://localhost:5000/add_grade \
        -H "Content-Type: application/json" \
        -d '{"student_id": 1, "course_id": 1, "grade": 92.0, "semester": "Spring", "year": 2024}'
   ```

### Using Python requests

```python
import requests
import json

base_url = "http://localhost:5000"

# Get all students
response = requests.get(f"{base_url}/students")
print(response.json())

# Add a new student
student_data = {
    "first_name": "Bob",
    "last_name": "Brown",
    "email": "bob.brown@email.com",
    "enrollment_date": "2023-09-01"
}
response = requests.post(f"{base_url}/add_student", json=student_data)
print(response.json())
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- **200:** Success
- **400:** Bad Request (missing or invalid data)
- **500:** Internal Server Error (database connection issues, etc.)

Error response format:
```json
{
  "success": false,
  "error": "Error description"
}
```

## Troubleshooting

### Local Development

1. **"Database connection error"**
   - Ensure MySQL server is running
   - Check database credentials in `DB_CONFIG`
   - Verify MySQL user has necessary privileges

2. **"Address already in use"**
   - The app uses port 5000 by default to avoid conflicts
   - If port 5000 is occupied, modify the port in the last line of `app.py`

3. **"SQL file not found"**
   - Ensure `database_structure.sql` is in the same directory as `app.py`

4. **Permission denied**
   - Ensure MySQL user has CREATE DATABASE and INSERT privileges

### Docker

1. **"Port already allocated"**
   - Stop other containers using port 5000:
   ```bash
   docker stop student-grades-api
   docker ps -q | xargs docker stop
   ```

2. **"Database connection failed"**
   - Ensure MySQL server is running on localhost:3306
   - Check database credentials in app.py
   - View container logs for more details:
   ```bash
   docker logs student-grades-api
   ```

3. **"Build failed"**
   - Ensure Docker is running and you have sufficient disk space
   - Check that requirements.txt exists and is valid
   - Try rebuilding:
   ```bash
   docker build -t student-grades-api .
   ```

4. **Container fails to start**
   - Check container logs:
   ```bash
   docker logs student-grades-api
   ```
   - Ensure all files are present and correct

## Development

The application is designed for easy extension:
- Add new endpoints by defining new Flask routes
- Modify database structure by updating `database_structure.sql`
- Add validation and business logic in the route functions

## License

This project is for educational purposes.
