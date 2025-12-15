-- Source management tables

CREATE TABLE IF NOT EXISTS sources
(
    id              SERIAL PRIMARY KEY,
    type            TEXT NOT NULL, -- web, git, s3, zip, pdf, sql, drive, ...
    name            TEXT,
    config          JSONB NOT NULL,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


-- Job management table

CREATE TABLE IF NOT EXISTS crawl_jobs (
    id SERIAL PRIMARY KEY,
    site_id INTEGER NOT NULL REFERENCES sites(id) ON DELETE CASCADE,
    status TEXT NOT NULL,  -- 'pending', 'running', 'completed', 'failed'
    started_at TIMESTAMP WITH TIME ZONE,
    finished_at TIMESTAMP WITH TIME ZONE,
    error TEXT
);

ALTER TABLE crawl_jobs
ADD COLUMN source_id INTEGER,
ADD CONSTRAINT crawl_jobs_source_id_fkey
    FOREIGN KEY (source_id)
    REFERENCES sources (id)
    ON DELETE CASCADE;


CREATE TABLE IF NOT EXISTS sites (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL UNIQUE,1
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

ALTER TABLE sites
    ADD COLUMN IF NOT EXISTS name TEXT,
    ADD COLUMN IF NOT EXISTS start_url TEXT,
    ADD COLUMN IF NOT EXISTS allowed_domains TEXT[] DEFAULT '{}',
    ADD COLUMN IF NOT EXISTS max_depth INTEGER DEFAULT 2,
    ADD COLUMN IF NOT EXISTS last_crawled_at TIMESTAMP WITH TIME ZONE,
    ADD COLUMN IF NOT EXISTS source_id INTEGER UNIQUE,
    ADD CONSTRAINT sites_source_id_fkey,
        FOREIGN KEY (source_id)
        REFERENCES sources (id)
        ON DELETE CASCADE;


-- Artifact management
CREATE TABLE artifacts (
    id SERIAL PRIMARY KEY,
    source_id INTEGER NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    type TEXT NOT NULL,               -- "upload", "crawl", "sync"
    mime_type TEXT NOT NULL,
    path TEXT NOT NULL,               -- filesystem / object-store path
    size_bytes BIGINT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

ALTER TABLE artifacts
    ADD COLUMN IF NOT EXISTS status TEXT NOT NULL DEFAULT 'created',
    ADD COLUMN IF NOT EXISTS metadata JSONB NOT NULL DEFAULT '{}',
    ADD COLUMN IF NOT EXISTS error TEXT,
    ADD COLUMN IF NOT EXISTS content_hash TEXT;


CREATE TABLE IF NOT EXISTS pages (
    id SERIAL PRIMARY KEY,
    site_id INTEGER NOT NULL REFERENCES sites(id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    html TEXT NOT NULL,
    crawled_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE (site_id, url)
);



