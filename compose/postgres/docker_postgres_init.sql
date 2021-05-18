CREATE USER mipha WITH PASSWORD 'mipha123' CREATEDB;
CREATE DATABASE mipha
    WITH
    OWNER = mipha
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
