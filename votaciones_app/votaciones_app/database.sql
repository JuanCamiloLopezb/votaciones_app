CREATE DATABASE votaciones_db;
USE votaciones_db;

CREATE TABLE ciudadanos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    documento VARCHAR(15) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    ciudad VARCHAR(100),
    telefono VARCHAR(20)
);

CREATE TABLE puestos_votacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    documento VARCHAR(15),
    lugar_votacion VARCHAR(150),
    direccion VARCHAR(150),
    mesa VARCHAR(10),
    zona VARCHAR(50),
    FOREIGN KEY (documento) REFERENCES ciudadanos(documento)
);