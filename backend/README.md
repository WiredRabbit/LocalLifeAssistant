# Backend API

## Run locally

```bash
cd /Users/baobao/Documents/LocalLifeAssistant/backend
PYTHONPATH=/Users/baobao/Documents/LocalLifeAssistant/backend /Users/baobao/Documents/LocalLifeAssistant/backend/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8002
```

## Example request

```bash
curl -X POST http://127.0.0.1:8002/api/v1/recommendations \
  -H 'Content-Type: application/json' \
  -d '{"query":"找一个安静、预算不超过 200 的餐厅","city":"Phoenix","limit":3}'
```

## Expected response

```json
{
  "recommendations": [
    {
      "business_id": "...",
      "name": "...",
      "city": "Phoenix",
      "stars": 5.0,
      "review_count": 2329,
      "address": "...",
      "categories": "...",
      "reason": "评分高、评论较多"
    }
  ],
  "summary": "为你筛选出 3 家符合条件的餐厅（城市：Phoenix）"
}
```
