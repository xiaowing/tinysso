-- This SQL script is written for PostgreSQL.
-- @author: xiaowing
-- @license:   Apache Lincese 2.0 

DROP TABLE IF EXISTS m_sch.m_user_auth;
DROP SCHEMA IF EXISTS m_sch;

CREATE SCHEMA m_sch AUTHORIZATION postgres;
CREATE TABLE m_sch.m_user_auth
(
    user_id character varying(20) NOT NULL,
    user_password character varying(20) NOT NULL,
    user_mail text NOT NULL,
    user_actived boolean NOT NULL DEFAULT false,
    CONSTRAINT m_user_auth_pkey PRIMARY KEY (user_id),
    CONSTRAINT m_user_auth_ukey UNIQUE (user_mail)
)
WITH (
    OIDS=FALSE
);
ALTER TABLE m_sch.m_user_auth OWNER TO postgres;

INSERT INTO m_sch.m_user_auth VALUES ('xiaowing', 'asdf1234', 'xiaowing@xyz.com');