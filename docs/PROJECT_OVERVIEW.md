# 项目概览

LocalLifeAssistant 是一个面向“餐厅推荐场景”的个人助手原型，目标是把自然语言请求转成结构化餐厅推荐结果。

## 功能特点

- 支持基于城市、评分、预算和距离的餐厅筛选
- 通过 FastAPI 提供推荐接口
- 提供 Android 客户端示例，可接入后端接口
- 包含设计文档、数据导入脚本和测试样例

## 技术栈

- 后端：Python 3.10 + FastAPI + psycopg
- 前端/客户端：Kotlin + Android Compose
- 数据：Yelp 商家数据样例

## 运行方式

### 后端

```bash
cd backend
PYTHONPATH=$PWD /Users/baobao/Documents/LocalLifeAssistant/backend/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8002
```

### Android 客户端

在 Android Studio 中打开 android 目录并运行项目。

## 接口示例

```bash
curl -X POST http://127.0.0.1:8002/api/v1/recommendations \
  -H 'Content-Type: application/json' \
  -d '{"query":"找一个安静、预算不超过 200 的餐厅","city":"Phoenix","limit":3}'
```

## 说明

当前项目更偏向“可演示原型”，适合用于课程展示、技术验证或后续扩展为更完整的智能助手。
