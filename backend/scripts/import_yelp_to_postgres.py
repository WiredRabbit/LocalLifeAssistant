#!/usr/bin/env python3
import json
import os
import sys
from typing import Any, Dict, Optional

import psycopg

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INPUT_PATH = os.path.join(BASE_DIR, "backend", "data", "yelp_academic_dataset_business.json")
DB_NAME = os.getenv("PGDATABASE", "yelp_db")
DB_USER = os.getenv("PGUSER", os.getenv("USER", "postgres"))
DB_PASSWORD = os.getenv("PGPASSWORD", "")
DB_HOST = os.getenv("PGHOST", "localhost")
DB_PORT = os.getenv("PGPORT", "5432")
BATCH_SIZE = 1000


def normalize_categories(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        pieces = [piece.strip() for piece in value.split(",") if piece.strip()]
        return ", ".join(pieces)
    if isinstance(value, list):
        pieces = [str(item).strip() for item in value if str(item).strip()]
        return ", ".join(pieces)
    return str(value)


def normalize_json(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def normalize_record(raw: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "business_id": raw.get("business_id"),
        "name": raw.get("name"),
        "address": raw.get("address"),
        "city": raw.get("city"),
        "state": raw.get("state"),
        "postal_code": raw.get("postal_code"),
        "latitude": raw.get("latitude"),
        "longitude": raw.get("longitude"),
        "stars": raw.get("stars"),
        "review_count": raw.get("review_count"),
        "is_open": bool(raw.get("is_open", 0)),
        "categories": normalize_categories(raw.get("categories")),
        "attributes_json": normalize_json(raw.get("attributes")),
        "hours_json": normalize_json(raw.get("hours")),
        "source": "yelp",
    }


def ensure_schema(conn) -> None:
    with conn.cursor() as cur:
        cur.execute("""
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
        )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_businesses_city ON businesses(city)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_businesses_state ON businesses(state)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_businesses_stars ON businesses(stars)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_businesses_review_count ON businesses(review_count)")
    conn.commit()


def insert_batch(conn, batch):
    with conn.cursor() as cur:
        for item in batch:
            cur.execute(
                """
                INSERT INTO businesses (
                    business_id, name, address, city, state, postal_code,
                    latitude, longitude, stars, review_count, is_open,
                    categories, attributes_json, hours_json, source
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                ON CONFLICT (business_id) DO NOTHING
                """,
                (
                    item["business_id"],
                    item["name"],
                    item["address"],
                    item["city"],
                    item["state"],
                    item["postal_code"],
                    item["latitude"],
                    item["longitude"],
                    item["stars"],
                    item["review_count"],
                    item["is_open"],
                    item["categories"],
                    item["attributes_json"],
                    item["hours_json"],
                    item["source"],
                ),
            )
    conn.commit()


def main() -> None:
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"Input file not found: {INPUT_PATH}")

    conn = psycopg.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )

    ensure_schema(conn)

    batch = []
    imported = 0
    with open(INPUT_PATH, "r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                raw = json.loads(line)
            except json.JSONDecodeError as exc:
                print(f"Skipping malformed JSON at line {line_number}: {exc}")
                continue

            batch.append(normalize_record(raw))
            imported += 1

            if len(batch) >= BATCH_SIZE:
                insert_batch(conn, batch)
                print(f"Imported batch of {len(batch)} records (total {imported})")
                batch.clear()

    if batch:
        insert_batch(conn, batch)
        print(f"Imported final batch of {len(batch)} records")

    conn.close()
    print(f"Import complete. Total records processed: {imported}")


if __name__ == "__main__":
    main()
