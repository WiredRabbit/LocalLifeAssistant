# LocalLifeAssistant

LocalLifeAssistant 是一个面向餐厅推荐场景的个人助手原型，包含：

- Android 客户端：基于 Kotlin / Android Studio 的简化界面
- 后端服务：基于 FastAPI 的餐厅推荐接口
- 数据与设计文档：包含推荐逻辑说明、接口设计和数据导入脚本

## 项目结构

- android/: Android 客户端代码
- backend/: FastAPI 后端与推荐服务
- 项目设计说明：AI 个人助手（餐厅推荐场景）: 需求与设计说明文档

## 快速开始

### 1. 启动后端

```bash
cd backend
PYTHONPATH=$PWD /Users/baobao/Documents/LocalLifeAssistant/backend/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8002
```

### 2. 启动 Android 客户端

在 Android Studio 中打开 android 目录并运行应用。

## 说明

- 当前后端接口地址默认使用 http://127.0.0.1:8002/
- 如果你希望接入真实数据源，需要准备并导入 Yelp 数据集

## 许可证

本项目采用 MIT License。
