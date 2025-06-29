CREATE DATABASE auth WITH OWNER postgres ENCODING 'UTF8';

-- ------------------------

\connect auth;

CREATE USER auth WITH ENCRYPTED PASSWORD 'auth_pwd';

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ------------------------

DROP TABLE IF EXISTS "SignupAccount" CASCADE;
CREATE TABLE "SignupAccount"
(
    id                  uuid            PRIMARY KEY DEFAULT uuid_generate_v4(),
    email               VARCHAR(255)    NOT NULL UNIQUE,
    pwd_hash            VARCHAR(255)    NOT NULL,
    salt                VARCHAR         NOT NULL,
    code                VARCHAR(10)     NOT NULL,
    created_at          TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at          TIMESTAMP       NULL,
    blocked_till        TIMESTAMP       NULL,
    attempts    INT             NOT NULL DEFAULT 1 CHECK (attempts <= 5)
);
--
CREATE INDEX ON "SignupAccount" (id);
--
COMMENT ON TABLE "SignupAccount" is 'Регистрация по емейл';
COMMENT ON COLUMN "SignupAccount".id is 'ID аккаунта в системе';
COMMENT ON COLUMN "SignupAccount".email is 'Email аккаунта';
COMMENT ON COLUMN "SignupAccount".pwd_hash is 'SHA-256-хеш пароля';
COMMENT ON COLUMN "SignupAccount".salt is 'Соль для хеша';
COMMENT ON COLUMN "SignupAccount".code is 'Код подтверждения (короткий)';
COMMENT ON COLUMN "SignupAccount".created_at is 'Создание записи';
COMMENT ON COLUMN "SignupAccount".updated_at is 'Дата последнего обновления';
COMMENT ON COLUMN "SignupAccount".blocked_till is 'Блокировка на сутки';
COMMENT ON COLUMN "SignupAccount".attempts is 'Количество неудачных попыток входа';

-- ------------------------

DROP TABLE IF EXISTS "RefreshToken";
CREATE TABLE "RefreshToken"
(
    id              uuid        PRIMARY KEY DEFAULT uuid_generate_v4(),
    account_id      uuid        NOT NULL,
    token           VARCHAR     NOT NULL,
    is_revoked      BOOLEAN     NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    expires_at      TIMESTAMP   NOT NULL
);
--
CREATE INDEX ON "RefreshToken" (account_id);
CREATE INDEX ON "RefreshToken" (is_revoked);
CREATE INDEX ON "RefreshToken" (expires_at);
--
COMMENT ON TABLE "RefreshToken" is 'Таблица для хранения токенов';
COMMENT ON COLUMN "RefreshToken".account_id is 'ID аккаунта, которому принадлежит токен';
COMMENT ON COLUMN "RefreshToken".token is 'Токен типа "Refresh"';
COMMENT ON COLUMN "RefreshToken".is_revoked is 'Отозван ли токен';
COMMENT ON COLUMN "RefreshToken".created_at is 'Время создания записи';
COMMENT ON COLUMN "RefreshToken".expires_at is 'Время истечения токена';

-- ------------------------

GRANT ALL PRIVILEGES ON DATABASE auth TO auth;
GRANT ALL ON SCHEMA public TO auth;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO auth;
GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA public TO auth;
