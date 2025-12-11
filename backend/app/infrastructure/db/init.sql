-- Sites management table

CREATE TABLE IF NOT EXISTS sites (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL UNIQUE,1
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

ALTER TABLE sites
    ADD COLUMN IF NOT EXISTS name TEXT,
    ADD COLUMN IF NOT EXISTS start_url TEXT,
    ADD COLUMN IF NOT EXISTS allowed_domains TEXT[] DEFAULT '{}',
    ADD COLUMN IF NOT EXISTS max_depth INTEGER DEFAULT 2;


-- Job management table

CREATE TABLE IF NOT EXISTS crawl_jobs (
    id SERIAL PRIMARY KEY,
    site_id INTEGER NOT NULL REFERENCES sites(id) ON DELETE CASCADE,
    status TEXT NOT NULL,  -- 'pending', 'running', 'completed', 'failed'
    started_at TIMESTAMP WITH TIME ZONE,
    finished_at TIMESTAMP WITH TIME ZONE,
    error TEXT
);

CREATE TABLE IF NOT EXISTS pages (
    id SERIAL PRIMARY KEY,
    site_id INTEGER NOT NULL REFERENCES sites(id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    html TEXT NOT NULL,
    crawled_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE (site_id, url)
);



