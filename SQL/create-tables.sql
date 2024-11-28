-- SQL Commands to build tables in my schema

-- Create users table
CREATE TABLE users (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(20) NOT NULL UNIQUE,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL,
    address VARCHAR(255)
);

-- Create albums table
CREATE TABLE albums (
    album_id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    format_type VARCHAR(20) NOT NULL,
    release_date DATE NOT NULL,
    genre VARCHAR(20) NOT NULL,
    artist_name VARCHAR(255) NOT NULL,
    description VARCHAR(MAX),
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Create tracks table
CREATE TABLE tracks (
    track_id INT IDENTITY(1,1) PRIMARY KEY,
    track_title VARCHAR(150) NOT NULL,
    duration TIME NOT NULL
);

-- Create pivot table between albums and tracks
CREATE TABLE album_tracks (
    album_id INT NOT NULL,
    track_id INT NOT NULL,
    PRIMARY KEY (album_id, track_id),
    FOREIGN KEY (album_id) REFERENCES albums(album_id) ON DELETE CASCADE,
    FOREIGN KEY (track_id) REFERENCES tracks(track_id) ON DELETE CASCADE
);