DROP TABLE IF EXISTS water_supply;

CREATE TABLE Role(
    role_id INT,
    role_name VARCHAR(10),
    role_description VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY(role_id)
)

CREATE TABLE UserLogin(
    employee_id VARCHAR(10) NOT NULL,
    first_name VARCHAR(10) NOT NULL,
    last_name VARCHAR(10) NOT NULL,
    password VARCHAR(10) NOT NULL,
    date_of_birth DATE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    image_profile VARCHAR(255) DEFAULT=NULL,
    role_id INT,
    FOREIGN KEY(role_id) REFERENCES Role(role_id)
    PRIMARY KEY(employee_id),
)
