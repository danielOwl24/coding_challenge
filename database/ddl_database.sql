CREATE DATABASE migration_db;

CREATE TABLE IF NOT EXISTS departments (
    id SERIAL PRIMARY KEY,      
    department VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,      
    job VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS hired_employees (
    id SERIAL PRIMARY KEY,  
    name VARCHAR(255) NOT NULL,  
    datetime TIMESTAMP NOT NULL,  
    department_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL, 
    CONSTRAINT fk_department FOREIGN KEY (department_id) REFERENCES departments(id),
    CONSTRAINT fk_job FOREIGN KEY (job_id) REFERENCES jobs(id)
);