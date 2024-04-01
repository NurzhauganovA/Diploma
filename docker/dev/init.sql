CREATE USER smartschooladmin WITH PASSWORD '@WSX3edc';
CREATE DATABASE smartschool;
GRANT ALL PRIVILEGES ON DATABASE smartschool TO smartschooladmin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO smartschooladmin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO smartschooladmin;
ALTER DATABASE smartschool OWNER TO smartschooladmin;