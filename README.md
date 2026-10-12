# Student Management System

A beginner-friendly college mini project built with **Python (Flask)** and **PostgreSQL**. This application manages student academic records, departments, and course enrollments using clean relational database principles and parameterized SQL queries.

Developed as an academic portfolio project for demonstrating core database management, SQL queries, and full-stack web development fundamentals.

---

## Project Overview

The **Student Management System** follows a clean **Three-Tier Architecture**:
1. **Presentation Layer:** Vanilla HTML5 and responsive CSS3 templates styled with a calm, muted color palette.
2. **Application / Backend Layer:** Python Flask server handling HTTP requests and routing.
3. **Database Layer:** PostgreSQL relational database with referential integrity, constraints, and relational joins.

---

## Features

- **Dashboard Overview:** Displays live count metrics of total students, academic departments, and available courses, alongside a list of recently enrolled students.
- **Student Directory:** Displays all registered students in a clean table with department badges and enrollment dates.
- **Search Functionality:** Filter student records by first name, last name, or email using case-insensitive PostgreSQL pattern matching (`ILIKE`).
- **Add New Student:** Web form to insert student profiles with client-side and server-side validation.
- **Duplicate Email Protection:** Gracefully catches database `UNIQUE` constraint violations (`psycopg2.IntegrityError`) and displays friendly flash error messages.
- **Edit Student Details:** Pre-populates existing student data into a form for updates.
- **Delete Student with Confirmation:** Delete student records with a native browser prompt to prevent accidental data loss.
- **Available Courses Catalog:** Multi-table query joining `courses`, `departments`, and `enrollments` to calculate active student counts per course.

---

## Technologies Used

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Database** | PostgreSQL 16 | Relational database management system |
| **Database Tool** | pgAdmin 4 | Database administration and executing SQL scripts |
| **Database Driver** | `psycopg2-binary` | PostgreSQL database adapter for Python |
| **Backend** | Python 3 + Flask | Web routing, controller logic, and session handling |
| **Frontend** | HTML5 & CSS3 | Jinja2 templating, responsive custom stylesheet |
| **Environment** | `python-dotenv` | Secure configuration management via `.env` |

---

## Database Design & Schema

The database consists of **4 interrelated tables**:

```text
departments (1) ────< (M) students
     │
     └───< (1) courses (1) ────< (M) enrollments >──── (M) students
```

### Table Details:
1. **`departments`**: Stores department information (`department_id` PK, `department_name` UNIQUE, `department_code` UNIQUE).
2. **`students`**: Stores student profiles (`student_id` PK, `first_name`, `last_name`, `email` UNIQUE, `phone`, `date_of_birth`, `department_id` FK).
3. **`courses`**: Stores course offerings (`course_id` PK, `course_code` UNIQUE, `course_name`, `credits` CHECK > 0, `department_id` FK).
4. **`enrollments`**: **Junction/Bridge table** resolving the Many-to-Many relationship between students and courses (`enrollment_id` PK, `student_id` FK, `course_id` FK, `grade`, with a composite UNIQUE constraint on `(student_id, course_id)`).

---

## Project Directory Structure

```text
student-database-management-system/
├── app.py                     # Main Flask routing and CRUD application logic
├── db.py                      # PostgreSQL connection management helper
├── requirements.txt           # Python dependencies (Flask, psycopg2-binary, python-dotenv)
├── schema.sql                 # SQL script defining tables, keys, and constraints
├── sample_data.sql            # Seed data script for initial records
├── .env                       # Environment variables (DB credentials - gitignored)
├── .env.example               # Sample environment configuration template
├── .gitignore                 # Files excluded from version control
├── README.md                  # Project documentation
├── templates/                 # Jinja2 HTML templates
│   ├── base.html              # Base layout with navbar and flash messages
│   ├── index.html             # Dashboard with summary statistic cards
│   ├── students.html          # Student directory table with search bar
│   ├── add_student.html       # Form to add a new student
│   ├── edit_student.html      # Form to update existing student record
│   └── courses.html           # Catalog of available courses
└── static/
    └── css/
        └── style.css          # Muted, accessible CSS styling
```

---

## Setup & Installation Guide (Windows / Localhost)

### 1. Prerequisites
- Python 3.10+ installed on your computer.
- PostgreSQL 14+ and pgAdmin 4 installed and running.

---

### 2. Database Setup
1. Open **pgAdmin 4** and connect to your PostgreSQL server.
2. Create a new database named **`student_db`**.
3. Open the **Query Tool** on `student_db`:
   - Open and run [`schema.sql`](schema.sql) (Press `F5`).
   - Open and run [`sample_data.sql`](sample_data.sql) (Press `F5`).
4. Run `SELECT * FROM students;` to verify that initial records appear.

---

### 3. Clone / Open the Project
Open a terminal (PowerShell or Command Prompt) and run:
```powershell
git clone https://github.com/sanskruti2409/student-database-management-system.git
cd student-database-management-system
```

---

### 4. Configure Environment Variables
Create a file named `.env` in the root folder with your database credentials (or copy from `.env.example`):
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=student_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
```

---

### 5. Install Dependencies
Install the required Python libraries using pip:
```powershell
python -m pip install -r requirements.txt
```

---

### 6. Run the Application
Start the Flask development server:
```powershell
python app.py
```

Open your browser and visit:
**`http://127.0.0.1:5000`**

---

## Application Pages & Interface

| Page | URL Route | Description |
| :--- | :--- | :--- |
| **Dashboard** | `/` | Displays live counts (students, departments, courses) and recent registrations. |
| **Student Directory** | `/students` | Tabular view of all students with department tags, search filter, and action buttons. |
| **Add Student** | `/add-student` | Form with field validation to register a new student profile. |
| **Edit Student** | `/edit-student/<id>` | Form pre-populated with existing student data for updating details. |
| **Delete Student** | `/delete-student/<id>` | Deletes a student record with browser confirmation to prevent accidental loss. |
| **Course Catalog** | `/courses` | Displays courses, credit hours, departments, and active enrollment totals. |

---

## Security & Best Practices Implemented

- **Parameterized SQL Queries:** All database interactions utilize `%s` placeholders via `psycopg2`, preventing SQL injection vulnerabilities.
- **Environment Isolation:** Database credentials are kept in a separate `.env` file and excluded from Git commits via `.gitignore`.
- **Referential Integrity:** Enforced at the database engine level with foreign keys and cascade rules.
- **Safe Transaction Management:** Database modifications use explicit `commit()` and `rollback()` handlers within `try...finally` resource cleanup blocks.

---

## Academic Profile
- **Author:** BCA Graduate & M.Sc. Computer Applications Student
- **Project Purpose:** Academic Mini Project & Entry-Level Technical Interview Portfolio
