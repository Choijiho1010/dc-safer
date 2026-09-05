-- 최초 기동 시 1회 실행된다. 벡터 확장은 pgvector 구현(ADR-002)에서 사용한다.
CREATE EXTENSION IF NOT EXISTS vector;

-- 인사정보: 이상 탐지 시 '누구에게 어떤 지시를 보낼지'의 근거가 된다.
-- 여기 들어가는 값은 전부 가상 인물이다(data/sop/personas.yaml 이 원천).
CREATE TABLE IF NOT EXISTS operators (
    id               TEXT PRIMARY KEY,
    name             TEXT NOT NULL,
    role             TEXT NOT NULL,
    team             TEXT NOT NULL,
    shift            TEXT NOT NULL CHECK (shift IN ('주간', '야간')),
    experience_years INT  NOT NULL DEFAULT 0,
    escalation_level INT  NOT NULL DEFAULT 1,
    on_call          BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS incidents (
    id           BIGSERIAL PRIMARY KEY,
    scenario_id  TEXT NOT NULL,
    severity     TEXT NOT NULL CHECK (severity IN ('P1', 'P2', 'P3', 'P4')),
    detected_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    closed_at    TIMESTAMPTZ,
    trigger_metric TEXT,
    trigger_value  DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS dispatches (
    id            BIGSERIAL PRIMARY KEY,
    incident_id   BIGINT NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
    operator_id   TEXT   NOT NULL REFERENCES operators(id),
    step          INT    NOT NULL,
    sop_doc_id    TEXT   NOT NULL,
    sop_section   TEXT   NOT NULL,
    instruction   TEXT   NOT NULL,
    status        TEXT   NOT NULL DEFAULT '대기'
                  CHECK (status IN ('대기', '수신', '진행', '보고완료')),
    dispatched_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    reported_at   TIMESTAMPTZ,
    UNIQUE (incident_id, operator_id, step)
);

CREATE INDEX IF NOT EXISTS idx_dispatches_incident ON dispatches(incident_id, step);
