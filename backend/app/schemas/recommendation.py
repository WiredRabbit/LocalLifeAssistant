from typing import Optional, List

from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    query: str = Field(..., description="User request in Chinese")
    city: Optional[str] = None
    max_distance_km: Optional[float] = None
    max_price: Optional[int] = None
    min_rating: Optional[float] = None
    limit: int = Field(default=10, ge=1, le=50)


class RecommendationItem(BaseModel):
    business_id: str
    name: str
    city: Optional[str]
    stars: Optional[float]
    review_count: Optional[int]
    address: Optional[str]
    distance_km: Optional[float] = None
    categories: Optional[str]
    reason: str


class RecommendationResponse(BaseModel):
    recommendations: List[RecommendationItem]
    summary: str
