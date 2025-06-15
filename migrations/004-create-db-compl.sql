CREATE DATABASE compl WITH OWNER postgres ENCODING 'UTF8';

-- ------------------------

\connect compl;

CREATE USER compl WITH ENCRYPTED PASSWORD 'compl_pwd';

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ------------------------

DROP TABLE IF EXISTS "Complaints";
CREATE TABLE "Complaints"
(
    id  uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    compl_on_id uuid NOT NULL,
    services VARCHAR NOT NULL,
    author_id uuid NOT NULL,
    complaints VARCHAR NOT NULL,
    is_notified BOOLEAN NOT NULL,
    is_resolved BOOLEAN NOT NULL,
    created_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
);
--
CREATE INDEX ON "Complaints" (compl_on_id);
CREATE INDEX ON "Complaints" (services);
CREATE INDEX ON "Complaints" (author_id);
--
COMMENT ON TABLE "Complaints" is 'Таблица жалоб на пользователей';
COMMENT ON COLUMN "Complaints".id is 'ID жалобы в системе';
COMMENT ON COLUMN "Complaints".compl_on_id is 'Жалоба на ID (Ads | Account)';
COMMENT ON COLUMN "Complaints".services is 'Сервис из которого жалоба (Ads | Account)';
COMMENT ON COLUMN "Complaints".author_id is 'ID автора жалобы';
COMMENT ON COLUMN "Complaints".complaints is 'Жалоба';
COMMENT ON COLUMN "Complaints".is_notified is 'Уведомлен ли автор';
COMMENT ON COLUMN "Complaints".is_resolved is 'Решена ли жалоба';
COMMENT ON COLUMN "Complaints".created_at is 'Дата создания';

-- ------------------------

GRANT ALL PRIVILEGES ON DATABASE compl TO compl;
GRANT ALL ON SCHEMA public TO compl;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO compl;
GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA public TO compl;