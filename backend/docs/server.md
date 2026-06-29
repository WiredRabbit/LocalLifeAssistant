# 服务端设计与后端说明

## 1. 项目用途

这个项目是一个面向餐厅推荐场景的 AI 个人助手。后端负责为 Android 客户端提供数据访问、推荐逻辑以及接口服务。

后端当前需要提供的能力包括：
- 为移动端提供推荐接口
- 从 PostgreSQL 中读取 Yelp 商家数据
- 根据用户意图进行简单筛选和排序
- 为后续接入 AI 解释、上下文记忆等能力打基础

---

## 2. 后端设计目标

后端设计的目标是：
- 结构简单，便于本地开发和调试
- 足够接近企业级，适合项目展示和面试演示
- 分层清晰，后续可以扩展为更复杂的 AI 服务
- 易于和 Android 端对接

### 当前 MVP 目标
- 接收 Android 端传来的用户查询
- 从 PostgreSQL 查询餐厅数据
- 按简单规则筛选和排序结果
- 返回结构化 JSON 给前端

### 后续目标
- 增加 AI 生成解释文本
- 支持多轮对话上下文
- 支持更复杂的推荐和个性化规则
- 增加鉴权、日志、监控等工程化能力

---

## 3. 推荐使用的后端技术栈

- Python 3.10+
- FastAPI 负责接口层
- Pydantic 负责请求与响应校验
- PostgreSQL 负责数据存储
- psycopg 负责数据库连接
- Uvicorn 作为 ASGI 服务运行器

---

## 4. 后端整体架构

当前后端采用简单的分层设计：

1. API 层
   - 处理 HTTP 请求和响应
   - 校验请求参数
   - 暴露给前端调用的接口

2. Service 层
   - 将用户意图解析为筛选条件
   - 查询并排序餐厅数据
   - 生成推荐结果和理由

3. Data 层
   - 与 PostgreSQL 交互
   - 从 businesses 表中读取数据

这种分层方式便于未来扩展和维护。

---

## 5. 当前接口说明

### 推荐接口
- 请求方法：POST
- 路径：/api/v1/recommendations

### 请求示例
```json
{
  "query": "找一个安静、预算不超过 200 的餐厅",
  "city": "Phoenix",
  "limit": 3
}
```

### 响应示例
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

---

## 6. 代码目录结构

```text
backend/
  app/
    api/
      recommendations.py
    schemas/
      recommendation.py
    services/
      recommendation_service.py
    main.py
  tests/
    test_recommendations.py
scripts/
  create_yelp_schema.sql
  import_yelp_to_postgres.py
android/
  app/
    src/main/java/com/example/aiassistant/
      MainActivity.kt
```

### 各目录用途
- backend/app/api：接口路由定义
- backend/app/schemas：请求和响应的数据模型
- backend/app/services：推荐业务逻辑
- backend/app/main.py：应用入口
- backend/tests：后端测试用例
- scripts：数据库建表和数据导入脚本
- android：调用后端接口的 Android 客户端

---

## 7. 数据来源

后端使用 Yelp 的公开商家数据，并导入到 PostgreSQL 中。

核心数据表为：
- businesses

主要字段包括：
- business_id
- name
- city
- stars
- review_count
- address
- categories
- latitude
- longitude

---

## 8. 本地开发流程

### 启动后端
```bash
cd /Users/baobao/Documents/LocalLifeAssistant/backend
PYTHONPATH=/Users/baobao/Documents/LocalLifeAssistant/backend /Users/baobao/Documents/LocalLifeAssistant/backend/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8002
```

### 测试接口
```bash
curl --noproxy '*' -i -X POST http://127.0.0.1:8002/api/v1/recommendations \
  -H 'Content-Type: application/json' \
  -d '{"query":"test","city":"Phoenix","limit":3}'
```

---

## 9. 为什么这种结构适合这个项目

这种后端结构适合当前项目，因为它具备以下优点：
- 能够完整演示“数据 → API → 前端”的链路
- 对面试场景很友好，便于解释架构设计
- 后续可以很自然地扩展到 AI 解释、上下文记忆和更复杂推荐逻辑

它的特点是：实现速度快、结构清晰、同时具备一定工程化意识。

---

## 10. 下一步计划

后续可以继续完善的内容：
- 增加日志与异常处理
- 增加健康检查接口
- 增加更细化的筛选和排序规则
- 接入 AI 生成推荐解释
- 让 Android 页面具备更好的交互体验
