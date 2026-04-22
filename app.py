from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import mysql.connector
from mysql.connector import Error
import os
import sys

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database configuration
# Support both Docker environment variables and local development
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'Unitec123')
}
DB_NAME = os.getenv('DB_NAME', 'student_grades')

def get_db_connection():
    """Get connection to the student_grades database"""
    try:
        config = DB_CONFIG.copy()
        config['database'] = DB_NAME
        connection = mysql.connector.connect(**config)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None

def get_base_connection():
    """Get connection to MySQL server without specifying database"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL server: {e}")
        return None

def database_exists():
    """Check if the database exists"""
    try:
        connection = get_base_connection()
        if not connection:
            return False
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES LIKE %s", (DB_NAME,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        print(f"Database check: '{DB_NAME}' {'exists' if result else 'does not exist'}")
        return result is not None
    except Error as e:
        print(f"Error checking database existence: {e}")
        print("Make sure MySQL server is running and credentials are correct")
        return False

def create_database():
    """Create the database if it doesn't exist"""
    try:
        connection = get_base_connection()
        if not connection:
            return False
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE {DB_NAME}")
        cursor.close()
        connection.close()
        print(f"Database '{DB_NAME}' created successfully")
        return True
    except Error as e:
        print(f"Error creating database: {e}")
        print("Check if you have CREATE DATABASE privileges")
        return False

def execute_sql_file():
    """Execute the database_structure.sql file to set up tables and initial data"""
    try:
        print(f"Looking for SQL file in: {os.path.abspath('database_structure.sql')}")
        if not os.path.exists('database_structure.sql'):
            print("Error: database_structure.sql file not found")
            return False
            
        connection = get_db_connection()
        if not connection:
            print("Error: Could not connect to database for SQL execution")
            return False
        
        cursor = connection.cursor()
        
        # Read and execute the SQL file
        with open('database_structure.sql', 'r') as file:
            sql_script = file.read()
        
        print(f"SQL file loaded, executing statements...")
        
        # Remove comments and clean up the script
        lines = sql_script.split('\n')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('--'):
                cleaned_lines.append(line)
        
        # Join lines and split into statements
        cleaned_script = '\n'.join(cleaned_lines)
        statements = [stmt.strip() for stmt in cleaned_script.split(';') if stmt.strip()]
        
        print(f"Found {len(statements)} statements to execute")
        
        executed_count = 0
        error_count = 0
        
        for i, statement in enumerate(statements, 1):
            try:
                cursor.execute(statement)
                connection.commit()
                executed_count += 1
                print(f"✓ {i}: {statement[:50]}...")
            except Error as e:
                error_count += 1
                print(f"✗ {i}: {statement[:50]}... - {e}")
                # Continue with other statements
        
        cursor.close()
        connection.close()
        print(f"SQL execution completed: {executed_count} successful, {error_count} errors")
        
        if executed_count > 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error executing SQL file: {e}")
        return False

def initialize_database():
    """Initialize the database if it doesn't exist"""
    if not database_exists():
        print(f"Database '{DB_NAME}' does not exist. Creating...")
        if create_database():
            print("Database created. Setting up structure and initial data...")
            if execute_sql_file():
                print("Database initialization completed successfully")
                return True
            else:
                print("Failed to set up database structure")
                return False
        else:
            print("Failed to create database")
            return False
    else:
        print(f"Database '{DB_NAME}' already exists")
        return True

@app.route('/')
def index():
    return jsonify({
        'message': 'Student Grades API',
        'database_status': 'connected' if database_exists() else 'not_initialized',
        'database_name': DB_NAME,
        'endpoints': {
            'students': '/students',
            'courses': '/courses',
            'grades': '/grades',
            'add_student': '/add_student',
            'add_course': '/add_course',
            'add_grade': '/add_grade',
            'add_grade_options': '/add_grade_options'
        }
    })

@app.route('/students')
def students():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students ORDER BY last_name, first_name")
        students = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({
            'success': True,
            'data': students,
            'count': len(students)
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Database connection error',
            'data': []
        }), 500

@app.route('/courses')
def courses():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM courses ORDER BY course_code")
        courses = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({
            'success': True,
            'data': courses,
            'count': len(courses)
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Database connection error',
            'data': []
        }), 500

@app.route('/grades')
def grades():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT g.grade_id, s.first_name, s.last_name, c.course_code, c.course_name, 
               g.grade, g.semester, g.year
        FROM grades g
        JOIN students s ON g.student_id = s.student_id
        JOIN courses c ON g.course_id = c.course_id
        ORDER BY s.last_name, s.first_name, c.course_code
        """
        cursor.execute(query)
        grades = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({
            'success': True,
            'data': grades,
            'count': len(grades)
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Database connection error',
            'data': []
        }), 500

@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.get_json()
    if not data:
        return jsonify({
            'success': False,
            'error': 'No JSON data provided'
        }), 400
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            INSERT INTO students (first_name, last_name, email, enrollment_date)
            VALUES (%s, %s, %s, %s)
            """, (data.get('first_name'), data.get('last_name'), 
                  data.get('email'), data.get('enrollment_date')))
            conn.commit()
            return jsonify({
                'success': True,
                'message': 'Student added successfully!'
            })
        except Error as e:
            return jsonify({
                'success': False,
                'error': f'Error adding student: {e}'
            }), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({
            'success': False,
            'error': 'Database connection error'
        }), 500

@app.route('/add_course', methods=['POST'])
def add_course():
    data = request.get_json()
    if not data:
        return jsonify({
            'success': False,
            'error': 'No JSON data provided'
        }), 400
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            INSERT INTO courses (course_code, course_name, credits)
            VALUES (%s, %s, %s)
            """, (data.get('course_code'), data.get('course_name'), 
                  int(data.get('credits'))))
            conn.commit()
            return jsonify({
                'success': True,
                'message': 'Course added successfully!'
            })
        except Error as e:
            return jsonify({
                'success': False,
                'error': f'Error adding course: {e}'
            }), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({
            'success': False,
            'error': 'Database connection error'
        }), 500

@app.route('/add_grade', methods=['POST'])
def add_grade():
    data = request.get_json()
    if not data:
        return jsonify({
            'success': False,
            'error': 'No JSON data provided'
        }), 400
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
            INSERT INTO grades (student_id, course_id, grade, semester, year)
            VALUES (%s, %s, %s, %s, %s)
            """, (int(data.get('student_id')), int(data.get('course_id')),
                  float(data.get('grade')), data.get('semester'),
                  int(data.get('year'))))
            conn.commit()
            return jsonify({
                'success': True,
                'message': 'Grade added successfully!'
            })
        except Error as e:
            return jsonify({
                'success': False,
                'error': f'Error adding grade: {e}'
            }), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({
            'success': False,
            'error': 'Database connection error'
        }), 500

@app.route('/add_grade_options', methods=['GET'])
def add_grade_options():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT student_id, first_name, last_name FROM students ORDER BY last_name, first_name")
            students = cursor.fetchall()
            cursor.execute("SELECT course_id, course_code, course_name FROM courses ORDER BY course_code")
            courses = cursor.fetchall()
            return jsonify({
                'success': True,
                'students': students,
                'courses': courses
            })
        except Error as e:
            return jsonify({
                'success': False,
                'error': f'Error fetching options: {e}'
            }), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({
            'success': False,
            'error': 'Database connection error'
        }), 500

if __name__ == '__main__':
    # Initialize database on startup
    print("Initializing database...")
    if initialize_database():
        print("Database is ready. Starting Flask application...")
    else:
        print("Warning: Database initialization failed. Some features may not work properly.")
    
    app.run(debug=True, port=5000)
