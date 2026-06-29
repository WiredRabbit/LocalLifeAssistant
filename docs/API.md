# API 接口文档

## 1. 接口概览

当前后端提供一个餐厅推荐接口，供 Android 客户端或其他调用方使用。

## 2. 推荐接口

### 2.1 接口地址

- POST /api/v1/recommendations

### 2.2 请求参数

请求体使用 JSON 格式。

| 字段 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| query | string | 是 | 用户自然语言描述，例如“找一个预算不超过 200 的餐厅” |
| city | string | 否 | 城市名 |
| max_distance_km | number | 否 | 最大距离，单位公里 |
| max_price | integer | 否 | 最大预算 |
| min_rating | number | 否 | 最低评分 |
| limit | integer | 否 | 返回结果数量，范围 1-50，默认 10 |

### 2.3 请求示例

```bash
curl -X POST http://127.0.0.1:8002/api/v1/recommendations \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "找一个安静、预算不超过 200 的餐厅",
    "city": "Phoenix",
    "max_distance_km": 5,
    "max_price": 200,
    "min_rating": 4.0,
    "limit": 3
  }'
```

### 2.4 响应格式

响应体包含推荐结果列表和总结文本。

#### 推荐项字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| business_id | string | 商家 ID |
| name | string | 餐厅名称 |
| city | string | 所在城市 |
| stars | number | 评分 |
| review_count | integer | 评论数量 |
| address | string | 地址 |
| distance_km | number | 距离，可能为空 |
| categories | string | 分类信息 |
| reason | string | 推荐理由 |

#### 响应示例

```json
{
  "recommendations": [
    {
      "business_id": "abc123",
      "name": "Example Restaurant",
      "city": "Phoenix",
      "stars": 4.5,
      "review_count": 2329,
      "address": "123 Main St",
      "distance_km": 1.2,
      "categories": "Restaurants, Italian",
      "reason": "评分高、评论较多"
    }
  ],
  "summary": "为你筛选出 3 家符合条件的餐厅（城市：Phoenix）"
}
```

## 3. 健康检查接口

### 3.1 接口地址

- GET /

### 3.2 响应示例

```json
{
  "message": "AI Personal Assistant API is running"
}
```

## 4. 说明

当前接口是一个轻量级原型，后续可以继续扩展为更智能的自然语言理解、上下文记忆与更复杂的推荐策略。
