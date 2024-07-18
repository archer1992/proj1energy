CREATE DATABASE powerplants_db;

USE powerplants_db;

CREATE TABLE powerplants (
    facility_name VARCHAR(255),
    resource_category VARCHAR(255),
    technology_type VARCHAR(255),
    installed_capacity FLOAT,
    dependable_capacity FLOAT,
    location TEXT,
    longitude FLOAT,
    latitude FLOAT,
    region VARCHAR(255),
    island VARCHAR(255),
    operator VARCHAR(255),
    owner VARCHAR(255),
    owner_type VARCHAR(255),
);
