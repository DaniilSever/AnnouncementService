CREATE DATABASE compl WITH OWNER postgres ENCODING 'UTF8';

-- ------------------------

\connect compl;

CREATE USER compl WITH ENCRYPTED PASSWORD 'compl_pwd';

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ------------------------

DROP TABLE IF EXISTS "ComplaintsAccount";
CREATE TABLE "ComplaintsAccount"
(
    id  uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    account_id uuid NOT NULL,
    complaints VARCHAR NOT NULL,
    is_notified BOOLEAN NOT NULL,
    is_resolved BOOLEAN NOT NULL,
    created_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
);
--
CREATE INDEX ON "ComplaintsAccount" (account_id);
--
COMMENT ON TABLE "ComplaintsAccount" is 'Таблица жалоб на пользователей';
COMMENT ON COLUMN "ComplaintsAccount".id is 'ID жалобы в системе';
COMMENT ON COLUMN "ComplaintsAccount".account_id is 'ID Пользователя';
COMMENT ON COLUMN "ComplaintsAccount".complaints is 'Жалоба';
COMMENT ON COLUMN "ComplaintsAccount".is_notified is 'Уведомлен ли автор';
COMMENT ON COLUMN "ComplaintsAccount".is_resolved is 'Решена ли жалоба';
COMMENT ON COLUMN "ComplaintsAccount".created_at is 'Дата создания';

-- ------------------------

DROP TABLE IF EXISTS "ComplaintsAds";
CREATE TABLE "ComplaintsAds"
(
    id  uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    ads_id uuid NOT NULL,
    complaints VARCHAR NOT NULL,
    is_notified BOOLEAN NOT NULL,
    is_resolved BOOLEAN NOT NULL,
    created_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
);
--
CREATE INDEX ON "ComplaintsAds" (ads_id);
--
COMMENT ON TABLE "ComplaintsAds" is 'Таблица жалоб на объявление';
COMMENT ON COLUMN "ComplaintsAds".id is 'ID жалобы в системе';
COMMENT ON COLUMN "ComplaintsAds".ads_id is 'ID Объявления';
COMMENT ON COLUMN "ComplaintsAds".complaints is 'Жалоба';
COMMENT ON COLUMN "ComplaintsAds".is_notified is 'Уведомлен ли автор';
COMMENT ON COLUMN "ComplaintsAds".is_resolved is 'Решена ли жалоба';
COMMENT ON COLUMN "ComplaintsAds".created_at is 'Дата создания';