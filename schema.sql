-- ====================================================================
-- Project: Student Database Management System
-- File: schema.sql
-- Description: Defines database tables, constraints, and relationships
-- ====================================================================

-- Drop tables if they already exist (in reverse dependency order)
-- We drop enrollments first because it references students and courses
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS departments;

-- --------------------------------------------------------------------
-- 1. DEPARTMENTS TABLE
-- Stores academic departments (e.g., Computer Applications, IT)
-- --------------------------------------------------------------------
CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE,
    department_code VARCHAR(10) NOT NULL UNIQUE
);

-- --------------------------------------------------------------------
-- 2. STUDENTS TABLE
-- Stores individual student demographic and academic records
-- --------------------------------------------------------------------
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(15),
    date_of_birth DATE,
    department_id INT REFERENCES departments(department_id) ON DELETE SET NULL,
    enrollment_date DATE NOT NULL DEFAULT CURRENT_DATE
);

-- --------------------------------------------------------------------
-- 3. COURSES TABLE
-- Stores courses offered by various departments
-- --------------------------------------------------------------------
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_code VARCHAR(20) NOT NULL UNIQUE,
    course_name VARCHAR(100) NOT NULL,
    credits INT NOT NULL CHECK (credits > 0),
    department_id INT NOT NULL REFERENCES departments(department_id) ON DELETE CASCADE
);

-- --------------------------------------------------------------------
-- 4. ENROLLMENTS TABLE (Junction / Bridge Table)
-- Resolves the Many-to-Many relationship between Students and Courses
-- A student can take multiple courses, and a course has multiple students.
-- --------------------------------------------------------------------
CREATE TABLE enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    course_id INT NOT NULL REFERENCES courses(course_id) ON DELETE CASCADE,
    enrollment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    grade VARCHAR(2),
    -- Ensure a student cannot be enrolled in the same course more than once
    CONSTRAINT unique_student_course UNIQUE (student_id, course_id)
);
