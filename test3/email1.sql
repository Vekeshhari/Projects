CREATE DATABASE IF NOT EXISTS email_spoof1;
USE email_spoof1;
show databases;

CREATE TABLE trusted (
  id INT AUTO_INCREMENT PRIMARY KEY,
  email_id VARCHAR(255) NOT NULL UNIQUE
);
CREATE TABLE untrusted (
  id INT AUTO_INCREMENT PRIMARY KEY,
  email_id VARCHAR(255) NOT NULL,
  suspicious_term VARCHAR(255)
);
CREATE TABLE email_hash (
  id INT AUTO_INCREMENT PRIMARY KEY,
  email_id VARCHAR(255) NOT NULL,
  email_hash VARCHAR(255),
  time_received DATETIME
);
CREATE TABLE not_spoofed (
  id INT AUTO_INCREMENT PRIMARY KEY,
  email_id VARCHAR(255) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS link_files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email_id VARCHAR(255),
    url TEXT, 
    time_received DATETIME
);
ALTER TABLE trusted ADD COLUMN time_received DATETIME DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE untrusted ADD COLUMN time_received DATETIME DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE not_spoofed ADD COLUMN time_received DATETIME DEFAULT CURRENT_TIMESTAMP;



-- Step 1: Delete data from all tables
SET SQL_SAFE_UPDATES = 0;
DELETE FROM trusted;
DELETE FROM untrusted;
DELETE FROM not_spoofed;
DELETE FROM email_hash;
DELETE FROM link_files;
ALTER TABLE trusted AUTO_INCREMENT = 1;
ALTER TABLE untrusted AUTO_INCREMENT = 1;
ALTER TABLE not_spoofed AUTO_INCREMENT = 1;
ALTER TABLE email_hash AUTO_INCREMENT = 1;
ALTER TABLE link_files AUTO_INCREMENT = 1;
SET SQL_SAFE_UPDATES = 1;




-- drop table link_files;
show tables;
select * from trusted;
select * from untrusted;
select * from not_spoofed;
select * from link_files;
select * from email_hash;
delete from untrusted where id between 1 and 19 ;