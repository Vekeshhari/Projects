-- Create the database and switch to it
CREATE DATABASE task_management00;
USE task_management00;

-- Create 'users' table with role field
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') NOT NULL
);

-- Create 'tasks' table with points field
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    deadline DATE,
    points INT DEFAULT 0,
    status ENUM('Pending', 'Completed') DEFAULT 'Pending',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create 'leaderboard' table
CREATE TABLE leaderboard (
    username VARCHAR(50) UNIQUE NOT NULL,
    points INT DEFAULT 0,
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
);

-- Insert users with hashed passwords
INSERT INTO users (username, password, role) VALUES 
('admin', SHA2('adminpass', 256), 'admin'),
('user1', SHA2('password123', 256), 'user'),
('user2', SHA2('mypassword', 256), 'user'),
('user3', SHA2('pass000', 256), 'user'),
('user4', SHA2('mypass111', 256), 'user'),
('user5', SHA2('userfivepass', 256), 'user');  -- New user

-- Insert tasks for users
INSERT INTO tasks (user_id, title, description, deadline, points, status) VALUES 
(2, 'Design a Webpage', 'Create a responsive HTML webpage.', '2024-10-15', 10, 'Pending'), 
(3, 'Write a Report', 'Write a report on task management systems.', '2024-10-20', 15, 'Pending'),
(4, 'Fix Bugs', 'Fix bugs in the existing Python codebase.', '2024-10-12', 20, 'Pending'),
(5, 'Update Documentation', 'Update the project documentation for the current project.', '2024-10-18', 5, 'Pending'),
(6, 'Conduct User Testing', 'Test the application with users and gather feedback.', '2024-10-22', 25, 'Pending');

-- Leaderboard initialization for users
INSERT INTO leaderboard (username, points) VALUES 
('user1', 0),
('user2', 0),
('user3', 0),
('user4', 0),
('user5', 0);  -- New user added to leaderboard

-- Create 'badges' table to define badge thresholds and names
CREATE TABLE badges (
    id INT AUTO_INCREMENT PRIMARY KEY,
    points_threshold INT NOT NULL UNIQUE,
    badge_name VARCHAR(50) NOT NULL
);

-- Create 'user_badges' table to associate users with their badges
CREATE TABLE user_badges (
    user_id INT NOT NULL,
    badge_id INT NOT NULL,
    PRIMARY KEY (user_id, badge_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (badge_id) REFERENCES badges(id) ON DELETE CASCADE
);

-- Insert badge definitions
INSERT INTO badges (points_threshold, badge_name) VALUES 
(50, 'Bronze Badge'),
(100, 'Silver Badge'),
(150, 'Gold Badge'),
(200, 'Platinum Badge'),
(300, 'Diamond Badge'),
(400, 'Emerald Badge'),
(500, 'Sapphire Badge');

select  * from leaderboard;
select * from user_badges ub join badges b on b.id=ub.badge_id;