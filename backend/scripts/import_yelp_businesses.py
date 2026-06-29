#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    business_id = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(Text)
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(50))
    postal_code = Column(String(20))
    latitude = Column(Float)
    longitude = Column(Float)
    stars = Column(Float)
    review_count = Column(Integer)
    is_open = Column(Boolean)
    categories = Column(Text)
    attributes_json = Column(Text)
    hours_json = Column(Text)
    source = Column(String(32), default="yelp")
    created_at = Column(DateTime, default=datetime.utcnow)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import Yelp business JSON into a SQLite or PostgreSQL database")
    parser.add_argument("--input", default="/Users/baobao/Documents/LocalLifeAssistant/yelp_academic_dataset_business.json")
    parser.add_argument("--db-url", default=None, help="Database URL, e.g. sqlite:///yelp_businesses.db or postgresql://user:pass@host/db")
    parser.add_argument("--limit", type=int, default=0, help="Optional max number of records to import (0 = all)")
    parser.add_argument("--batch-size", type=int, default=500)
    return parser.parse_args()


def normalize_categories(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        categories = [item.strip() for item in value.split(",") if item.strip()]
        return ", ".join(categories)
    if isinstance(value, list):
        return ", ".join(str(item).strip() for item in value if str(item).strip())
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


def create_engine_from_url(db_url: Optional[str]):
    if db_url:
        return create_engine(db_url)
    default_path = "/Users/baobao/Documents/LocalLifeAssistant/yelp_businesses.db"
    return create_engine(f"sqlite:///{default_path}")


def main() -> None:
    args = parse_args()

    db_url = args.db_url or os.getenv("DATABASE_URL") or None
    engine = create_engine_from_url(db_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    input_path = args.input
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    imported = 0
    batch = []
    with open(input_path, "r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                raw = json.loads(line)
            except json.JSONDecodeError as exc:
                print(f"Skipping malformed JSON at line {line_number}: {exc}")
                continue

            record = normalize_record(raw)
            batch.append(record)

            if args.limit and imported >= args.limit:
                break

            if len(batch) >= args.batch_size:
                insert_batch(session, batch)
                batch.clear()
            imported += 1

    if batch:
        insert_batch(session, batch)

    session.commit()
    session.close()
    print(f"Imported {imported} businesses into {engine.url}")


def insert_batch(session, batch):
    for item in batch:
        exists = session.query(Business).filter(Business.business_id == item["business_id"]).first()
        if exists:
            continue
        session.add(Business(**item))
    session.commit()


if __name__ == "__main__":
    main()
