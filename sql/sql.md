Создание таблицы Regions

CREATE TABLE Regions (
  id serial PRIMARY KEY,
  Name varchar
);

Создание таблицы Locations

CREATE TABLE Locations (
  id serial PRIMARY KEY,
  Address varchar,
  Region_id integer REFERENCES Regions(id)
);

Создание Departments

CREATE TABLE Departments (
  id serial PRIMARY KEY,
  Name varchar,
  Location_id integer REFERENCES Locations(id)
);

Создание Employees

CREATE TABLE Employees (
  id serial PRIMARY KEY,
  Name varchar,
  Last_name varchar,
  Hire_date date,
  Salary integer,
  Email varchar,
  Manager_id integer REFERENCES Employees(id),
  Department_id integer REFERENCES Departments(id)
);

Добавляем столб в Departments

ALTER TABLE Departments
ADD Manager_id integer REFERENCES Employees(id);

Выборки:

Показать работников у которых нет почты или почта не в корпоративном домене (домен dualbootpartners.com)

SELECT name, last_name
FROM employees
WHERE Email IS NULL OR Email NOT LIKE '%@dualbootpartners.com';

Получить список работников нанятых в последние 30 дней

SELECT name, last_name
FROM employees
WHERE Hire_date >= CURRENT_DATE - INTERVAL '30' DAY;

Найти максимальную и минимальную зарплату по каждому департаменту

SELECT Department_id, MAX(Salary) AS MaxSalary, MIN(Salary) AS MinSalary
FROM Employees
GROUP BY Department_id;

Посчитать количество работников в каждом регионе

SELECT r.Name, COUNT(e.id)
FROM Regions r
JOIN Locations L ON r.id = L.Region_id
JOIN Departments d ON L.id = d.Location_id
JOIN Employees e ON d.id = e.Department_id
GROUP BY r.Name;

Показать сотрудников у которых фамилия длиннее 10 символов

SELECT name, last_name
FROM employees
WHERE LENGTH(Last_name) > 10;

Показать сотрудников с зарплатой выше средней по всей компании

SELECT name, last_name
FROM employees
WHERE Salary > (SELECT AVG(Salary) FROM Employees);

;
