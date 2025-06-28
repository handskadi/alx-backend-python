CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  name VARCHAR(255),
  age INTEGER,
  email VARCHAR(255),
  phone_number VARCHAR(20)
);


insert into users(name, age, phone_number, email) VALUES
('John', 21, '099999395', 'test@gmail.com');