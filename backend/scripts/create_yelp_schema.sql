CREATE TABLE IF NOT EXISTS businesses (
    id SERIAL PRIMARY KEY,
    business_id TEXT UNIQUE NOT NULL,
    name TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    postal_code TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    stars DOUBLE PRECISION,
    review_count INTEGER,
    is_open BOOLEAN,
    categories TEXT,
    attributes_json TEXT,
    hours_json TEXT,
    source TEXT DEFAULT 'yelp',
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_businesses_city ON businesses(city);
CREATE INDEX IF NOT EXISTS idx_businesses_state ON businesses(state);
CREATE INDEX IF NOT EXISTS idx_businesses_stars ON businesses(stars);
CREATE INDEX IF NOT EXISTS idx_businesses_review_count ON businesses(review_count);
