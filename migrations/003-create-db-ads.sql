CREATE DATABASE ads WITH OWNER postgres ENCODING 'UTF8';

-- ------------------------

\connect ads;

CREATE USER ads WITH ENCRYPTED PASSWORD 'ads_pwd';

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ------------------------

DROP TABLE IF EXISTS "Ads";
CREATE TABLE "Ads"
(
    id                  uuid            PRIMARY KEY DEFAULT uuid_generate_v4(),
    account_id          uuid            NOT NULL, 
    title               VARCHAR(255)    NOT NULL,
    description         VARCHAR         NOT NULL,
    price               INT             NOT NULL,
    count_views         INT             NOT NULL DEFAULT 0,
    count_comments      INT             NOT NULL DEFAULT 0,
    created_at          TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at          TIMESTAMP       NULL,
    deleted_at          TIMESTAMP       NULL,
    reason_deletion     VARCHAR         NULL
);
--
CREATE INDEX ON "Ads" (id);
CREATE INDEX ON "Ads" (account_id);
--
COMMENT ON TABLE "Ads" is 'Таблица объявлений';
COMMENT ON COLUMN "Ads".id is 'ID объявления в системе';
COMMENT ON COLUMN "Ads".account_id is 'ID аккаунта владельца объявления';
COMMENT ON COLUMN "Ads".title is 'Название объявления';
COMMENT ON COLUMN "Ads".description is 'Описания объявления';
COMMENT ON COLUMN "Ads".price is 'Цена услуги';
COMMENT ON COLUMN "Ads".count_views is 'Количество просмотров объявления';
COMMENT ON COLUMN "Ads".count_comments is 'Количество комментариев';
COMMENT ON COLUMN "Ads".created_at is 'Дата создания';
COMMENT ON COLUMN "Ads".updated_at is 'Дата последнего изменения';
COMMENT ON COLUMN "Ads".deleted_at is 'Дата удаления объявления';
COMMENT ON COLUMN "Ads".reason_deletion is 'Причина удаления объявления';

-- ------------------------

DROP TABLE IF EXISTS "AdsComment";
CREATE TABLE "AdsComment"
(
    id              uuid            PRIMARY KEY DEFAULT uuid_generate_v4(),
    ads_id          uuid            NOT NULL REFERENCES "Ads" (id) ON DELETE CASCADE,
    account_id      uuid            NOT NULL,
    ads_comment     VARCHAR         NOT NULL,
    created_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at      TIMESTAMP       NULL
);
--
CREATE INDEX ON "AdsComment" (id);
CREATE INDEX ON "AdsComment" (ads_id);
CREATE INDEX ON "AdsComment" (account_id);
--
COMMENT ON TABLE "AdsComment" is 'Таблица комментариев к объявлению';
COMMENT ON COLUMN "AdsComment".id is 'ID комментария в системе';
COMMENT ON COLUMN "AdsComment".ads_id is 'ID Объявления';
COMMENT ON COLUMN "AdsComment".account_id is 'ID Автора комментария';
COMMENT ON COLUMN "AdsComment".ads_comment is 'Комментарий в объявлении';
COMMENT ON COLUMN "AdsComment".created_at is 'Дата создания';
COMMENT ON COLUMN "AdsComment".updated_at is 'Дата последнего изменения';

-- ------------------------

GRANT ALL PRIVILEGES ON DATABASE ads TO ads;
GRANT ALL ON SCHEMA public TO ads;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO ads;
GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA public TO ads;