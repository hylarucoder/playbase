CREATE USER playbase WITH PASSWORD 'playbase123' CREATEDB;
CREATE DATABASE playbase
    WITH
    OWNER = playbase
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
