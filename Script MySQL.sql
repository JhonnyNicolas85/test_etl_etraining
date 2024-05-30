/*CREATE SCHEMA test;*/
USE test;
/*Creación de tabla Gender*/
CREATE TABLE gender (
	id_gender INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(45) NOT NULL
);

/*Creación de tabla type_contagion*/
CREATE TABLE type_contagion (
	id_type_contagion INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(45) NOT NULL
);

/*Creación de tabla status*/
CREATE TABLE `status`(
	id_status INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(45) NOT NULL
);

/*Creación de tabla department SIN auto increment*/
CREATE TABLE department (
	id_department INT PRIMARY KEY,
    name VARCHAR(45) NOT NULL
);

/*Creación de tabla municipality SIN auto increment*/
CREATE TABLE municipality (
    id_municipality INT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    id_department INT NOT NULL,
    FOREIGN KEY (id_department) REFERENCES department(id_department)
);


/* Creación de tabla cases */
CREATE TABLE cases (
    id_case INT PRIMARY KEY,
    id_municipality INT NOT NULL,
    age INT NOT NULL,
    id_gender INT NOT NULL,
    id_type_contagion INT NOT NULL,
    id_status INT NOT NULL,
    date_symptom DATETIME,
    date_death DATETIME,
    date_diagnosis DATETIME,
    date_recovery DATETIME,
    FOREIGN KEY (id_municipality) REFERENCES municipality(id_municipality),
    FOREIGN KEY (id_gender) REFERENCES gender(id_gender),
    FOREIGN KEY (id_type_contagion) REFERENCES type_contagion(id_type_contagion),
    FOREIGN KEY (id_status) REFERENCES `status`(id_status)
);


SELECT * FROM municipality;