import os
import re
from typing import Optional

import psycopg

from backend.app.schemas.recommendation import (
    RecommendationItem,
    RecommendationRequest,
    RecommendationResponse,
)


DB_NAME = os.getenv("PGDATABASE", "yelp_db")
DB_USER = os.getenv("PGUSER", os.getenv("USER", "postgres"))
DB_PASSWORD = os.getenv("PGPASSWORD", "")
DB_HOST = os.getenv("PGHOST", "localhost")
DB_PORT = os.getenv("PGPORT", "5432")


class RecommendationService:
    def __init__(self) -> None:
        self.conn = psycopg.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )

    def close(self) -> None:
        self.conn.close()

    def build_filters(self, request: RecommendationRequest) -> tuple[list[str], list[object]]:
        clauses: list[str] = []
        values: list[object] = []

        if request.city:
            clauses.append("city = %s")
            values.append(request.city)

        if request.min_rating is not None:
            clauses.append("stars >= %s")
            values.append(request.min_rating)

        if request.max_distance_km is not None:
            clauses.append("latitude IS NOT NULL")
            clauses.append("longitude IS NOT NULL")

        if request.max_price is not None:
            clauses.append("(categories IS NOT NULL)")

        query = "SELECT business_id, name, city, stars, review_count, address, latitude, longitude, categories FROM businesses"
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY stars DESC, review_count DESC LIMIT %s"
        values.append(request.limit * 5)
        return [query], values

    def recommend(self, request: RecommendationRequest) -> RecommendationResponse:
        query, values = self.build_filters(request)

        with self.conn.cursor() as cur:
            cur.execute(query[0], values)
            rows = cur.fetchall()

        items: list[RecommendationItem] = []
        for row in rows:
            business_id, name, city, stars, review_count, address, latitude, longitude, categories = row
            distance_km = None
            if request.max_distance_km is not None and latitude is not None and longitude is not None:
                distance_km = round(float(abs(latitude - 37.7749)) + float(abs(longitude - -122.4194)) / 100.0, 2)
            reason = self._build_reason(stars, review_count, request)
            items.append(
                RecommendationItem(
                    business_id=business_id,
                    name=name,
                    city=city,
                    stars=stars,
                    review_count=review_count,
                    address=address,
                    distance_km=distance_km,
                    categories=categories,
                    reason=reason,
                )
            )

        if request.max_price is not None:
            items = [item for item in items if item.categories is None or "Restaurant" in item.categories or "Restaurants" in item.categories]

        if request.limit and len(items) > request.limit:
            items = items[: request.limit]

        summary = self._build_summary(request, len(items))
        return RecommendationResponse(recommendations=items, summary=summary)

    def _build_reason(self, stars: Optional[float], review_count: Optional[int], request: RecommendationRequest) -> str:
        reasons = []
        if stars is not None and stars >= 4.0:
            reasons.append("评分高")
        if review_count is not None and review_count >= 100:
            reasons.append("评论较多")
        if request.max_price is not None:
            reasons.append("预算相符")
        if request.max_distance_km is not None:
            reasons.append("位置较近")
        if not reasons:
            reasons.append("符合你的筛选条件")
        return "、".join(reasons)

    def _build_summary(self, request: RecommendationRequest, count: int) -> str:
        base = f"为你筛选出 {count} 家符合条件的餐厅"
        if request.city:
            base += f"（城市：{request.city}）"
        return base
