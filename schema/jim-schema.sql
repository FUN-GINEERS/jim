-- Intended for use with PostgreSQL
-- Modifications will be needed to use with sqlite3

-- Custom command table
--
CREATE TABLE commands (
    server_id VARCHAR(255) NOT NULL,
    command VARCHAR(255) NOT NULL,
    response TEXT DEFAULT ''
);

-- User command permissions table
--
CREATE TABLE perms (
    server_id VARCHAR(255) NOT NULL,
    perm_type INTEGER DEFAULT 0 NOT NULL,
    role_id VARCHAR(255) NOT NULL,
    is_user BOOLEAN DEFAULT FALSE NOT NULL
);

-- Ser
--
CREATE TABLE servers (
    id VARCHAR(255) NOT NULL,
    prefix CHAR(1) DEFAULT '&' NOT NULL
);


