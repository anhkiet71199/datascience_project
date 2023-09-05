-- Database: Student

-- DROP DATABASE IF EXISTS "Student";

CREATE DATABASE "Student"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

--Excercise 1 Create table and insert data
CREATE TABLE students (
	student_id serial PRIMARY KEY, 
	first_name VARCHAR(100),
	last_name VARCHAR(100),
	age INT,
	major VARCHAR(100)
);

INSERT INTO students (first_name, last_name, age, major) 
VALUES 
    ('John', 'Doe', 22, 'Computer Science'),
    ('Jane', 'Smith', 20, 'Mathematics'),
    ('Alice', 'Johnson', 25, 'Physics'),
    ('Bob', 'Brown', 19, 'Chemistry'),
    ('Eva', 'Williams', 21, 'Biology');


--Excercise 2 Query 
/* Get all students */
SELECT * from students;

/* Get students with age greater than 20 */
select * from students where age > 20;

/* Get students with major is 'Computer Science'*/
select * from students where major = 'Computer Science';

--Excercise 3 Update and Delete
/* Update age with student_id = 3 to 25 */
UPDATE students
SET age = 25
WHERE student_id = 3;

/* Delete student with student_id = 4 */
DELETE FROM students
WHERE student_id = 4;

--Excercise 4 create table and query combine
/* Create table 'courses' with course_id is primary key and course_name */
CREATE TABLE courses(
	course_id serial primary KEY,
	course_name varchar(100)
);
INSERT INTO courses(course_name)
VALUES
    ('Introduction to Programming'),
    ('Biology 101'),
    ('Physics for Engineers');

/* Create table 'student_courses' with student_id is foreign key and course_id is foreign key */
CREATE TABLE student_courses(
	student_id int,
	course_id int,
	foreign key (student_id) references students(student_id),
	foreign key (course_id) references courses(course_id)
);

/* Insert at least 3 records to table courses and 5 records to student_courses */
INSERT INTO student_courses (student_id, course_id)
VALUES
    (1, 1),  
    (2, 2),  
    (3, 3),  
    (1, 2);  
	
/* Write query to get all students and courses with student register */
SELECT students.first_name, students.last_name, courses.course_name
FROM students
LEFT JOIN student_courses ON students.student_id = student_courses.student_id
LEFT JOIN courses ON student_courses.course_id = courses.course_id;
