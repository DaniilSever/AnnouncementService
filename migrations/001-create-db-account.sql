CREATE DATABASE acc WITH OWNER postgres ENCODING 'UTF8';

-- ------------------------

\connect acc;

CREATE USER acc WITH ENCRYPTED PASSWORD 'acc_pwd';

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ------------------------

DROP TYPE IF EXISTS acc_role CASCADE;
CREATE TYPE acc_role as enum ('base', 'admin');

DROP TYPE IF EXISTS "Account" CASCADE;
CREATE TABLE "Account"
(
    id              uuid            PRIMARY KEY DEFAULT uuid_generate_v4(),
    username        VARCHAR(255)    NOT NULL,
    email           VARCHAR(255)    NOT NULL,
    pwd_hash        VARCHAR(255)    NOT NULL,
    salt            VARCHAR         NOT NULL,
    role            acc_role        NOT NULL,
    is_banned       BOOLEAN         NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at      TIMESTAMP       NULL,
    blocked_at      TIMESTAMP       NULL,
    blocked_till    TIMESTAMP       NULL
);
--
CREATE INDEX ON "Account" (id);
--
COMMENT ON TABLE "Account" is 'Аккаунты (Подтвержденные)';
COMMENT ON COLUMN "Account".id is 'ID аккаунта в системе';
COMMENT ON COLUMN "Account".username is 'Никнейм аккаунта';
COMMENT ON COLUMN "Account".email is 'Email аккаунта';
COMMENT ON COLUMN "Account".pwd_hash is 'SHA-256-хеш пароля';
COMMENT ON COLUMN "Account".salt is 'Соль для хеша';
COMMENT ON COLUMN "Account".is_banned is 'Забанен ли аккаунт';
COMMENT ON COLUMN "Account".created_at is 'Дата создания аккаута';
COMMENT ON COLUMN "Account".updated_at is 'Дата обновления аккаунта';
COMMENT ON COLUMN "Account".blocked_at is 'Дата блокировки аккаунта';
COMMENT ON COLUMN "Account".blocked_till is 'Дата снятие блокировки';

-- ------------------------

GRANT ALL PRIVILEGES ON DATABASE acc TO acc;
GRANT ALL ON SCHEMA public TO acc;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO acc;
GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA public TO acc;