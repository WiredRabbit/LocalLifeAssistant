# Backend Implementation Plan for AI Personal Assistant

## 1. Backend Goal

Build a minimal but production-like backend service that can:
- read restaurant data from PostgreSQL
- accept user requirements from Android client
- filter and rank restaurants based on simple rules
- return structured recommendation results
- later evolve to add AI explanation and multi-turn context

This is the first milestone and should be completed before adding complex AI features.

---

## 2. MVP Scope

### Functional scope
- Create a recommendation API
- Query restaurants from PostgreSQL
- Filter by city, rating, review count, price, and distance (if coordinates are available)
- Return top N results
- Support a simple text query that can be parsed into filters

### Non-goals for MVP
- full AI conversation engine
- multi-user auth system
- complex recommendation algorithm
- advanced caching and observability

---

## 3. Recommended Tech Stack

- Python 3.11+
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- psycopg
- Uvicorn
- Docker (optional for later)

---

## 4. Backend Architecture

### 4.1 Layers
1. API Layer
   - receives request from Android
   - validates input
   - returns JSON response

2. Service Layer
   - parses user input into filters
   - queries database
   - ranks results

3. Data Layer
   - PostgreSQL access
   - business table query

### 4.2 Suggested folders
```text
backend/
  app/
    main.py
    api/
      recommendations.py
    schemas/
      recommendation.py
    services/
      recommendation_service.py
      intent_service.py
    db/
      session.py
    models/
      business.py
    tests/
      test_recommendations.py
  requirements.txt
```

---

## 5. Core API Design

### Endpoint
- POST /api/v1/recommendations

### Request body
```json
{
  "query": "找一个安静、预算不超过 200 的餐厅",
  "city": "Cornelius",
  "max_distance_km": 1,
  "max_price": 2,
  "min_rating": 4.0,
  "limit": 10
}
```

### Response body
```json
{
  "recommendations": [
    {
      "business_id": "abc123",
      "name": "Restaurant A",
      "city": "Cornelius",
      "stars": 4.5,
      "review_count": 120,
      "address": "123 Main St",
      "distance_km": 0.8,
      "categories": "Restaurants, Italian",
      "reason": "评分高、环境较好、预算相符"
    }
  ],
  "summary": "为你筛选出 10 家符合条件的餐厅"
}
```

---

## 6. Data Model

Use the existing businesses table imported from Yelp.

### businesses table fields
- id
- business_id
- name
- address
- city
- state
- postal_code
- latitude
- longitude
- stars
- review_count
- is_open
- categories
- attributes_json
- hours_json
- source
- created_at

---

## 7. Recommendation Logic

### 7.1 Input parsing
The backend should parse the query into a simple filter object.

For example:
- "安静" -> ambiance = quiet
- "预算不超过 200" -> max_price = 200
- "附近 1km" -> max_distance_km = 1
- "评分高" -> min_rating = 4.0

### 7.2 Filtering rules
Start with simple hard rules:
- city filter if provided
- minimum rating if provided
- review count threshold if provided
- price filter if provided
- distance filter if coordinates are available

### 7.3 Ranking logic
Rank results using a simple score.

Example scoring:
- higher rating -> higher score
- more reviews -> higher score
- lower price mismatch -> higher score
- shorter distance -> higher score

A simple formula is:
```text
score = 0.5 * rating_score + 0.2 * review_score + 0.2 * price_score + 0.1 * distance_score
```

### 7.4 Output reason
Generate a short reason in plain text, e.g.:
- "评分高、评论较多、价格相符"
- "位置较近，且符合你的预算"

---

## 8. Database Query Strategy

### Simple query example
```sql
SELECT
  business_id,
  name,
  city,
  stars,
  review_count,
  address,
  latitude,
  longitude,
  categories
FROM businesses
WHERE city = 'Cornelius'
  AND stars >= 4.0
  AND review_count >= 20
ORDER BY stars DESC, review_count DESC
LIMIT 20;
```

### Distance handling
If latitude/longitude are available and the client provides a location, compute distance in Python or use PostgreSQL geospatial functions later.

For MVP, you can first ignore distance or use an approximate filter based on city only.

---

## 9. FastAPI Implementation Notes

### Pydantic models
```python
class RecommendationRequest(BaseModel):
    query: str
    city: Optional[str] = None
    max_distance_km: Optional[float] = None
    max_price: Optional[int] = None
    min_rating: Optional[float] = None
    limit: int = 10

class RecommendationItem(BaseModel):
    business_id: str
    name: str
    city: Optional[str]
    stars: Optional[float]
    review_count: Optional[int]
    address: Optional[str]
    distance_km: Optional[float]
    categories: Optional[str]
    reason: str

class RecommendationResponse(BaseModel):
    recommendations: List[RecommendationItem]
    summary: str
```

### Endpoint skeleton
```python
@app.post("/api/v1/recommendations", response_model=RecommendationResponse)
def recommend(request: RecommendationRequest):
    return recommendation_service.get_recommendations(request)
```

---

## 10. Backend Service Skeleton

### recommendation_service.py
Responsibilities:
- parse input query into filters
- query database
- rank restaurants
- build response

Pseudo-flow:
```python
def get_recommendations(request: RecommendationRequest) -> RecommendationResponse:
    filters = intent_service.parse_query(request.query)
    businesses = repository.fetch_businesses(filters)
    ranked = rank_businesses(businesses, filters)
    items = [build_item(b) for b in ranked[:request.limit]]
    return RecommendationResponse(recommendations=items, summary=...)
```

---

## 11. Suggested Next Step Order

1. Create FastAPI app
2. Add PostgreSQL connection
3. Add businesses table query
4. Implement recommendation endpoint
5. Test with sample request
6. Add simple intent parsing
7. Add simple reason generation
8. Later connect AI provider for explanation generation

---

## 12. Implementation Notes for Claude Code

When generating code, follow these rules:
- keep it minimal and working first
- no over-engineering in the first milestone
- use clear directory structure
- use Pydantic for request/response validation
- use dependency injection style for DB session if possible
- make the recommendation logic easy to test
- keep the AI integration isolated in a separate service layer

---

## 13. Suggested Acceptance Criteria

The backend is considered complete for MVP if:
- a POST request returns a list of recommendations
- results are read from PostgreSQL
- filtering/ranking are performed based on request parameters
- response shape is stable and easy for Android to consume
