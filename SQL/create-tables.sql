-- SQL Commands to build tables in my schema

-- Create users table
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO INCREMENT,
    username VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL,
    address VARCHAR(255) NULL
);

-- Create albums table
CREATE TABLE albums (
    album_id INT PRIMARY KEY AUTO INCREMENT,
    name VARCHAR(50) NOT NULL,
    format_type VARCHAR(20) NOT NULL,
    release_date DATE NOT NULL,
    genre VARCHAR(20) NOT NULL,
    artist_name VARCHAR(255) NOT NULL,
    description TEXT NULL,
    user_id int FOREIGN KEY NOT NULL
);

-- Create tracks table
CREATE TABLE tracks (
    track_id INT PRIMARY KEY AUTO INCREMENT,
    track_title VARCHAR(50) NOT NULL,
    duration TIME NOT NULL
);

-- Create pivot table between albums and tracks
-- TODO: Need to revise this table definition
CREATE TABLE album_tracks (
    album_id INT FOREIGN KEY,
    track_id INT FOREIGN KEY
);