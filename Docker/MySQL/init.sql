DROP DATABASE IF EXISTS chatapp;
DROP USER IF EXISTS 'testuser'@'%';

CREATE USER 'testuser'@'%' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser'@'%';

CREATE TABLE users (
    id VARCHAR(255) UNIQUE NOT NULL PRIMARY KEY,
    user_name VARCHAR(50) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE channels (
    id VARCHAR(255) UNIQUE NOT NULL PRIMARY KEY,
    channel_name VARCHAR(255),
    event_date DATETIME,
    url TEXT,
    image_place VARCHAR(255),
    uid VARCHAR(255),
    FOREIGN KEY (uid) REFERENCES users(id) ON DELETE CASCADE
);


CREATE TABLE channelmembers (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    uid VARCHAR(255),
    cid VARCHAR(255),
    FOREIGN KEY (uid) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (cid) REFERENCES channels(id) ON UPDATE CASCADE ON DELETE CASCADE,
    starred BOOLEAN 
);


CREATE TABLE messages(
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    message TEXT NOT NULL,
    posted_at DATETIME NOT NULL,
    uid VARCHAR(255),
    cid VARCHAR(255),
    FOREIGN KEY (uid)
     REFERENCES users(id)
     ON DELETE CASCADE,
    FOREIGN KEY (cid)
     REFERENCES channels(id)
     ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE albums(
    id INT AUTO_INCREMENT PRIMARY KEY,
    album_place VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL,
    album_title VARCHAR(255),
    album_discription TEXT,
    uid VARCHAR(255),
    cid VARCHAR(255),
    FOREIGN KEY (uid) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (cid) REFERENCES channels(id) ON UPDATE CASCADE ON DELETE CASCADE
);

INSERT INTO users(id,user_name,email,password) VALUES ('8bf2c5c2-e8bd-424c-abb9-a14aa43fcb3b','test1','test1@mail.com','password1');
INSERT INTO channels(id,channel_name,event_date,url,uid) VALUES ('9af15cce-7cfb-4ad6-a2ea-5638405d3516','BTSツアー2024','2024-12-15 12:00:00','https://bts-official.jp/news/detail.php?nid=ekt721nWwJ0=','8bf2c5c2-e8bd-424c-abb9-a14aa43fcb3b');
INSERT INTO users(id,user_name,email,password) VALUES ('13f2836a-443b-45cd-a257-ea9e958d5b2d','test2','test2@mail.com','password2');
INSERT INTO channelmembers(uid,cid) VALUES ('8bf2c5c2-e8bd-424c-abb9-a14aa43fcb3b','9af15cce-7cfb-4ad6-a2ea-5638405d3516');
INSERT INTO messages(message,posted_at,uid,cid) VALUES ('こんにちは、世界','2024-04-15 19:00:00','8bf2c5c2-e8bd-424c-abb9-a14aa43fcb3b','9af15cce-7cfb-4ad6-a2ea-5638405d3516');