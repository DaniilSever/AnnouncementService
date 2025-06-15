CREATE DATABASE acc WITH OWNER postgres ENCODING 'UTF8';

-- ------------------------

\connect acc;

CREATE USER acc WITH ENCRYPTED PASSWORD 'acc_pwd';

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ------------------------

DROP TYPE IF EXISTS "Account" CASCADE;
CREATE TABLE "Account"
(
    id              uuid            PRIMARY KEY DEFAULT uuid_generate_v4(),
    email           VARCHAR(255)    NOT NULL UNIQUE,
    pwd_hash        VARCHAR(255)    NOT NULL,
    salt            VARCHAR         NOT NULL,
    role            VARCHAR         NOT NULL,
    count_ads       INTEGER         NOT NULL DEFAULT 0,
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
COMMENT ON COLUMN "Account".email is 'Email аккаунта';
COMMENT ON COLUMN "Account".pwd_hash is 'SHA-256-хеш пароля';
COMMENT ON COLUMN "Account".salt is 'Соль для хеша';
COMMENT ON COLUMN "Account".role is 'Роль аккаунта';
COMMENT ON COLUMN "Account".count_ads is 'Количество созданных объявлений';
COMMENT ON COLUMN "Account".is_banned is 'Забанен ли аккаунт';
COMMENT ON COLUMN "Account".created_at is 'Дата создания аккаута';
COMMENT ON COLUMN "Account".updated_at is 'Дата обновления аккаунта';
COMMENT ON COLUMN "Account".blocked_at is 'Дата блокировки аккаунта';
COMMENT ON COLUMN "Account".blocked_till is 'Дата снятие блокировки';

-- ------------------------

--SEED ADMIN
-- Данные для входа: email | password:
-- admin@ad.com | admin

INSERT INTO "Account"(
    id
    , email
    , pwd_hash
    , salt
    , role
    , count_ads
    , is_banned
    , created_at
    , updated_at
    , blocked_at
    , blocked_till
)
VALUES(
    '3a77e9c9-2861-4fbb-9fd9-522517f13021'
    , 'admin@ad.com'
    , 'e1ee98334d5bfd0810fa6c03beef3cc3d05486a56c9d32e9b528d9af4477e3fa'
    , 'a9330649b51c9ed1d905fddeabd606f7'
    , 'admin'
    , 0
    , FALSE
    , CURRENT_TIMESTAMP
    , NULL
    , NULL
    , NULL
);


GRANT ALL PRIVILEGES ON DATABASE acc TO acc;
GRANT ALL ON SCHEMA public TO acc;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO acc;
GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA public TO acc;