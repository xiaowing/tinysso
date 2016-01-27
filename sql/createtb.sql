-- This SQL script is written for PostgreSQL.
-- @author: xiaowing
-- @license:   Apache Lincese 2.0 

DROP TABLE IF EXISTS m_sch.m_user_auth;
DROP SCHEMA IF EXISTS m_sch;

DROP ROLE IF EXISTS tinysso;
CREATE USER tinysso NOSUPERUSER NOCREATEDB NOCREATEROLE ENCRYPTED PASSWORD 'asdf1234';

CREATE SCHEMA m_sch AUTHORIZATION tinysso;
CREATE TABLE m_sch.m_user_auth(
    user_serial serial NOT NULL,
    user_id character varying(20) NOT NULL,
    user_password character varying(20) NOT NULL,
    user_mail text NOT NULL,
    signup_time  timestamp(3) DEFAULT now(),
    user_actived boolean NOT NULL DEFAULT false,
    PRIMARY KEY (user_serial),
    CONSTRAINT m_user_auth_ukey UNIQUE (user_id),
    CONSTRAINT m_user_auth_mail_ukey UNIQUE (user_mail)
);
ALTER TABLE m_sch.m_user_auth OWNER TO tinysso;

INSERT INTO m_sch.m_user_auth (user_id, user_password, user_mail, user_actived) VALUES ('xiaowing', 'asdf1234', 'xiaowing@xyz.com', TRUE);

