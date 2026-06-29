# AI Personal Assistant 项目实现说明书

## 1. 项目目标

构建一个“端云混合”的 AI 智能助手应用，MVP 场景聚焦于“餐厅推荐”。

核心能力：
- 用户输入自然语言需求
- Android 端负责交互、展示、轻量本地智能
- 后端负责意图理解、上下文管理、结构化推荐、AI 生成解释
- 支持多轮对话：用户可以继续补充限制条件，系统根据上下文重新推荐

目标不是做一个纯 Demo，而是要尽量接近真实产品的工程化实现。

---

## 2. 产品范围（MVP）

### 2.1 用户故事
1. 用户在 Android 端输入一句自然语言需求，例如“找一个安静、预算不超过 200 的餐厅”。
2. Android 端将请求发给后端。
3. 后端解析意图、获取候选餐厅、调用 AI 生成简短解释和推荐理由。
4. Android 端展示推荐结果列表。
5. 用户不满意，可继续补充条件，例如“不要太吵”“再近一点”。
6. 后端基于上下文重新生成推荐结果。
7. 用户点击某个结果，查看详情。

### 2.2 MVP 不做
- 完整多端（iOS/Harmony/Flutter）
- 复杂知识库 / RAG
- 完整用户体系与支付
- 大规模推荐算法训练

---

## 3. 技术栈建议

### 3.1 后端
- Python 3.11+
- FastAPI
- Pydantic
- SQLAlchemy + Alembic
- PostgreSQL
- Redis
- Docker / Docker Compose
- OpenAPI / Swagger
- 可选：Celery

### 3.2 Android
- Kotlin
- Jetpack Compose
- MVVM
- ViewModel + StateFlow
- Hilt
- Retrofit
- Room / DataStore
- Material 3

### 3.3 AI 能力
- 优先使用免费模型 / 本地模型
- 推荐方案：
  - 本地开发阶段：Ollama + Qwen / Llama
  - 免费云兜底：Gemini / DeepSeek 试用额度
- 业务层必须抽象为“Provider 接口”，避免死绑定某一家模型

---

## 4. 架构设计

### 4.1 总体架构

Android 端负责体验层和轻量智能，后端负责云端智能与业务编排。

- Android 端：
  - 输入页
  - 会话页
  - 推荐结果列表页
  - 详情页
  - 本地缓存
  - 输入联想 / 快捷条件推荐 / 历史上下文

- 后端：
  - API 层
  - 会话与上下文管理
  - 意图理解
  - 推荐服务
  - AI 服务
  - 数据源服务
  - 缓存与存储

### 4.2 端云边界

#### Android 端适合做
- 输入联想
- 快捷条件推荐
- 本地历史缓存
- 简单意图分类
- 页面渲染与交互
- 轻量状态管理

#### 后端适合做
- 多轮会话上下文
- 复杂意图理解
- 推荐逻辑编排
- 外部数据源接入
- 大模型调用
- 推荐结果结构化
- 日志、限流、缓存、监控

---

## 5. 后端设计

## 5.1 后端目标

后端提供统一智能服务接口，给 Android 端返回结构化推荐结果，并支持多轮对话。

## 5.2 后端目录结构建议

```text
backend/
  app/
    api/
      v1/
        routes/
          sessions.py
          recommendations.py
          health.py
    core/
      config.py
      logging.py
      exceptions.py
    db/
      base.py
      session.py
      models/
        session.py
        message.py
        constraint.py
        recommendation.py
        restaurant.py
    schemas/
      session.py
      message.py
      recommendation.py
      constraint.py
    services/
      session_service.py
      intent_service.py
      recommendation_service.py
      ai_service.py
      provider_factory.py
      providers/
        base.py
        ollama_provider.py
        gemini_provider.py
        deepseek_provider.py
        openai_provider.py
      data_source_service.py
      cache_service.py
    workers/
      tasks.py
    main.py
  tests/
    test_sessions.py
    test_recommendations.py
  requirements.txt
  docker-compose.yml
  Dockerfile
```

## 5.3 API 设计

### 5.3.1 创建会话
- POST /api/v1/sessions

请求体：
```json
{
  "initial_message": "找一个安静、预算不超过 200 的餐厅"
}
```

响应：
```json
{
  "session_id": "sess_123",
  "created_at": "2026-06-25T10:00:00Z"
}
```

### 5.3.2 发送消息并获取推荐
- POST /api/v1/sessions/{session_id}/messages

请求体：
```json
{
  "message": "不要太吵，离我近一点",
  "context": {
    "constraints": {
      "budget": 200,
      "ambiance": "quiet"
    }
  }
}
```

响应：
```json
{
  "session_id": "sess_123",
  "recommendations": [
    {
      "id": "r1",
      "name": "某某餐厅",
      "rating": 4.6,
      "price_level": "$$",
      "distance": "1.2km",
      "tags": ["安静", "适合约会"],
      "reason": "环境舒适，适合轻松聊天，且价格在你的预算范围内",
      "score": 0.92
    }
  ],
  "summary": "我为你筛选出了 3 家符合条件的餐厅。",
  "follow_up_suggestions": [
    "想要更便宜一点的吗？",
    "需要离你更近的选择吗？"
  ]
}
```

### 5.3.3 添加限制条件
- POST /api/v1/sessions/{session_id}/constraints

请求体：
```json
{
  "constraints": [
    {"key": "budget", "value": 200},
    {"key": "distance", "value": "1km"},
    {"key": "ambiance", "value": "quiet"}
  ]
}
```

### 5.3.4 获取会话历史
- GET /api/v1/sessions/{session_id}/history

### 5.3.5 获取详情
- GET /api/v1/recommendations/{recommendation_id}

## 5.4 数据模型

### Session
- id
- created_at
- updated_at
- status
- topic_type

### Message
- id
- session_id
- role
- content
- created_at

### Constraint
- id
- session_id
- key
- value
- created_at

### Recommendation
- id
- session_id
- restaurant_id
- rank
- score
- reason
- created_at

### Restaurant
- id
- name
- rating
- price_level
- address
- latitude
- longitude
- tags
- source

## 5.5 后端服务职责

### SessionService
- 创建会话
- 读取/更新上下文
- 保存消息
- 保存约束条件

### IntentService
- 提取用户意图
- 识别约束条件
- 识别是否是“继续补充条件”或“重新推荐”

### RecommendationService
- 获取候选餐厅
- 过滤与排序
- 生成结果列表

### AIService
- 调用大模型
- 生成解释、摘要、推荐理由
- 进行结构化输出

### ProviderFactory
- 根据配置选择 provider
- 支持本地模型 / 免费云模型 / 付费模型

### DataSourceService
- 连接外部餐厅数据源
- 进行数据转换和统一字段映射

## 5.6 AI Provider 抽象设计

定义统一接口：

```python
class BaseProvider:
    async def chat(self, messages: list[dict], **kwargs) -> str:
        raise NotImplementedError

    async def structured_chat(self, messages: list[dict], schema: dict, **kwargs) -> dict:
        raise NotImplementedError
```

可实现的 provider：
- OllamaProvider
- GeminiProvider
- DeepSeekProvider
- OpenAIProvider

配置示例：
```yaml
ai:
  provider: ollama
  model: qwen2.5:3b
  timeout: 30
  fallback_provider: gemini
```

## 5.7 推荐流程（后端）

1. 接收 Android 请求
2. 读取当前会话上下文
3. 解析新输入中的约束条件
4. 从数据源获取候选餐厅
5. 使用规则过滤与排序
6. 调用 AI 生成推荐理由和总结
7. 返回结构化结果给 Android 端
8. 将上下文和结果保存到数据库

---

## 6. Android 设计

## 6.1 Android 目标

Android 端负责提供良好的用户体验和轻量本地智能能力，核心职责是：
- 输入自然语言
- 展示结果列表与详情
- 支持多轮对话
- 维护本地状态与缓存
- 做端侧轻量提示和条件推荐

## 6.2 Android 目录结构建议

```text
app/
  src/main/java/com/example/app/
    data/
      api/
        ApiService.kt
        ApiClient.kt
      model/
        SessionModel.kt
        RecommendationModel.kt
        ConstraintModel.kt
      repository/
        RecommendationRepository.kt
      local/
        AppDatabase.kt
        SessionDao.kt
        RecommendationDao.kt
    domain/
      usecase/
        SendMessageUseCase.kt
        LoadSessionHistoryUseCase.kt
        AddConstraintUseCase.kt
    ui/
      navigation/
        AppNavHost.kt
      screen/
        home/
          HomeScreen.kt
          HomeViewModel.kt
        chat/
          ChatScreen.kt
          ChatViewModel.kt
        results/
          ResultsScreen.kt
          ResultsViewModel.kt
        detail/
          DetailScreen.kt
          DetailViewModel.kt
      component/
        RecommendationCard.kt
        MessageBubble.kt
        SuggestionChip.kt
        LoadingView.kt
    ui/theme/
    di/
      AppModule.kt
```

## 6.3 页面设计

### 1）首页 / 输入页
内容：
- 标题和引导文案
- 输入框
- 示例按钮
- 最近会话入口

### 2）对话页
内容：
- 用户消息气泡
- 系统返回结果卡片
- AI 解释
- 输入框
- 快捷建议按钮

### 3）推荐列表页
内容：
- 推荐卡片列表
- 评分 / 距离 / 价格 / 标签
- 继续补充条件按钮

### 4）详情页
内容：
- 餐厅基础信息
- AI 推荐理由
- 标签与说明
- 返回/继续对话按钮

## 6.4 Android 状态设计

建议使用 ViewModel + StateFlow 管理 UI 状态：

```kotlin
data class ChatUiState(
    val messages: List<MessageUiModel> = emptyList(),
    val recommendations: List<RecommendationUiModel> = emptyList(),
    val isLoading: Boolean = false,
    val errorMessage: String? = null
)
```

## 6.5 Android 端轻量 AI 能力

### 输入联想
- 根据输入文本实时提示可能的限制条件
- 例如：预算、距离、安静

### 快捷条件推荐
- 基于本地历史和常见场景推荐标签
- 用户点击即可加入条件

### 历史上下文补全
- 根据最近会话自动补全上下文

### 本地缓存
- 最近会话缓存
- 最近推荐结果缓存
- 常用约束条件缓存

## 6.6 Android 网络层设计

### Retrofit 接口
```kotlin
interface ApiService {
    @POST("/api/v1/sessions")
    suspend fun createSession(@Body request: CreateSessionRequest): CreateSessionResponse

    @POST("/api/v1/sessions/{sessionId}/messages")
    suspend fun sendMessage(
        @Path("sessionId") String sessionId,
        @Body request: SendMessageRequest
    ): SendMessageResponse
}
```

## 6.7 Android 端性能优化

- 使用 `LazyColumn` 渲染推荐列表
- 只渲染可见区域
- 对长文本做折叠/展开
- 结果先快显示，再补充解释内容
- 使用 `remember` / `derivedStateOf` 避免不必要重组
- 网络请求使用协程，避免阻塞主线程
- 对最近会话做本地缓存，减少重复请求

## 6.8 Android 端与后端的交互方式

### 主流程
1. 用户输入意图
2. Android 端发起 POST /messages
3. 后端返回推荐结果
4. Android 端渲染结果列表
5. 用户继续补充条件，重复上述流程

---

## 7. 端云混合 AI 设计

### Android 端的 AI 责任
- 输入联想
- 快捷条件推荐
- 本地历史上下文
- 本地缓存和轻量提示

### 后端的 AI 责任
- 意图理解
- 多轮会话上下文
- 推荐生成
- 数据源融合
- 大模型解释生成

### 设计原则
- 端侧做“轻量、低延迟、体验层”能力
- 云端做“复杂、重逻辑、核心智能”能力

---

## 8. 推荐开发顺序

### Phase 1：后端基础能力
- FastAPI 初始化
- 会话接口
- 简单推荐接口
- 数据库与模型
- mock 数据源

### Phase 2：Android 基础交互
- 首页输入页
- 对话页
- 推荐列表页
- 详情页
- 网络层接入

### Phase 3：多轮对话与上下文
- 会话上下文存储
- 条件补充逻辑
- 重新推荐流程

### Phase 4：AI 能力增强
- 大模型接入
- 推荐理由生成
- 结果解释生成
- 本地轻量 AI 提示

### Phase 5：工程化与优化
- 缓存
- 日志
- 异常处理
- 单元测试
- Docker 部署

---

## 9. Claude Code 可直接执行的实现要求

当你要让 Claude Code 直接生成代码时，建议按下面顺序实现：

1. 先实现后端 API 和数据库模型
2. 再实现 Android 的网络层和页面骨架
3. 再接入多轮会话与上下文管理
4. 再接入 AI provider 与推荐服务
5. 最后补 UI 细节、缓存与性能优化

### Claude Code 生成代码时优先遵循的规则
- 先实现 MVP，避免过度设计
- 先保证能跑通再优化结构
- 所有接口都使用统一响应格式
- Android 端使用 ViewModel + StateFlow 管理状态
- 后端使用 FastAPI + Pydantic + SQLAlchemy
- AI provider 必须支持切换，不要写死某一家模型

---

## 10. 交付物清单

### 后端交付物
- FastAPI 服务
- 会话管理接口
- 推荐接口
- 数据库模型
- AI provider 抽象层
- Docker 部署文件

### Android 交付物
- 输入页
- 对话页
- 推荐列表页
- 详情页
- 网络层与 Repository
- 本地缓存
- 轻量端侧 AI 提示能力

---

## 11. 适合简历和面试的表述

“项目采用端云混合架构，Android 端负责交互与轻量本地智能，后端负责多轮对话上下文、意图理解、推荐生成和 AI 能力编排，最终形成一个可演示、可扩展的智能推荐系统。”
