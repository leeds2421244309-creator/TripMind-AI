# TripMind-AI 项目架构学习手册

> 本手册目标：让你在没有电脑的情况下，只读这份文档，也能完整理解整个项目的设计思想与代码结构。
>
> 它不是代码审查，不是优化建议，而是一份**面向初学者的长期学习资料**。

---

## 目录

- [第一部分：项目背景理解](#第一部分项目背景理解)
- [第二部分：产品功能与代码对应关系](#第二部分产品功能与代码对应关系)
- [第三部分：整体技术架构](#第三部分整体技术架构)
- [第四部分：Backend 目录详细解析](#第四部分backend-目录详细解析)
- [第五部分：逐文件解释](#第五部分逐文件解释)
- [第六部分：FastAPI 请求生命周期](#第六部分fastapi-请求生命周期)
- [第七部分：解释核心概念](#第七部分解释核心概念)
- [第八部分：数据库设计理解](#第八部分数据库设计理解)
- [第九部分：用户认证系统分析](#第九部分用户认证系统分析)
- [第十部分：AI 模块未来设计](#第十部分ai-模块未来设计)
- [第十一部分：项目开发路线复盘](#第十一部分项目开发路线复盘)
- [第十二部分：学习建议](#第十二部分学习建议)
- [附录 A：文件调用关系总图](#附录-a文件调用关系总图)
- [附录 B：数据流图](#附录-b数据流图)
- [附录 C：用户登录完整流程图](#附录-c用户登录完整流程图)
- [附录 D：AI 生成完整流程图](#附录-dai-生成完整流程图)
- [附录 E：每个文件夹存在原因汇总](#附录-e每个文件夹存在原因汇总)
- [附录 F：初学者必读基础概念补充](#附录-f初学者必读基础概念补充)

---

# 第一部分：项目背景理解

## 1.1 TripMind-AI 是什么项目？

TripMind-AI 是一个**面向大学生的 AI 旅行助手**（AI Travel Companion）。

它不是简单的"AI 行程生成器"，而是一个想陪伴用户走过**完整旅行生命周期**的产品：

```
旅行前（规划）  →  旅行中（陪伴）  →  旅行后（记忆）
```

项目的长期愿景是演化为一个 **AI Travel Agent（AI 旅行智能体）**——能够替用户完成订酒店、订机票、买门票等真实旅行任务。

这是一个**教学兼作品集项目**（educational and portfolio project），目的是探索：如何用现代 AI 技术 + 企业级软件工程流程，构建一个完整的旅行助手。

## 1.2 解决什么用户问题？

根据 `docs/product/PRD.md` 和 `docs/product/UserResearch.md` 中的用户调研，大学生在自由行时面临三大核心痛点：

### 痛点一：信息碎片化

用户规划一次旅行，需要横跨多个平台收集信息：

```
小红书  →  知乎  →  B站  →  Google  →  地图  →  酒店平台
```

问题：信息太多、难以筛选、需要手动整理、攻略可能已过时。

### 痛点二：路线规划困难

用户需要自己决定：
- 去哪些景点？
- 景点之间什么顺序？
- 怎么坐车？
- 每天怎么安排？

问题：耗时、容易做出低效路线、缺乏专业规划经验。

### 痛点三：住宿选择困难

用户不知道：
- 住哪个区域方便？
- 怎么平衡价格和位置？

**TripMind-AI 的解决方案**：用 AI 把分散的旅行信息，转化为个性化、可执行的旅行方案。

## 1.3 目标用户是谁？

**主要用户**：18-25 岁的大学生和年轻独立旅行者。

根据 `docs/product/Persona.md` 的真实用户访谈，典型用户画像：

| 用户 | 特点 | 预算 | 核心诉求 |
|-|-|-|-|
| 面条 | 大学生，缺乏规划经验 | 视目的地而定 | 快速获得可靠旅行起点 |
| 乌柩 | 有经验的年轻旅行者 | 约 5000 元 | 降低决策成本，优化路线 |
| 芊沫 | 注重体验的大学生 | 1000-6000 元 | 减少规划压力，专注体验 |

共同特征：偏好自由行、依赖小红书、需要自己整理路线、希望降低规划时间。

## 1.4 核心使用场景

结合 `docs/product/PRD.md` 中的用户旅程，核心场景如下：

```
用户想去旅行
      ↓
输入目的地、预算、时间、兴趣
      ↓
AI 分析需求，生成个性化旅行方案
（包含每日行程、景点、交通、预算估算）
      ↓
地图可视化展示路线
      ↓
用户保存旅行计划
      ↓
旅行过程中：AI 问答、导航、翻译辅助
      ↓
旅行结束后：整理照片、生成旅行档案
```

### TripMind-AI 的核心创新：AI 计划校验（Plan Validation）

这是区别于普通 AI 生成器的关键功能。用户经常提出**互相矛盾的需求**，例如：

> "酒店预算 300 以内 + 离迪士尼 10 分钟内 + 高端环境"

AI 不仅生成方案，还会**自我校验**：
- 哪些需求满足了？ ✓
- 哪些部分满足？ ⚠
- 哪些无法满足？ ×
- 给出优化建议

这让产品从"AI 内容生成器"升级为"AI 决策助手"。

---

# 第二部分：产品功能与代码对应关系

这一部分建立**产品需求 → 代码文件**的映射，让你知道一个功能最终落在哪。

## 2.1 功能与代码对应表

| 产品功能 | 对应代码文件 | 作用 | 当前状态 |
|-|-|-|-|
| 用户注册 | [auth.py](file:///e:/Odyssey/Projects/TripMind-AI/backend/app/api/auth/auth.py) `register()` | 接收用户名/邮箱/密码，加密后存入 users 表 | ✅ 已实现 |
| 用户登录 | [auth.py](file:///e:/Odyssey/Projects/TripMind-AI/backend/app/api/auth/auth.py) `login()` | 验证密码，生成 JWT Token 返回 | ✅ 已实现 |
| 获取当前用户 | [auth.py](file:///e:/Odyssey/Projects/TripMind-AI/backend/app/api/auth/auth.py) `get_me()` | 通过 Token 解析当前登录用户 | ✅ 已实现 |
| 密码加密 | [security.py](file:///e:/Odyssey/Projects/TripMind-AI/backend/app/core/security.py) | bcrypt 加密与校验密码 | ✅ 已实现 |
| Token 生成与解析 | [jwt.py](file:///e:/Odyssey/Projects/TripMind-AI/backend/app/core/jwt.py) | JWT 签发与解码 | ✅ 已实现 |
| 旅行计划查询 | [travel_plan.py](file:///e:/Odyssey/Projects/TripMind-AI/backend/app/api/travel_plan.py) `get_travel_plans()` | 查询所有旅行计划列表 | ✅ 已实现 |
| 旅行计划创建 | [travel_plan.py](file:///e:/Odyssey/Projects/TripMind-AI/backend/app/api/travel_plan.py) `create_travel_plan()` | 创建新的旅行计划 | ✅ 已实现 |
| 旅行计划修改 | [travel_plan.py](file:///e:/Odyssey/Projects/TripMind-AI/backend/app/api/travel_plan.py) `update_travel_plan()` | 更新旅行计划字段 | ✅ 已实现 |
| 旅行计划删除 | [travel_plan.py](file:///e:/Odyssey/Projects/TripMind-AI/backend/app/api/travel_plan.py) `delete_travel_plan()` | 删除旅行计划 | ✅ 已实现 |
| AI 旅行方案生成 | （规划中）`services/ai_service.py` | 调用通义千问生成行程 | 🔜 待开发 |
| AI Prompt 管理 | （规划中）`prompts/travel_prompt.py` | 管理发送给 LLM 的提示词 | 🔜 待开发 |
| 地图 POI 搜索 | （规划中）`services/map_service.py` | 调用高德地图 API | 🔜 待开发 |
| 路线规划 | （规划中）`services/route_service.py` | 高德路线规划 API | 🔜 待开发 |
| 收藏管理 | [favorite.py](file:///e:/Odyssey/Projects/TripMind-AI/backend/app/models/favorite.py)（model 已建） | 用户收藏旅行方案 | 🔜 待开发（API） |
| AI 对话 | [chat_history.py](file:///e:/Odyssey/Projects/TripMind-AI/backend/app/models/chat_history.py)（model 已建） | 保存 AI 聊天记录 | 🔜 待开发（API） |
| 每日行程管理 | [itinerary_day.py](file:///e:/Odyssey/Projects/TripMind-AI/backend/app/models/itinerary_day.py)（model 已建） | 存储每天早/中/晚安排 | 🔜 待开发（API） |

## 2.2 一个产品需求如何落到代码？

以"用户创建一个旅行计划"为例：

```
产品需求：用户填写目的地、预算、天数，保存一个旅行计划

    ↓ 落到代码

1. schemas/travel_plan.py
   定义 TravelPlanCreate（用户能传什么字段）

2. api/travel_plan.py → create_travel_plan()
   接收请求，调用数据库

3. models/travel_plan.py → TravelPlan 类
   定义数据库表结构

4. db/session.py → get_db()
   提供数据库连接

5. MySQL travel_plans 表
   真正存储数据的地方
```

**记住这个链条**：Schema（输入验证）→ API（接收请求）→ Model（数据库映射）→ MySQL（真实存储）。

---

# 第三部分：整体技术架构

## 3.1 系统架构图

```
                         ┌──────────┐
                         │   用户    │
                         └────┬─────┘
                              │ 浏览器操作
                              ↓
                    ┌─────────────────────┐
                    │  前端 (未来 Vue3)    │
                    │  Vue3 + TypeScript   │
                    │  + Vite + Pinia      │
                    └────────┬────────────┘
                             │ Axios 发送 HTTP 请求
                             ↓
                    ┌─────────────────────┐
                    │   FastAPI 后端       │
                    │  (Python Web 框架)   │
                    └────────┬────────────┘
                             │ 路由分发
              ┌──────────────┼──────────────┐
              ↓              ↓              ↓
        ┌──────────┐  ┌──────────┐  ┌──────────────┐
        │ 业务逻辑  │  │ 数据访问  │  │  外部服务调用  │
        │ Service  │  │   ORM    │  │              │
        └────┬─────┘  └────┬─────┘  └──────┬───────┘
             │             │               │
             │             ↓               ↓
             │      ┌────────────┐  ┌──────────────┐
             │      │   MySQL    │  │ 通义千问 LLM  │
             │      │  数据库    │  │  高德地图 API  │
             │      └────────────┘  └──────────────┘
             │
             └───────────── 第三方 AI / 地图服务
```

## 3.2 每一层存在的意义

### 第一层：前端（Vue3）

**为什么需要它？**
用户不会用命令行，需要一个可视化界面。前端负责：展示数据、收集用户输入、地图可视化。

**为什么选 Vue3？**
- 国内生态成熟，学习资料多
- Composition API 适合中大型项目
- Pinia 是官方推荐的状态管理

> 注意：当前项目前端尚未开发，`frontend/` 目录只有占位 README。当前重点在后端。

### 第二层：FastAPI 后端

**为什么需要它？**
前端不能直接连数据库（不安全），需要一个"中间人"处理业务逻辑。

**为什么选 FastAPI？**
- Python 生态对 AI 最友好（未来要调用 LLM）
- 自动生成 API 文档（Swagger）
- 性能高（基于 Starlette + ASGI）
- 类型提示天然契合 Pydantic

### 第三层：业务层（Service）

**为什么需要它？**
把"做什么"和"怎么做"分开。API 层只管"接收请求"，Service 层管"具体业务逻辑"。

> 当前项目还未建立 `services/` 目录，业务逻辑直接写在 API 中。这是早期阶段的正常做法，后续会拆分。

### 第四层：数据库（MySQL）

**为什么需要它？**
用户数据、旅行计划必须永久保存。内存重启就丢了，文件查询太慢，数据库专门解决"持久化存储 + 高效查询"。

**为什么选 MySQL？**
- 开源稳定、企业广泛使用
- 支持事务、索引优化
- 与 Python + SQLAlchemy 生态成熟

### 第五层：第三方服务

**为什么需要它？**
- **通义千问 LLM**：AI 生成能力不是自己造的，调用专业大模型 API
- **高德地图 API**：地图、POI、路线规划能力调用专业地图服务

**核心设计思想：专注自己的核心业务，非核心能力调用专业服务。**

---

# 第四部分：Backend 目录详细解析

## 4.1 目录总览

```
backend/
├── app/                    ← 应用主目录（所有 Python 代码都在这）
│   ├── api/                ← API 路由层（接收 HTTP 请求）
│   │   ├── auth/           ← 认证相关路由
│   │   │   ├── __init__.py
│   │   │   └── auth.py     ← 注册/登录/获取用户
│   │   ├── __init__.py
│   │   └── travel_plan.py  ← 旅行计划 CRUD 路由
│   ├── core/               ← 核心工具（安全、配置）
│   │   ├── _init_.py
│   │   ├── jwt.py          ← JWT Token 生成与解析
│   │   └── security.py     ← 密码加密与校验
│   ├── db/                 ← 数据库连接层
│   │   ├── __init__.py
│   │   ├── base.py         ← SQLAlchemy 基类
│   │   ├── database.py     ← 引擎创建（连接 MySQL）
│   │   └── session.py      ← Session 工厂（每次请求的数据库会话）
│   ├── models/             ← 数据模型层（SQLAlchemy，对应数据库表）
│   │   ├── __init__.py     ← 统一导出所有模型
│   │   ├── user.py         ← users 表
│   │   ├── travel_plan.py  ← travel_plans 表
│   │   ├── itinerary_day.py← itinerary_days 表
│   │   ├── itinerary_poi.py← itinerary_pois 表
│   │   ├── favorite.py     ← favorites 表
│   │   └── chat_history.py ← chat_history 表
│   ├── schemas/            ← 数据验证层（Pydantic，对应 API 输入输出）
│   │   ├── travel_plan.py  ← 旅行计划的请求/响应模型
│   │   └── user.py         ← 用户的请求/响应模型
│   ├── __init__.py
│   └── main.py             ← 应用入口（启动 FastAPI）
├── .env.example            ← 环境变量示例
├── README.md
└── requirements.txt        ← Python 依赖
```

下面逐个目录解释。

## 4.2 `api/` —— API 路由层

**作用**：接收 HTTP 请求（GET/POST/PUT/DELETE），调用业务逻辑，返回 JSON 响应。

**为什么需要这个目录？**
把"网络入口"和"业务实现"分开。API 层只关心：接收什么参数、返回什么格式。具体怎么查数据库、怎么调 AI，交给其他层。

**为什么不能放到其他目录？**
如果 API 和业务逻辑混在一起，代码会变成"面条代码"，难以测试和复用。

**包含文件**：
- `travel_plan.py`：旅行计划增删改查接口
- `auth/auth.py`：注册、登录、获取当前用户

**调用关系**：
```
HTTP 请求
  ↓
api/（接收请求 + 参数验证）
  ↓
schemas/（验证数据格式）
  ↓
models/（操作数据库）
  ↓
MySQL
```

## 4.3 `core/` —— 核心工具层

**作用**：存放与具体业务无关的"工具能力"，比如密码加密、JWT 处理。

**为什么需要这个目录？**
密码加密、Token 生成是**通用能力**，不属于"旅行计划"也不属于"用户"。它们是基础设施，单独放。

**包含文件**：
- `security.py`：bcrypt 密码加密与校验
- `jwt.py`：JWT Token 的生成与解析、获取当前用户的依赖

**为什么不能放到 models/ 或 api/?**
- 放 `models/`：模型只管"数据长什么样"，不该管加密逻辑
- 放 `api/`：API 只管接收请求，加密是底层能力

## 4.4 `db/` —— 数据库连接层

**作用**：管理数据库连接——创建引擎、提供 Session、定义所有模型的基类。

**为什么需要这个目录？**
数据库连接是**全局共享的资源**，必须在统一地方管理，避免每个文件各自连接。

**包含文件**：
- `database.py`：创建 `engine`（数据库连接引擎）
- `session.py`：创建 `SessionLocal` 和 `get_db()`（每次请求的数据库会话）
- `base.py`：定义 `Base` 类（所有 Model 的父类）

**调用关系**：
```
database.py（创建引擎）
  ↓
session.py（基于引擎创建 Session 工厂）
  ↓
get_db()（每次请求生成一个 Session）
  ↓
api/ 中通过 Depends(get_db) 注入
```

## 4.5 `models/` —— 数据模型层

**作用**：用 Python 类定义数据库表结构。每个类 = 一张表，每个属性 = 一个字段。

**为什么需要这个目录？**
直接写 SQL 字符串容易出错（拼写错误、类型不对）。用类定义表，IDE 能自动补全、类型检查。

**为什么不能放到 api/?**
API 不该关心"表结构长什么样"，只该关心"接收什么请求"。表结构是底层的事。

**包含文件**：
- `user.py` → users 表
- `travel_plan.py` → travel_plans 表
- `itinerary_day.py` → itinerary_days 表
- `itinerary_poi.py` → itinerary_pois 表
- `favorite.py` → favorites 表
- `chat_history.py` → chat_history 表
- `__init__.py` → 统一导出所有模型，方便其他地方 `from app.models import User`

## 4.6 `schemas/` —— 数据验证层

**作用**：定义 API 的输入输出数据格式（用 Pydantic）。验证用户传的数据对不对。

**为什么需要这个目录？**
用户可能传错数据（比如 days 传了字符串"三天"）。Schema 在请求进入业务逻辑前就拦住错误。

**为什么 models 和 schemas 要分开？**（重点，第七部分详解）
- `models` 是给数据库看的（定义表结构）
- `schemas` 是给用户看的（定义 API 能传/能返回什么）
- 两者职责不同：数据库需要 `password_hash`，但用户请求只传 `password`；数据库有 `created_at`，但用户创建时不需要传

**包含文件**：
- `user.py`：UserCreate、UserLogin、Token
- `travel_plan.py`：TravelPlanCreate、TravelPlanUpdate、TravelPlanResponse

## 4.7 `main.py` —— 应用入口

**作用**：创建 FastAPI 应用实例，注册所有路由，启动服务。

**为什么需要它？**
FastAPI 需要一个入口点。所有路由分散在各文件，需要在这里"汇总挂载"。

**启动流程**：
```
uvicorn app.main:app
  ↓
main.py 执行
  ↓
创建 app = FastAPI(...)
  ↓
app.include_router(travel_plan.router)  挂载旅行计划路由
app.include_router(auth.router)         挂载认证路由
  ↓
服务启动，监听端口
```

## 4.8 未来目录预告

根据 `docs/api/API_DESIGN.md` 和 PRD，后续会新增：

| 目录 | 作用 |
|-|-|
| `services/` | 业务逻辑层（AI 调用、地图调用、复杂业务） |
| `prompts/` | AI 提示词管理（发送给 LLM 的模板） |
| `core/ai_client.py` | LLM API 客户端封装 |
| `core/config.py` | 集中配置管理 |

---

# 第五部分：逐文件解释

## 5.1 `app/main.py` —— 应用入口

**作用**：创建 FastAPI 应用，注册路由，提供健康检查接口。

**为什么存在**：FastAPI 应用需要一个起点。所有分散在 `api/` 的路由，必须在这里"挂载"到 app 上才能被访问。

**启动流程**：
1. 导入 `engine`（数据库引擎，启动时建立连接池）
2. 导入各路由模块
3. 创建 `app = FastAPI(title="TripMind AI", version="1.0.0")`
4. 用 `app.include_router()` 挂载路由
5. 定义根路径 `/` 和健康检查 `/health`、`/health/database`

**调用谁**：
- `app.db.database` 的 `engine`（数据库健康检查用）
- `app.api.travel_plan` 的 `router`
- `app.api.auth.auth` 的 `router`

**被谁调用**：由 `uvicorn app.main:app` 命令启动，是整个应用的根。

**关键接口**：
- `GET /` → 返回欢迎信息
- `GET /health` → 服务存活检查
- `GET /health/database` → 数据库连通性检查（执行 `SELECT 1`）

## 5.2 `app/api/travel_plan.py` —— 旅行计划 CRUD

**作用**：提供旅行计划的增删改查接口。

**提供的接口**：

| 方法 | 路径 | 作用 |
|-|-|-|
| GET | `/api/v1/travel-plans/` | 获取所有旅行计划列表 |
| GET | `/api/v1/travel-plans/{plan_id}` | 获取单个旅行计划详情 |
| POST | `/api/v1/travel-plans/` | 创建旅行计划 |
| PUT | `/api/v1/travel-plans/{plan_id}` | 更新旅行计划 |
| DELETE | `/api/v1/travel-plans/{plan_id}` | 删除旅行计划 |

**请求进入后的流转**（以 POST 创建为例）：

```
用户发送 POST /api/v1/travel-plans/
    带 JSON body: {title, destination, days, budget, ...}
        ↓
1. FastAPI 接收请求，匹配到 create_travel_plan 函数
        ↓
2. 参数 plan: TravelPlanCreate 自动用 schemas 验证
   （如果字段不对，直接返回 422 错误）
        ↓
3. db: Session = Depends(get_db) 自动注入数据库连接
        ↓
4. 创建 TravelPlan Model 实例（user_id 当前硬编码为 1）
        ↓
5. db.add(new_plan)  → 加入 Session
   db.commit()       → 提交到 MySQL
   db.refresh()      → 刷新获取自增 ID
        ↓
6. response_model=TravelPlanResponse 自动转换输出格式
        ↓
7. 返回 JSON 给用户
```

**关键设计点**：
- `prefix="/api/v1/travel-plans"` 统一加前缀，方便版本管理
- `tags=["Travel Plans"]` 在 Swagger 文档中分组
- `response_model` 控制返回字段，避免泄露敏感信息

## 5.3 `app/api/auth/auth.py` —— 认证路由

**作用**：用户注册、登录、获取当前登录用户信息。

**提供的接口**：

| 方法 | 路径 | 作用 |
|-|-|-|
| POST | `/api/v1/auth/register` | 注册新用户 |
| POST | `/api/v1/auth/login` | 登录，返回 JWT Token |
| GET | `/api/v1/auth/me` | 获取当前登录用户（需 Token） |

**注册流程**：
```
用户提交 username/email/password
  ↓
调用 security.get_password_hash(password)  bcrypt 加密
  ↓
创建 User 模型，存入 password_hash（不存明文！）
  ↓
db.add + commit + refresh
  ↓
返回用户信息（不含密码）
```

**登录流程**：
```
用户提交 username/password（OAuth2PasswordRequestForm 格式）
  ↓
查数据库找用户 → 没找到返回 400
  ↓
verify_password(明文, hash) 验证 → 不匹配返回 400
  ↓
create_access_token({"sub": user_id}) 生成 JWT
  ↓
返回 {access_token, token_type: "bearer"}
```

**获取当前用户流程**：
```
请求带 Authorization: Bearer <token>
  ↓
Depends(get_current_user) 自动解析 Token
  ↓
jwt.decode 解出 user_id
  ↓
查数据库返回 User 对象
  ↓
接口函数直接拿到 current_user
```

## 5.4 `app/core/security.py` —— 密码安全

**作用**：提供密码的 bcrypt 加密与校验。

**为什么存在**：绝不能存明文密码。bcrypt 是专门为密码设计的哈希算法（自带盐值、故意慢）。

**两个核心函数**：
- `get_password_hash(password)` → 注册时调用，返回哈希字符串
- `verify_password(plain, hashed)` → 登录时调用，返回 True/False

**执行过程**：
```
注册：
"123456" → bcrypt.hash → "$2b$12$xxxxx..." 存入数据库

登录：
用户输入 "123456"
数据库取出 "$2b$12$xxxxx..."
bcrypt.verify("123456", "$2b$12$xxxxx...") → True
```

## 5.5 `app/core/jwt.py` —— JWT Token

**作用**：生成和解析 JWT Token，提供"获取当前用户"的依赖。

**为什么存在**：HTTP 是无状态的，服务器记不住"你是谁"。JWT 是一张"数字身份证"，每次请求带上它，服务器就知道你是谁。

**核心函数**：
- `create_access_token(data)` → 把用户 ID 编码成 Token
- `get_current_user(token, db)` → 从 Token 解出用户，返回 User 对象

**Token 结构**（JWT 三段式）：
```
Header.Payload.Signature
eyJhbGc.eyJzdWIiOiIx.SflKxw

Payload 解码后：
{
  "sub": "1",           ← 用户 ID
  "exp": 1735689600     ← 过期时间（1小时后）
}
```

**关键配置**：
- `SECRET_KEY`：签名密钥（只有服务器知道，防止伪造）
- `ALGORITHM = "HS256"`：签名算法
- `ACCESS_TOKEN_EXPIRE_MINUTES = 60`：Token 有效期 1 小时

## 5.6 `app/db/database.py` —— 数据库引擎

**作用**：读取环境变量，拼接数据库连接字符串，创建 SQLAlchemy 引擎。

**为什么存在**：数据库连接是全局资源，只创建一次，所有请求共用。

**执行过程**：
```
load_dotenv()  ← 从 .env 文件读取环境变量
  ↓
拼接 DATABASE_URL = "mysql+pymysql://user:pass@host:port/dbname"
  ↓
engine = create_engine(DATABASE_URL, echo=True)
  （echo=True 会打印执行的 SQL，方便学习调试）
```

**为什么用环境变量？**
数据库密码是敏感信息，不能写死在代码里（会进 Git）。`.env` 文件在 `.gitignore` 中，不会上传。

## 5.7 `app/db/session.py` —— 数据库会话

**作用**：基于 engine 创建 Session 工厂，提供 `get_db()` 依赖函数。

**为什么存在**：每个请求需要独立的数据库会话（避免并发污染），请求结束就关闭。

**`get_db()` 是整个项目最重要的函数之一**：
```python
def get_db():
    db = SessionLocal()    # 1. 创建 Session
    try:
        yield db           # 2. 把 db 交给接口使用
    finally:
        db.close()         # 3. 请求结束，关闭连接
```

**执行过程**（结合 Depends）：
```
请求来了
  ↓
Depends(get_db) 触发
  ↓
get_db() 执行 → 创建 db → yield 给接口
  ↓
接口用 db 查询数据库
  ↓
接口返回响应
  ↓
finally 执行 → db.close() 关闭连接
```

## 5.8 `app/db/base.py` —— 模型基类

**作用**：定义所有 Model 的父类 `Base`。

**为什么存在**：SQLAlchemy 2.0 要求所有模型继承一个 `DeclarativeBase` 子类。这个 Base 是"所有表的祖先"。

```python
class Base(DeclarativeBase):
    pass
```

虽然只有两行，但它让 SQLAlchemy 知道"哪些类是数据库模型"。

## 5.9 `app/models/*.py` —— 数据模型

每个文件定义一张表。以 `user.py` 为例：

```python
class User(Base):                    # 继承 Base，说明这是张表
    __tablename__ = "users"          # 数据库中的表名

    id: Mapped[int] = mapped_column( # 字段定义
        BigInteger, primary_key=True, autoincrement=True
    )
    username: Mapped[str] = mapped_column(String(50), unique=True, ...)
    ...
```

**所有模型一览**：

| 文件 | 表名 | 作用 |
|-|-|-|
| `user.py` | users | 用户基础信息 |
| `travel_plan.py` | travel_plans | 旅行计划主表 |
| `itinerary_day.py` | itinerary_days | 每日行程（早/中/晚） |
| `itinerary_poi.py` | itinerary_pois | 行程中的具体景点 |
| `favorite.py` | favorites | 用户收藏 |
| `chat_history.py` | chat_history | AI 聊天记录 |

## 5.10 `app/schemas/*.py` —— 数据验证

以 `travel_plan.py` 为例，定义了三种 Schema：

```python
class TravelPlanBase(BaseModel):     # 公共字段（被继承）
    title: str
    destination: str
    ...

class TravelPlanCreate(TravelPlanBase):  # 创建时用（用户传入）
    pass

class TravelPlanUpdate(BaseModel):       # 更新时用
    title: str
    ...

class TravelPlanResponse(TravelPlanBase): # 返回时用（带 id、时间）
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True   # 允许 SQLAlchemy 对象 → Pydantic 对象
```

**为什么分 Create / Update / Response？**
- 创建时：用户不传 id（数据库自增）
- 更新时：可能只改部分字段
- 返回时：要带 id 和时间戳

**`from_attributes = True` 的作用**：
让 Pydantic 能直接读取 SQLAlchemy 对象的属性。没有它，`response_model` 无法把 Model 对象转成 JSON。

---

# 第六部分：FastAPI 请求生命周期

以真实接口 **`POST /api/v1/travel-plans/`**（创建旅行计划）为例，完整追踪一次请求的全过程。

## 6.1 完整生命周期图

```
① 用户发送请求
   POST /api/v1/travel-plans/
   Headers: Content-Type: application/json
   Body: {"title":"东京5日游","destination":"东京","days":5,"budget":8000,...}
        ↓
② main.py 中的 app 接收请求
   FastAPI 根据路径匹配到 travel_plan.router
        ↓
③ 路由匹配
   prefix="/api/v1/travel-plans" + path="/"
   匹配到 create_travel_plan 函数
        ↓
④ Schema 验证（请求体）
   FastAPI 自动把 Body 反序列化为 TravelPlanCreate 对象
   plan: TravelPlanCreate
   ↓
   Pydantic 验证：
   - title 是 str 吗？ ✓
   - days 是 int 吗？ ✓
   - start_date 是合法日期吗？ ✓
   - 必填字段都有吗？
   如果验证失败 → 直接返回 422 Unprocessable Entity
        ↓
⑤ 依赖注入（数据库 Session）
   db: Session = Depends(get_db)
   ↓
   FastAPI 调用 get_db()：
   - 创建 SessionLocal()
   - yield db（把连接交给接口）
        ↓
⑥ 执行业务逻辑（Model 操作）
   new_plan = TravelPlan(
       user_id=1,
       title=plan.title,
       destination=plan.destination,
       ...
   )
   db.add(new_plan)    # 加入 Session（还没入库）
   db.commit()         # 提交事务 → 真正写入 MySQL
   db.refresh(new_plan) # 刷新 → 获取数据库生成的 id、created_at
        ↓
⑦ SQLAlchemy → MySQL
   db.commit() 时，SQLAlchemy 把操作翻译成 SQL：
   INSERT INTO travel_plans (user_id, title, destination, ...)
   VALUES (1, '东京5日游', '东京', ...)
        ↓
⑧ MySQL 执行
   数据真正写入磁盘，返回自增 ID
        ↓
⑨ response_model 转换
   response_model=TravelPlanResponse
   ↓
   FastAPI 把 TravelPlan 对象 → TravelPlanResponse 对象
   （依靠 from_attributes = True）
   ↓
   只返回 Response 中定义的字段（过滤敏感字段）
        ↓
⑩ 返回 JSON
   {
     "id": 1,
     "title": "东京5日游",
     "destination": "东京",
     "days": 5,
     "budget": 8000,
     "user_id": 1,
     "created_at": "2026-08-09T...",
     "updated_at": "2026-08-09T..."
   }
        ↓
⑪ finally 执行
   get_db() 的 finally 块运行 → db.close() 关闭连接
        ↓
⑫ 用户收到 201 Created 响应
```

## 6.2 每一步为什么存在？

| 步骤 | 为什么存在 |
|-|-|
| ① 请求 | 用户的操作入口 |
| ② app 接收 | FastAPI 是统一入口，所有请求先到这 |
| ③ 路由匹配 | 把不同 URL 分发给不同处理函数 |
| ④ Schema 验证 | **在进入业务前拦住非法数据**，避免脏数据入库 |
| ⑤ 依赖注入 | 自动管理数据库连接生命周期，不用手动开关 |
| ⑥ 业务逻辑 | 真正的处理逻辑 |
| ⑦ ORM 翻译 | 让你写 Python 而不是 SQL，提升效率 |
| ⑧ MySQL 执行 | 数据持久化 |
| ⑨ response_model | **控制返回内容**，防止泄露不该返回的字段 |
| ⑩ 返回 JSON | 前端能解析的标准格式 |
| ⑪ 关闭连接 | 释放数据库资源，避免连接泄漏 |

**核心思想：FastAPI 把"安全验证、连接管理、格式转换"这些通用工作自动化了，让你专注写业务逻辑。**

---

# 第七部分：解释核心概念

## 7.1 FastAPI Router（路由）

**问题**：为什么不用所有接口写在 main.py？

**答案**：

如果所有接口都写在 main.py，文件会变成几千行的"巨石"。Router 解决这个问题：

```python
# api/travel_plan.py
router = APIRouter(
    prefix="/api/v1/travel-plans",   # 统一前缀
    tags=["Travel Plans"]            # 文档分组
)

@router.get("/")
def get_travel_plans(): ...

# main.py
app.include_router(travel_plan.router)   # 挂载
```

**好处**：
1. **分文件管理**：旅行计划接口放一个文件，认证接口放另一个
2. **统一前缀**：所有旅行计划接口自动带 `/api/v1/travel-plans`
3. **文档分组**：Swagger UI 自动按 tags 分类展示
4. **可复用**：一个 router 可以挂到多个 app

**类比**：Router 就像"部门"，main.py 是"公司总部"。总部把不同业务分给不同部门处理。

## 7.2 Depends()（依赖注入）

**问题**：`db: Session = Depends(get_db)` 到底怎么执行？

**答案**：`Depends` 是 FastAPI 的**依赖注入**机制。执行过程：

```
1. 请求来了，FastAPI 看到 Depends(get_db)
        ↓
2. 自动调用 get_db()
        ↓
3. get_db() 内部：
   db = SessionLocal()   # 创建连接
   yield db              # 暂停，把 db 交给接口函数
        ↓
4. 接口函数用 db 查询数据库，返回结果
        ↓
5. FastAPI 回到 get_db() 的 yield 之后
   finally: db.close()   # 自动关闭连接
```

**为什么用 Depends 而不是直接调用？**

```python
# ❌ 不好：手动调用，忘记关连接就泄漏了
def get_travel_plans():
    db = SessionLocal()
    plans = db.query(TravelPlan).all()
    db.close()   # 容易忘
    return plans

# ✓ 好：Depends 自动管理生命周期
def get_travel_plans(db: Session = Depends(get_db)):
    return db.query(TravelPlan).all()
    # 用完自动关，不用操心
```

**Depends 还能嵌套**：
```python
def get_current_user(token=Depends(oauth2_scheme), db=Depends(get_db)):
    # token 依赖 oauth2_scheme
    # db 依赖 get_db
    # FastAPI 自动按顺序解析
```

**核心价值**：把"准备工作"和"清理工作"自动化，让你只写核心逻辑。

## 7.3 Schema（为什么 models 和 schemas 要分开？）

这是初学者最容易困惑的点。

**models（SQLAlchemy）**：定义**数据库表结构**
**schemas（Pydantic）**：定义**API 输入输出格式**

**为什么不合并？** 因为两者的"读者"不同：

| 维度 | models（给数据库） | schemas（给用户） |
|-|-|-|
| 读者 | MySQL | 前端/客户端 |
| password | 存 `password_hash`（加密后） | 接收 `password`（明文，加密前） |
| created_at | 数据库自动生成 | 用户创建时不需要传 |
| id | 自增主键 | 创建时不传，返回时才有 |

**具体例子**：

```python
# models/user.py —— 数据库表
class User(Base):
    id: int                    # 数据库自增
    username: str
    email: str
    password_hash: str         # 存加密后的密码
    created_at: datetime       # 数据库自动填

# schemas/user.py —— API 接口
class UserCreate(BaseModel):
    username: str
    email: str
    password: str              # 用户传明文，后端加密后存
    # 没有 id、created_at —— 用户不该传这些
```

**如果合并会怎样？**
- 用户能看到 `password_hash` 字段（安全风险）
- 用户创建时要传 `id`、`created_at`（不合理）
- 数据库结构变动直接影响 API（耦合）

**核心思想：分离关注点。数据库关心存储，API 关心交互。**

## 7.4 SQLAlchemy ORM（为什么不用直接写 SQL？）

**对比**：

```python
# ❌ 直接写 SQL
cursor.execute(
    "INSERT INTO travel_plans (user_id, title, destination, days) "
    "VALUES (%s, %s, %s, %s)",
    (1, title, destination, days)
)

# ✓ 用 ORM
new_plan = TravelPlan(user_id=1, title=title, destination=destination, days=days)
db.add(new_plan)
db.commit()
```

**ORM 的好处**：

1. **防 SQL 注入**：ORM 自动参数化，不用手动防注入
2. **IDE 补全**：`TravelPlan.` 后面能提示所有字段
3. **类型安全**：字段类型错了，启动时就报错
4. **数据库无关**：换 MySQL → PostgreSQL 只改连接字符串
5. **关系映射**：`user.travel_plans` 自动关联查询

**什么时候该用原生 SQL？**
- 极致性能要求（复杂多表 JOIN）
- ORM 表达不了的复杂查询
- 数据库迁移脚本

**核心思想：用面向对象的方式操作数据库，提升开发效率和安全性。**

## 7.5 response_model

**作用**：控制 API 返回的数据结构。

```python
@router.post("/", response_model=TravelPlanResponse)
def create_travel_plan(plan: TravelPlanCreate, db=Depends(get_db)):
    new_plan = TravelPlan(...)   # Model 对象（含所有字段）
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return new_plan   # 返回 Model 对象
```

**FastAPI 做了什么？**
1. 拿到 `new_plan`（TravelPlan Model 对象）
2. 按 `TravelPlanResponse` 定义的字段过滤
3. 只返回 Response 中有的字段
4. 自动转成 JSON

**为什么需要它？**
- **安全**：Model 可能有敏感字段（如 password_hash），Response 不含就自动过滤
- **稳定**：前端依赖固定字段结构，后端加字段不影响前端
- **文档**：Swagger 自动生成响应示例

## 7.6 Pydantic

**它解决什么问题？**

用户传来的 JSON 是"无类型"的字符串。如果不验证，`days` 可能是 `"五"` 而不是 `5`。

**Pydantic 做三件事**：
1. **验证**：数据类型对不对？必填字段有没有？
2. **转换**：字符串 `"5"` 能自动转成 int `5`（如果配置允许）
3. **序列化**：Python 对象 → JSON 返回给前端

```python
class TravelPlanCreate(BaseModel):
    title: str           # 必须是字符串
    days: int            # 必须是整数
    budget: float        # 必须是数字
    start_date: date     # 必须是合法日期

# 用户传 {"title":"东京游","days":"五","budget":8000}
# Pydantic 验证 → "五"不是int → 返回422错误
# 错误信息精确指出：days 字段类型错误
```

**核心价值**：把"数据验证"从业务逻辑中抽离，声明式地定义数据格式。

---

# 第八部分：数据库设计理解

## 8.1 数据库总览

根据 `database/schema.sql` 和 `docs/database/database-design.md`，当前数据库 `tripmind` 包含 6 张表：

| 表名 | 作用 | 核心字段 |
|-|-|-|
| `users` | 用户信息 | id, username, email, password_hash |
| `travel_plans` | 旅行计划 | id, user_id, title, destination, days, budget |
| `itinerary_days` | 每日行程 | id, plan_id, day_number, morning, afternoon, evening |
| `itinerary_pois` | 行程景点 | id, day_id, poi_name, latitude, longitude |
| `favorites` | 用户收藏 | id, user_id, plan_id |
| `chat_history` | AI 聊天记录 | id, user_id, role, message |

## 8.2 各表字段详解

### 8.2.1 users 表（用户）

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,   -- 为什么：唯一标识，自增方便
    username VARCHAR(50) NOT NULL,          -- 为什么：登录用用户名
    email VARCHAR(100) NOT NULL UNIQUE,     -- 为什么：UNIQUE 防止重复注册
    password_hash VARCHAR(255) NOT NULL,    -- 为什么：存加密密码，不存明文！
    avatar VARCHAR(255),                    -- 为什么：头像 URL，可空
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,      -- 为什么：记录注册时间
    updated_at TIMESTAMP ... ON UPDATE CURRENT_TIMESTAMP -- 为什么：自动更新修改时间
);
```

**关键设计**：
- `email UNIQUE`：数据库层面保证邮箱不重复（比代码判断更可靠）
- `password_hash` 而非 `password`：永远不存明文
- `created_at` / `updated_at`：审计字段，追溯数据变化

### 8.2.2 travel_plans 表（旅行计划）

```sql
CREATE TABLE travel_plans (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,                -- 为什么：计划属于谁？外键关联 users
    title VARCHAR(100) NOT NULL,            -- 为什么：计划名称，如"东京5日游"
    destination VARCHAR(100) NOT NULL,      -- 为什么：核心信息——去哪
    departure_city VARCHAR(100),            -- 为什么：出发城市，规划交通用
    start_date DATE,                        -- 为什么：出发日期
    days INT NOT NULL,                      -- 为什么：旅行天数
    budget DECIMAL(10,2),                   -- 为什么：DECIMAL 精确存金额（不用FLOAT）
    travelers INT DEFAULT 1,                -- 为什么：出行人数
    interests TEXT,                         -- 为什么：兴趣标签，自由文本
    transportation VARCHAR(50),             -- 为什么：出行方式（飞机/高铁）
    status ENUM('draft','generated','completed') DEFAULT 'draft',  -- 为什么：状态机
    created_at TIMESTAMP ...,
    updated_at TIMESTAMP ...,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE  -- 为什么：删用户连计划一起删
);
```

**关键设计**：
- `user_id` **外键**：建立 user → plan 的一对多关系。`ON DELETE CASCADE` 表示删用户时自动删其所有计划
- `budget DECIMAL`：金额必须用 DECIMAL，FLOAT 会有精度问题（0.1+0.2≠0.3）
- `status ENUM`：状态机，draft（草稿）→ generated（已生成）→ completed（已完成）
- `interests TEXT`：兴趣可能很长，用 TEXT 而非 VARCHAR

**`user_id` 为什么存在？**
没有它，不知道这个计划是谁的。它是连接用户和计划的"桥梁"。

**`created_at` / `updated_at` 为什么存在？**
- 排序（按时间显示计划列表）
- 审计（什么时候创建/修改的）
- 软删除参考（很久没更新的可以归档）

### 8.2.3 itinerary_days 表（每日行程）

```sql
CREATE TABLE itinerary_days (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    plan_id BIGINT NOT NULL,        -- 为什么：属于哪个旅行计划
    day_number INT NOT NULL,        -- 为什么：第几天（1,2,3...）
    morning TEXT,                   -- 为什么：上午安排
    afternoon TEXT,                 -- 为什么：下午安排
    evening TEXT,                   -- 为什么：晚上安排
    estimated_cost DECIMAL(10,2),   -- 为什么：当天预计花费
    transportation VARCHAR(100),    -- 为什么：当天交通方式
    notes TEXT,                     -- 为什么：备注
    FOREIGN KEY (plan_id) REFERENCES travel_plans(id) ON DELETE CASCADE
);
```

**为什么拆成单独的表？**
一个计划有 N 天，如果塞进 travel_plans 表，要么只能存一天，要么用 JSON（无法查询）。拆表后能按天查询、按天修改。

### 8.2.4 itinerary_pois 表（行程景点）

```sql
CREATE TABLE itinerary_pois (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    day_id BIGINT NOT NULL,              -- 为什么：属于哪一天
    poi_name VARCHAR(200) NOT NULL,      -- 为什么：景点名称
    latitude DECIMAL(10,7),              -- 为什么：经纬度用于地图定位
    longitude DECIMAL(10,7),             -- 7位小数精度足够
    address VARCHAR(255),                -- 为什么：地址
    visit_order INT,                     -- 为什么：游览顺序（第1个去、第2个去）
    stay_minutes INT,                    -- 为什么：停留时长（分钟）
    FOREIGN KEY (day_id) REFERENCES itinerary_days(id) ON DELETE CASCADE
);
```

**`latitude/longitude DECIMAL(10,7)`**：经纬度需要高精度，7位小数约精确到厘米级。

**`visit_order`**：一天可能去多个景点，顺序很重要（影响路线规划）。

### 8.2.5 favorites 表（收藏）

```sql
CREATE TABLE favorites (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    plan_id BIGINT NOT NULL,
    created_at TIMESTAMP ...,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (plan_id) REFERENCES travel_plans(id) ON DELETE CASCADE,
    UNIQUE KEY uk_favorite(user_id, plan_id)   -- 为什么：防止重复收藏
);
```

**`UNIQUE KEY uk_favorite(user_id, plan_id)`**：联合唯一约束，同一个用户对同一个计划只能收藏一次。

### 8.2.6 chat_history 表（AI 聊天记录）

```sql
CREATE TABLE chat_history (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    role ENUM('user','assistant') NOT NULL,  -- 为什么：区分谁说的
    message TEXT NOT NULL,                    -- 为什么：消息内容
    created_at TIMESTAMP ...,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**`role ENUM('user','assistant')`**：AI 对话有"用户说的"和"AI说的"两种，用 role 区分。未来 AI 可以基于历史记录理解上下文。

## 8.3 ER 关系图（实体关系图）

```
┌──────────────┐
│    users     │
│──────────────│
│ id (PK)      │◄────────────────────────────────┐
│ username     │                                 │
│ email        │                                 │
│ password_hash│                                 │
│ created_at   │                                 │
└──────┬───────┘                                 │
       │                                         │
       │ 1:N                                     │
       │ (一个用户多个计划)                          │
       │                                         │
       ▼                                         │
┌──────────────────┐                             │
│  travel_plans    │                             │
│──────────────────│                             │
│ id (PK)          │◄──────────────────────┐     │
│ user_id (FK)─────┘                       │     │
│ title             │                      │     │
│ destination       │       1:N            │     │
│ days              │──────────────┐       │     │
│ budget            │              │       │     │
│ status            │              ▼       │     │
└──────┬────────────┘   ┌──────────────────┐ │   │
       │                │ itinerary_days   │ │   │
       │ 1:N            │──────────────────│ │   │
       │ (计划→收藏)      │ id (PK)          │ │   │
       ▼                │ plan_id (FK)─────┘ │   │
┌──────────────────┐    │ day_number        │   │
│   favorites      │    │ morning/afternoon │   │
│──────────────────│    │ evening           │   │
│ id (PK)          │    └──────┬────────────┘   │
│ user_id (FK)─────┼───┐       │ 1:N             │
│ plan_id (FK)─────┼─┐ │       │ (一天多个景点)    │
│ UNIQUE(user,plan)│ │ │       ▼                 │
└──────────────────┘ │ │  ┌──────────────────┐  │
                   │ │  │ itinerary_pois   │  │
                   │ │  │──────────────────│  │
                   │ │  │ id (PK)          │  │
                   │ │  │ day_id (FK)──────┘  │
                   │ │  │ poi_name            │
                   │ │  │ latitude/longitude  │
                   │ │  │ visit_order         │
                   │ │  └──────────────────┘  │
                   │ │                        │
                   │ └────────────────────────┘
                   │   (收藏关联到计划)
                   │
┌──────────────────┐ │
│  chat_history    │ │
│──────────────────│ │
│ id (PK)          │ │
│ user_id (FK)─────┼─┘
│ role             │
│ message          │
│ created_at       │
└──────────────────┘
```

## 8.4 表关系总结

| 关系 | 类型 | 说明 |
|-|-|-|
| users → travel_plans | 1:N | 一个用户可创建多个计划 |
| travel_plans → itinerary_days | 1:N | 一个计划包含多天行程 |
| itinerary_days → itinerary_pois | 1:N | 一天可去多个景点 |
| users → favorites → travel_plans | N:M | 用户通过 favorites 收藏计划（多对多） |
| users → chat_history | 1:N | 一个用户有多条聊天记录 |

## 8.5 索引设计

`schema.sql` 末尾定义了索引：

```sql
CREATE INDEX idx_plan_user ON travel_plans(user_id);          -- 快速查"某用户的计划"
CREATE INDEX idx_plan_destination ON travel_plans(destination); -- 快速按目的地搜索
CREATE INDEX idx_day_plan ON itinerary_days(plan_id);         -- 快速查"某计划的所有天"
CREATE INDEX idx_poi_day ON itinerary_pois(day_id);           -- 快速查"某天的所有景点"
CREATE INDEX idx_chat_user ON chat_history(user_id);          -- 快速查"某用户的聊天记录"
```

**为什么需要索引？**
没有索引，查"用户1的所有计划"要扫描整张表（慢）。有索引，像查字典目录一样直接定位（快）。

---

# 第九部分：用户认证系统分析

## 9.1 认证系统全景

TripMind-AI 采用 **JWT + bcrypt** 的认证方案，涉及三个核心文件：

```
api/auth/auth.py     ← 路由层：注册/登录/获取用户
       ↓ 调用
core/security.py     ← 密码层：bcrypt 加密/校验
core/jwt.py          ← Token 层：JWT 生成/解析
       ↓ 操作
models/user.py       ← 数据层：users 表
```

## 9.2 注册流程详解

```
用户提交注册信息
{username, email, password}
        ↓
auth.py: register(user: UserCreate, db)
        ↓
security.py: get_password_hash(user.password)
    ↓
    pwd_context = CryptContext(schemes=["bcrypt"])
    pwd_context.hash("123456")
    ↓
    返回 "$2b$12$XXXXXXX..."（bcrypt 哈希）
        ↓
auth.py: 创建 User 模型
    User(
        username=...,
        email=...,
        password_hash="$2b$12$XXXXXXX..."   # 存哈希，不存明文！
    )
        ↓
db.add + commit + refresh
        ↓
返回 {id, username, email}（不含密码）
```

**为什么用 bcrypt 而不是 MD5/SHA256？**
- bcrypt **自带盐值**（每次加密结果不同，防彩虹表攻击）
- bcrypt **故意慢**（增加暴力破解成本）
- bcrypt **可调成本因子**（未来硬件变强可以调高）

## 9.3 登录流程详解

```
用户提交登录
username + password（表单格式 OAuth2PasswordRequestForm）
        ↓
auth.py: login(user, db)
        ↓
查数据库：db.query(User).filter(User.username == user.username).first()
    ↓
    没找到 → HTTPException(400, "用户名不存在")
    找到 → 继续
        ↓
security.py: verify_password(user.password, db_user.password_hash)
    ↓
    pwd_context.verify("123456", "$2b$12$XXXXXXX...")
    ↓
    bcrypt 内部：用同样的盐重新哈希，比对结果
    ↓
    返回 True / False
        ↓
    False → HTTPException(400, "密码错误")
    True → 继续
        ↓
jwt.py: create_access_token({"sub": str(db_user.id)})
    ↓
    1. 复制 data: {"sub": "1"}
    2. 加上过期时间: {"sub":"1", "exp": <1小时后的时间戳>}
    3. jwt.encode(payload, SECRET_KEY, HS256)
    ↓
    返回 Token 字符串
        ↓
返回 {access_token: "eyJhbGc...", token_type: "bearer"}
```

## 9.4 获取当前用户流程详解

```
前端请求带 Header:
Authorization: Bearer eyJhbGc...
        ↓
auth.py: get_me(current_user: User = Depends(get_current_user))
        ↓
jwt.py: get_current_user(token, db)
    ↓
    1. Depends(oauth2_scheme) 自动从 Header 提取 Token
    2. jwt.decode(token, SECRET_KEY, [HS256])
       ↓
       解出 payload: {"sub": "1", "exp": ...}
       ↓
       验证是否过期（过期自动抛异常）
    3. user_id = payload.get("sub")  → "1"
    4. 查数据库: db.query(User).filter(User.id == 1).first()
    5. 返回 User 对象
        ↓
auth.py: 直接用 current_user
    return {id, username, email}
```

## 9.5 三个文件的职责分工

| 文件 | 职责 | 为什么单独放 |
|-|-|-|
| `core/security.py` | 只管密码加密/校验 | 密码逻辑与业务无关，是通用工具 |
| `core/jwt.py` | 只管 Token 生成/解析 | JWT 逻辑复杂，独立维护 |
| `api/auth/auth.py` | 编排注册/登录流程 | 这是业务流程，组合调用上面两个 |

**设计思想：单一职责。** security 不知道业务，jwt 不知道密码，auth 负责把它们组合起来。

## 9.6 JWT 认证 vs Session 认证

| 维度 | JWT（本项目） | Session |
|-|-|-|
| 存储 | 客户端（Token 在前端） | 服务端（内存/Redis） |
| 扩展性 | 好（多服务器无需共享 Session） | 差（需共享 Session 存储） |
| 注销 | 难（Token 过期前一直有效） | 简单（删 Session 即可） |
| 适合 | 前后端分离、移动端 | 传统 Web 应用 |

TripMind-AI 选 JWT 因为是前后端分离架构。

---

# 第十部分：AI 模块未来设计

## 10.1 未来 AI 模块结构

根据 `docs/api/API_DESIGN.md` 的设计（`POST /api/v1/travel/generate`）和 PRD 中的 AI Plan Validation 机制，未来 AI 模块规划如下：

```
app/
├── api/
│   └── ai.py                    ← AI 相关路由（生成旅行方案、AI 问答）
├── services/
│   └── ai_service.py            ← AI 业务逻辑（组装 Prompt、调 LLM、解析结果）
├── prompts/
│   └── travel_prompt.py         ← Prompt 模板管理
└── core/
    └── ai_client.py             ← LLM API 客户端封装（通义千问）
```

## 10.2 为什么这样设计？

### `core/ai_client.py` —— LLM 客户端封装

**职责**：只管"怎么调用通义千问 API"（HTTP 请求、鉴权、重试）。

**为什么单独放？**
LLM SDK 可能升级、可能换模型（通义→GPT→Claude）。封装在一处，换模型只改这一个文件。

### `prompts/travel_prompt.py` —— Prompt 模板

**职责**：管理发送给 LLM 的提示词模板。

**为什么单独放？**
Prompt 是 AI 应用的"灵魂"。好的 Prompt 需要反复调试。如果散落在代码里，修改困难。集中管理便于：
- 版本化（v1 Prompt → v2 Prompt）
- A/B 测试（对比不同 Prompt 效果）
- 复用（多个场景用同一套 Prompt）

### `services/ai_service.py` —— AI 业务逻辑

**职责**：编排"组装 Prompt → 调 LLM → 解析结果 → 存数据库"。

**为什么不写在 api 里？**
AI 生成逻辑复杂（多步骤、异常处理、结果解析）。写在 api 里会让路由文件臃肿。Service 层让 API 保持"瘦"。

### `api/ai.py` —— AI 路由

**职责**：只管接收请求、调用 service、返回结果。

## 10.3 一次 AI 旅行生成请求的完整流转

```
① 用户在前端输入
   {destination: "香港", days: 3, budget: 3000, preferences: ["美食","购物"]}
        ↓
② 前端发送请求
   POST /api/v1/travel/generate
        ↓
③ api/ai.py 接收请求
   → 调用 ai_service.generate_travel_plan(user_input)
        ↓
④ services/ai_service.py 编排
   ↓
   4.1 从 prompts/travel_prompt.py 取 Prompt 模板
       模板形如：
       "你是旅行规划专家。用户想去{destination}，玩{days}天，
        预算{budget}元，喜欢{preferences}。
        请生成详细旅行方案，包含每天早中晚安排..."
   ↓
   4.2 填充用户数据到模板
       destination="香港", days=3, budget=3000, ...
   ↓
   4.3 调用 core/ai_client.py
       ai_client.chat(prompt) → HTTP 请求通义千问 API
        ↓
        通义千问返回 AI 生成的旅行方案（文本/JSON）
        ↓
   4.4 解析 AI 返回结果
       把 AI 文本解析成结构化数据：
       {title, days: [{day:1, morning:..., afternoon:...}]}
        ↓
   4.5 存入数据库
       - TravelPlan 主记录
       - ItineraryDay 每日行程
       - ItineraryPoi 景点信息
        ↓
⑤ api/ai.py 返回响应
   {success: true, data: {title, days: [...]}}
        ↓
⑥ 前端展示
   - 显示旅行方案
   - 地图标注景点
   - 用户可保存/编辑
```

## 10.4 AI Plan Validation（计划校验）的未来实现

根据 PRD 第 13 章，AI 生成后还有"校验"步骤：

```
用户需求输入
    ↓
需求分析（提取结构化需求）
    ↓
旅行计划生成（第一次 LLM 调用）
    ↓
计划校验（第二次 LLM 调用，对比需求 vs 计划）
    ↓
输出评估报告
{
  "match_score": 85,
  "satisfied": ["budget", "destination"],
  "partial": ["hotel_distance"],
  "failed": ["high_end_hotel"],
  "suggestion": "建议增加住宿预算"
}
    ↓
用户查看报告，决定是否调整
```

这是 TripMind-AI 区别于普通 AI 生成器的**核心创新**，体现了 AI Agent 的"反思"能力。

---

# 第十一部分：项目开发路线复盘

## 11.1 28 天开发计划

根据 `docs/development/Day01.md`（已完成 Day01，日期 2026-08-04）和 `docs/product/MVP.md` 中的"4 周 MVP 开发周期"，整理 28 天开发路线如下：

> 说明：`docs/development/` 目前只有 Day01 的开发日志。以下是基于 MVP 范围、当前代码状态和用户提到的"Day8-Day10 AI 能力接入"整理的完整规划。

### 第一周（Day 1-7）：项目基础与后端骨架

| Day | 目标 | 完成内容 | 对应代码/文档 |
|-|-|-|-|
| Day 1 | 项目初始化 | GitHub 仓库、目录结构、README、PRD 框架 | [Day01.md](file:///e:/Odyssey/Projects/TripMind-AI/docs/development/Day01.md) ✅ |
| Day 2 | 产品定义 | PRD 完善、用户画像、用户旅程 | [PRD.md](file:///e:/Odyssey/Projects/TripMind-AI/docs/product/PRD.md) ✅ |
| Day 3 | MVP 范围 | MVP 文档、功能优先级 P0/P1/P2 | [MVP.md](file:///e:/Odyssey/Projects/TripMind-AI/docs/product/MVP.md) ✅ |
| Day 4 | API 设计 | 接口设计文档、错误码规范 | [API_DESIGN.md](file:///e:/Odyssey/Projects/TripMind-AI/docs/api/API_DESIGN.md) ✅ |
| Day 5 | 数据库设计 | schema.sql、ER 关系、索引规划 | [schema.sql](file:///e:/Odyssey/Projects/TripMind-AI/database/schema.sql) ✅ |
| Day 6 | 后端骨架 | FastAPI 项目结构、目录分层 | [backend/app/](file:///e:/Odyssey/Projects/TripMind-AI/backend/app/) ✅ |
| Day 7 | 数据库连接 | engine、session、get_db、健康检查 | [database.py](file:///e:/Odyssey/Projects/TripMind-AI/backend/app/db/database.py) ✅ |

### 第二周（Day 8-14）：AI 能力接入与核心功能

| Day | 目标 | 完成内容 | 对应代码 |
|-|-|-|-|
| Day 8 | AI 客户端 | 通义千问 API 封装、配置管理 | `core/ai_client.py`（待开发） |
| Day 9 | Prompt 工程 | 旅行规划 Prompt 模板设计与调试 | `prompts/travel_prompt.py`（待开发） |
| Day 10 | AI 生成服务 | AI 旅行方案生成、结果解析 | `services/ai_service.py`（待开发） |
| Day 11 | AI 路由 | `POST /api/v1/travel/generate` 接口 | `api/ai.py`（待开发） |
| Day 12 | 用户认证 | 注册、登录、JWT、密码加密 | [auth.py](file:///e:/Odyssey/Projects/TripMind-AI/backend/app/api/auth/auth.py) ✅ |
| Day 13 | 旅行计划 CRUD | 增删改查接口 | [travel_plan.py](file:///e:/Odyssey/Projects/TripMind-AI/backend/app/api/travel_plan.py) ✅ |
| Day 14 | 行程管理 | 每日行程、景点 POI 的 CRUD | `api/itinerary.py`（待开发） |

### 第三周（Day 15-21）：地图集成与前端

| Day | 目标 | 完成内容 | 对应代码 |
|-|-|-|-|
| Day 15 | 地图服务 | 高德 POI 搜索封装 | `services/map_service.py`（待开发） |
| Day 16 | 路线规划 | 高德路线规划、距离计算 | `services/route_service.py`（待开发） |
| Day 17 | 地图 API | POI 搜索、周边推荐接口 | `api/map.py`（待开发） |
| Day 18 | 前端初始化 | Vue3 + Vite 项目搭建 | `frontend/`（待开发） |
| Day 19 | 前端页面 | 首页、生成计划页 | `frontend/views/`（待开发） |
| Day 20 | 地图组件 | 高德地图集成、路线展示 | `frontend/components/`（待开发） |
| Day 21 | 前后端联调 | API 对接、数据流贯通 | 全栈 |

### 第四周（Day 22-28）：完善与交付

| Day | 目标 | 完成内容 | 对应代码 |
|-|-|-|-|
| Day 22 | AI 问答 | 旅行智能问答、聊天记录 | `api/chat.py`（待开发） |
| Day 23 | 收藏功能 | 收藏/取消收藏接口 | `api/favorite.py`（待开发） |
| Day 24 | Plan Validation | AI 计划校验、评估报告 | `services/validation_service.py`（待开发） |
| Day 25 | 用户体验优化 | 错误处理、加载状态、提示 | 全栈 |
| Day 26 | 测试 | 接口测试、边界情况 | 测试用例 |
| Day 27 | 部署 | 服务器部署、环境配置 | 部署脚本 |
| Day 28 | 总结复盘 | 文档整理、作品集总结 | 文档 |

## 11.2 当前进度

**已完成**（对应 Day 1-7 + Day 12-13）：
- ✅ 项目初始化与文档体系（PRD、MVP、API 设计、数据库设计）
- ✅ 后端骨架搭建（FastAPI + SQLAlchemy 分层结构）
- ✅ 数据库设计与建表（6 张表 + 索引 + 外键）
- ✅ 用户认证系统（注册、登录、JWT、bcrypt）
- ✅ 旅行计划 CRUD（增删改查 5 个接口）

**当前所处阶段**：约 Day 13-14，即将进入第二周末。

**下一阶段重点**（Day 14-17）：
1. 完善行程管理 API（itinerary_days、itinerary_pois 的 CRUD）
2. 接入 AI 能力（通义千问 + Prompt 工程）
3. 接入地图能力（高德 POI + 路线规划）

---

# 第十二部分：学习建议

## 12.1 当前最应该理解的知识点

作为软件技术专业学生，通过这个项目学习，**当前阶段优先级**如下：

### 第一优先级：FastAPI 的分层架构思想

这是企业项目的"骨架"。理解为什么分 api / schemas / models / services 四层，比记住任何语法都重要。

**重点理解**：
- 一个请求从进入到返回，经过哪些层
- 为什么 each 层只做一件事
- `Depends()` 依赖注入如何自动管理资源

**对应代码**：[main.py](file:///e:/Odyssey/Projects/TripMind-AI/backend/app/main.py) → [travel_plan.py](file:///e:/Odyssey/Projects/TripMind-AI/backend/app/api/travel_plan.py) → [session.py](file:///e:/Odyssey/Projects/TripMind-AI/backend/app/db/session.py) → [travel_plan.py model](file:///e:/Odyssey/Projects/TripMind-AI/backend/app/models/travel_plan.py)

### 第二优先级：ORM 与数据库的关系

理解 SQLAlchemy Model 和 MySQL 表的对应关系。

**重点理解**：
- 一个 Python 类怎么变成一张表
- `db.query().filter().first()` 对应什么 SQL
- 为什么用外键、为什么用索引

**实践建议**：开 `echo=True`（已在 [database.py](file:///e:/Odyssey/Projects/TripMind-AI/backend/app/db/database.py) 配置），看控制台打印的 SQL，对照理解。

### 第三优先级：认证流程的完整链路

理解"用户密码 → bcrypt → JWT → 请求带 Token → 解析用户"的完整闭环。

**重点理解**：
- 为什么不存明文密码
- JWT 如何让 HTTP"记住"用户
- `Depends(get_current_user)` 如何自动注入当前用户

### 第四优先级：models 与 schemas 的分离

这是初学者最容易困惑的设计。理解"为什么数据库模型和 API 模型要分开"，就理解了"关注点分离"的核心思想。

## 12.2 哪些代码可以暂时不用深入

### 暂时不用深入的

1. **`core/jwt.py` 的加密算法细节**：知道 JWT 能解出 user_id 就行，HS256 的数学原理不用深究
2. **`core/security.py` 的 bcrypt 内部机制**：知道"加密不可逆、自带盐值"就够，算法细节面试时再补
3. **SQLAlchemy 的高级特性**（如 relationship、eager/lazy loading）：当前项目还没用，等需要时再学
4. **FastAPI 的底层 ASGI/Starlette**：会用就行，深入原理是进阶阶段的事
5. **MySQL 的存储引擎、事务隔离级别**：知道 InnoDB 支持事务、外键就够，DBA 级知识后期补

### 可以先跳过、后面回来看的

1. **前端 Vue3 代码**：还没开发，等后端稳固了再学前端
2. **高德地图 SDK 细节**：等服务层建好再看
3. **Prompt 工程的调优技巧**：先让 AI 能跑起来，再优化质量

## 12.3 后续开发应该重点关注什么

### 短期重点（接下来的开发）

1. **AI 集成的架构设计**
   - 如何封装 LLM 客户端（`core/ai_client.py`）
   - Prompt 模板如何管理（`prompts/`）
   - AI 返回结果如何解析存库（`services/ai_service.py`）

   **这是从"CRUD 项目"升级为"AI 应用项目"的关键一步。**

2. **Service 层的引入**
   - 当前的业务逻辑直接写在 API 里（如 [travel_plan.py](file:///e:/Odyssey/Projects/TripMind-AI/backend/app/api/travel_plan.py)）
   - 当 AI 逻辑加入后，必须拆出 Service 层
   - 理解"什么时候该拆 Service"：当 API 函数超过 30 行、逻辑复用时

3. **当前认证与业务的整合**
   - 当前 [travel_plan.py](file:///e:/Odyssey/Projects/TripMind-AI/backend/app/api/travel_plan.py) 中 `user_id=1` 是硬编码
   - 后续要用 `Depends(get_current_user)` 获取真实用户
   - 这是"打通认证与业务"的关键

### 中期重点

1. **地图服务集成**：理解如何封装第三方 API、错误处理、超时重试
2. **AI Plan Validation**：这是产品核心创新，体现"AI 反思"能力
3. **数据库关系查询**：从单表 CRUD 升级到多表关联（plan → days → pois）

### 长期重点

1. **AI Agent 架构**：从"单次生成"到"多步骤规划"
2. **用户偏好学习**：基于历史数据个性化推荐
3. **系统可扩展性**：如何支持更多 AI 模型、更多旅行服务

## 12.4 学习方法建议

1. **先跑通，再深究**：先把项目跑起来，调通一个接口，再回头看架构
2. **看 SQL 学 ORM**：开 `echo=True`，对照 ORM 代码和打印的 SQL
3. **画图理解**：自己画一遍请求流程图、ER 关系图，比读十遍代码管用
4. **带着问题读文档**：FastAPI 官方文档很好，遇到具体问题（如 Depends 怎么用）再查
5. **小步迭代**：每加一个功能，先理解设计，再写代码，最后复盘

---

# 附录 A：文件调用关系总图

> 这张图回答一个核心问题：**哪个文件 import 了哪个文件？谁调用谁？**
>
> 初学者最容易迷路的就是"代码写在哪、从哪开始读"。这张图就是你的"地图"。

## A.1 启动入口（程序从这里开始）

```
命令行: uvicorn app.main:app --reload
              ↓
        加载 main.py
```

## A.2 完整文件依赖关系图

```
app/main.py  ← 程序入口
  │
  ├── import → app/db/database.py          （创建 engine）
  │                ├── import → dotenv     （读 .env）
  │                └── import → sqlalchemy  （create_engine）
  │
  ├── import → app/api/travel_plan.py      （旅行计划路由）
  │    │
  │    ├── import → app/db/session.py      （get_db 依赖）
  │    │              └── import → app/db/database.py（engine）
  │    │
  │    ├── import → app/models/travel_plan.py（TravelPlan 模型）
  │    │              └── import → app/db/base.py（Base 基类）
  │    │
  │    └── import → app/schemas/travel_plan.py（验证 Schema）
  │                   └── import → pydantic（BaseModel）
  │
  └── import → app/api/auth/auth.py        （认证路由）
       │
       ├── import → app/db/session.py      （get_db）
       ├── import → app/models/user.py     （User 模型）
       │              └── import → app/db/base.py
       ├── import → app/schemas/user.py    （UserCreate/Token）
       │              └── import → pydantic
       ├── import → app/core/security.py   （密码加密）
       │              └── import → passlib（CryptContext）
       └── import → app/core/jwt.py        （JWT 处理）
                      ├── import → jose（jwt 编解码）
                      ├── import → fastapi.security（OAuth2PasswordBearer）
                      ├── import → app/db/session.py（get_db）
                      └── import → app/models/user.py（User）
```

## A.3 分层调用关系（从上到下）

```
┌─────────────────────────────────────────────────────────┐
│  入口层    │  main.py                                      │
│            │  创建 app，挂载 router                         │
└──────────────────────┬──────────────────────────────────┘
                       │ include_router()
                       ↓
┌─────────────────────────────────────────────────────────┐
│  路由层    │  api/travel_plan.py    api/auth/auth.py       │
│  (api/)    │  接收 HTTP 请求，调用业务逻辑                   │
└──────┬──────────────────┬──────────────────┬────────────┘
       │                  │                  │
       ↓                  ↓                  ↓
┌────────────┐   ┌──────────────┐   ┌────────────────┐
│ schemas/   │   │ core/        │   │ db/session.py  │
│ 数据验证    │   │ security.py  │   │ get_db()       │
│ (Pydantic) │   │ jwt.py       │   │ 数据库连接      │
└────────────┘   └──────────────┘   └───────┬────────┘
                                            │
                                            ↓
                                   ┌────────────────┐
                                   │ models/        │
                                   │ SQLAlchemy ORM │
                                   │ 操作数据库表     │
                                   └───────┬────────┘
                                           │ SQL
                                           ↓
                                   ┌────────────────┐
                                   │  MySQL 数据库   │
                                   │  真实数据存储    │
                                   └────────────────┘
```

## A.4 关键调用链（读懂这条链 = 读懂整个项目）

以"创建旅行计划"为例，实际代码调用顺序：

```
1. main.py
   app.include_router(travel_plan.router)
       ↓ 路由挂载

2. api/travel_plan.py
   @router.post("/", response_model=TravelPlanResponse)
   def create_travel_plan(plan: TravelPlanCreate, db: Session = Depends(get_db)):
       ↓ 调用 schemas 验证 plan
       ↓ 调用 get_db 获取 db
       ↓ 调用 models 创建对象

3. schemas/travel_plan.py
   class TravelPlanCreate(BaseModel):  ← 验证用户输入
       title: str
       destination: str
       ...

4. db/session.py
   def get_db():
       db = SessionLocal()  ← 创建连接
       yield db
       ↓ 把 db 交给 step 2

5. models/travel_plan.py
   new_plan = TravelPlan(title=..., destination=...)
   db.add(new_plan)
   db.commit()  ← 提交到 MySQL
       ↓ 翻译成 SQL

6. MySQL
   INSERT INTO travel_plans (...) VALUES (...)
       ↓ 写入磁盘

7. schemas/travel_plan.py
   response_model=TravelPlanResponse  ← 过滤返回字段
       ↓ 转成 JSON

8. 返回给用户
```

**阅读建议**：先读 main.py → 再读一个 api 文件 → 跟着 import 跳到 schemas/models/db，就能理解全貌。

---

# 附录 B：数据流图

> 这张图回答：**数据从用户输入到最终返回，经历了哪些"形态变化"？**
>
> 理解数据流，就理解了为什么需要这么多层。

## B.1 数据形态变化全图

```
                  用户在浏览器输入
                  ┌─────────────────────────────┐
                  │ 标题：东京5日游               │
                  │ 目的地：东京                  │
                  │ 天数：5                      │
                  │ 预算：8000                   │
                  └─────────────────────────────┘
                              │
                              │ 前端收集为 JS 对象
                              ↓
                  ┌─────────────────────────────┐
                  │  ① JSON 字符串（HTTP Body）   │  ← 网络传输格式
                  │  {                          │
                  │    "title": "东京5日游",      │
                  │    "destination": "东京",    │
                  │    "days": 5,               │
                  │    "budget": 8000           │
                  │  }                         │
                  └─────────────────────────────┘
                              │
                              │ FastAPI 接收请求
                              ↓
                  ┌─────────────────────────────┐
                  │  ② Pydantic Schema 对象      │  ← 验证 + 类型转换
                  │  TravelPlanCreate(           │
                  │    title="东京5日游",         │
                  │    destination="东京",        │
                  │    days=5,  ← 确保是 int     │
                  │    budget=8000.0  ← 转 float │
                  │  )                         │
                  └─────────────────────────────┘
                              │
                              │ 业务逻辑处理
                              ↓
                  ┌─────────────────────────────┐
                  │  ③ SQLAlchemy Model 对象     │  ← ORM 对象
                  │  TravelPlan(                 │
                  │    id=None,  ← 还没自增      │
                  │    user_id=1,               │
                  │    title="东京5日游",         │
                  │    created_at=None,          │
                  │    updated_at=None           │
                  │  )                         │
                  └─────────────────────────────┘
                              │
                              │ db.commit() 触发
                              ↓
                  ┌─────────────────────────────┐
                  │  ④ SQL 语句                  │  ← 数据库语言
                  │  INSERT INTO travel_plans    │
                  │  (user_id, title, ...)       │
                  │  VALUES (1, '东京5日游', ...)│
                  └─────────────────────────────┘
                              │
                              │ MySQL 执行
                              ↓
                  ┌─────────────────────────────┐
                  │  ⑤ MySQL 表行（磁盘存储）     │  ← 真实数据
                  │  ┌────┬─────┬────────┬────┐ │
                  │  │ id │user │ title  │... │ │
                  │  ├────┼─────┼────────┼────┤ │
                  │  │ 1  │  1  │东京5日游│... │ │
                  │  └────┴─────┴────────┴────┘ │
                  └─────────────────────────────┘
                              │
                              │ db.refresh() 回读
                              ↓
                  ┌─────────────────────────────┐
                  │  ⑥ Model 对象（带完整数据）   │  ← 补全 id、时间戳
                  │  TravelPlan(                 │
                  │    id=1,  ← 现在有了！       │
                  │    user_id=1,               │
                  │    created_at=2026-08-09,    │
                  │    updated_at=2026-08-09     │
                  │  )                         │
                  └─────────────────────────────┘
                              │
                              │ response_model 过滤
                              ↓
                  ┌─────────────────────────────┐
                  │  ⑦ Response Schema 对象      │  ← 只保留该返回的字段
                  │  TravelPlanResponse(         │
                  │    id=1,                     │
                  │    user_id=1,               │
                  │    title="东京5日游",         │
                  │    created_at=...,           │
                  │    updated_at=...            │
                  │  )  ← 没有 password 等敏感字段│
                  └─────────────────────────────┘
                              │
                              │ FastAPI 序列化
                              ↓
                  ┌─────────────────────────────┐
                  │  ⑧ JSON 响应（HTTP Body）    │  ← 返回给前端
                  │  {                          │
                  │    "id": 1,                 │
                  │    "title": "东京5日游",      │
                  │    "days": 5,               │
                  │    ...                      │
                  │  }                         │
                  └─────────────────────────────┘
                              │
                              ↓
                  前端渲染显示给用户
```

## B.2 数据流总结表

| 阶段 | 数据形态 | 所在层 | 负责文件 | 为什么需要这一步 |
|-|-|-|-|-|
| ① | JSON 字符串 | 网络 | HTTP | 跨语言传输的标准格式 |
| ② | Pydantic 对象 | schemas/ | schemas/travel_plan.py | 验证类型正确、拦截非法数据 |
| ③ | Model 对象 | models/ | models/travel_plan.py | 面向对象操作，准备入库 |
| ④ | SQL 语句 | ORM | SQLAlchemy | 翻译成数据库能懂的语言 |
| ⑤ | 表行 | 数据库 | MySQL | 永久持久化存储 |
| ⑥ | Model 对象 | models/ | models/travel_plan.py | 回读自增 ID 和时间戳 |
| ⑦ | Response Schema | schemas/ | schemas/travel_plan.py | 过滤敏感字段，保证返回格式稳定 |
| ⑧ | JSON 字符串 | 网络 | HTTP | 返回给前端的标准格式 |

**核心洞察**：数据不是直接从 JSON 存到数据库的，中间经历了多次"变形"。每次变形都有目的——验证、安全、类型保证。这就是"分层"的本质。

---

# 附录 C：用户登录完整流程图

> 这是包含前端、后端、数据库三方交互的完整登录流程。
>
> 之前的第九部分讲了后端内部流程，这里补全"前端怎么存 Token、后续请求怎么带 Token"。

## C.1 登录全流程（时序图）

```
前端 (Vue3)                    后端 (FastAPI)                 数据库 (MySQL)
    │                               │                              │
    │  ① 用户输入用户名密码           │                              │
    │  username=alice               │                              │
    │  password=123456              │                              │
    │                               │                              │
    │  ② 前端构造表单数据             │                              │
    │  (OAuth2PasswordRequestForm   │                              │
    │   格式: application/x-www-     │                              │
    │   form-urlencoded)            │                              │
    │                               │                              │
    │  ③ POST /api/v1/auth/login    │                              │
    │  ─────────────────────────────>│                              │
    │  Body: username=alice         │                              │
    │        password=123456        │                              │
    │                               │                              │
    │                               │  ④ auth.py: login()          │
    │                               │  解析表单数据                  │
    │                               │                              │
    │                               │  ⑤ 查询用户                   │
    │                               │  SELECT * FROM users         │
    │                               │  WHERE username='alice'      │
    │                               │  ────────────────────────────>│
    │                               │                              │
    │                               │  ⑥ 返回用户记录               │
    │                               │  <────────────────────────────│
    │                               │  {id:1, username:alice,       │
    │                               │   password_hash:"$2b$12$..."} │
    │                               │                              │
    │                               │  ⑦ 没找到用户？               │
    │                               │  → 返回 400 "用户名不存在"     │
    │                               │                              │
    │                               │  ⑧ 验证密码                   │
    │                               │  verify_password(            │
    │                               │    "123456",                 │
    │                               │    "$2b$12$..."              │
    │                               │  )                           │
    │                               │                              │
    │                               │  ⑨ bcrypt 比对哈希            │
    │                               │  匹配 → True                 │
    │                               │  不匹配 → 返回 400 "密码错误"  │
    │                               │                              │
    │                               │  ⑩ 生成 JWT Token             │
    │                               │  create_access_token(        │
    │                               │    {"sub": "1"}              │
    │                               │  )                           │
    │                               │  → "eyJhbGciOi..."           │
    │                               │                              │
    │  ⑪ 返回 Token                 │                              │
    │  <─────────────────────────────│                              │
    │  {                            │                              │
    │    "access_token": "eyJ...",  │                              │
    │    "token_type": "bearer"     │                              │
    │  }                            │                              │
    │                               │                              │
    │  ⑫ 前端保存 Token             │                              │
    │  localStorage.setItem(       │                              │
    │    "token", "eyJ..."          │                              │
    │  )                            │                              │
    │                               │                              │
    │  ⑬ 跳转到首页                  │                              │
    │                               │                              │
```

## C.2 后续请求如何带 Token（认证闭环）

```
前端                            后端                          数据库
  │                               │                             │
  │  ① 用户点击"我的计划"           │                             │
  │                               │                             │
  │  ② 从 localStorage 读 Token   │                             │
  │  token = localStorage         │                             │
  │    .getItem("token")          │                             │
  │                               │                             │
  │  ③ 发送请求（带 Authorization）│                             │
  │  GET /api/v1/auth/me          │                             │
  │  Headers:                     │                             │
  │    Authorization: Bearer      │                             │
  │    eyJhbGciOi...              │                             │
  │  ─────────────────────────────>│                             │
  │                               │                             │
  │                               │  ④ Depends(get_current_user)│
  │                               │  触发                        │
  │                               │                             │
  │                               │  ⑤ oauth2_scheme 从 Header  │
  │                               │  提取 Token                  │
  │                               │  → "eyJhbGciOi..."          │
  │                               │                             │
  │                               │  ⑥ jwt.decode(Token,        │
  │                               │    SECRET_KEY, HS256)       │
  │                               │  → {"sub":"1","exp":...}    │
  │                               │                             │
  │                               │  ⑦ 过期了？                  │
  │                               │  过期 → 401 Unauthorized     │
  │                               │  未过期 → 继续                │
  │                               │                             │
  │                               │  ⑧ 查用户                    │
  │                               │  SELECT * FROM users        │
  │                               │  WHERE id=1                 │
  │                               │  ───────────────────────────>│
  │                               │  <───────────────────────────│
  │                               │  → User 对象                 │
  │                               │                             │
  │                               │  ⑨ 把 User 注入接口函数       │
  │                               │  get_me(current_user=User)  │
  │                               │                             │
  │  ⑩ 返回用户信息                │                             │
  │  <─────────────────────────────│                             │
  │  {                            │                             │
    │    "id": 1,                 │                             │
    │    "username": "alice",     │                             │
    │    "email": "alice@..."     │                             │
    │  }                          │                             │
    │                               │                             │
    │  ⑪ 前端显示用户信息            │                             │
    │                               │                             │
```

## C.3 关键细节解释

### 为什么登录用表单格式而不是 JSON？

```python
# auth.py 中登录接口
def login(user: OAuth2PasswordRequestForm = Depends()):
```

`OAuth2PasswordRequestForm` 是 OAuth2 标准规定的表单格式（`application/x-www-form-urlencoded`），不是 JSON。

**为什么？**
- OAuth2 是国际标准，前端工具（如 Swagger UI 的"Authorize"按钮）默认支持表单格式
- 保持与标准兼容，未来换前端框架不用改后端

**对比**：
| 接口 | 格式 | 原因 |
|-|-|-|
| 注册 `/register` | JSON（`UserCreate`） | 自定义接口，用 JSON 更灵活 |
| 登录 `/login` | 表单（`OAuth2PasswordRequestForm`） | 遵循 OAuth2 标准 |

### Token 存哪里？

前端拿到 Token 后通常存在：
- `localStorage`：关闭浏览器还在（本项目推荐）
- `sessionStorage`：关浏览器就没了
- `Cookie`：自动带，但有 CSRF 风险

### Token 过期了怎么办？

Token 过期后返回 401。前端处理方式：
1. 跳转登录页让用户重新登录（简单方案）
2. 用 refresh_token 自动换新 Token（进阶方案，本项目未来可加）

---

# 附录 D：AI 生成完整流程图

> 这是 AI 旅行方案生成的完整流程，包含前端、后端、LLM、地图、数据库五方交互。
>
> 当前 AI 模块尚未开发，这是按 PRD 和 API 设计文档规划的完整流程。

## D.1 AI 生成全流程（时序图）

```
前端                后端 API          AI Service        LLM(千问)       地图API      数据库
 │                     │                  │                │              │           │
 │ ① 用户填写表单       │                  │                │              │           │
 │ 目的地:香港          │                  │                │              │           │
 │ 天数:3              │                  │                │              │           │
 │ 预算:3000           │                  │                │              │           │
 │ 偏好:美食,购物       │                  │                │              │           │
 │                     │                  │                │              │           │
 │ ② POST /generate    │                  │                │              │           │
 │ ───────────────────>│                  │                │              │           │
 │ Body: JSON          │                  │                │              │           │
 │                     │                  │                │              │           │
 │                     │ ③ 验证 Token      │                │              │           │
 │                     │ Depends(          │                │              │           │
 │                     │   get_current_user)│                │              │           │
 │                     │ → current_user    │                │              │           │
 │                     │                  │                │              │           │
 │                     │ ④ Schema 验证     │                │              │           │
 │                     │ TravelGenerateReq │                │              │           │
 │                     │                  │                │              │           │
 │                     │ ⑤ 调用 AI 服务    │                │              │           │
 │                     │ ai_service        │                │              │           │
 │                     │   .generate(req)  │                │              │           │
 │                     │ ─────────────────>│                │              │           │
 │                     │                  │                │              │           │
 │                     │                  │ ⑥ 取 Prompt 模板│              │           │
 │                     │                  │ prompts/        │              │           │
 │                     │                  │   travel_prompt │              │           │
 │                     │                  │   .build_prompt(│              │           │
 │                     │                  │     "香港",3,    │              │           │
 │                     │                  │     3000,...)   │              │           │
 │                     │                  │                  │              │           │
 │                     │                  │ ⑦ 填充模板       │              │           │
 │                     │                  │ "你是旅行专家... │              │           │
 │                     │                  │  用户想去香港... │              │           │
 │                     │                  │  玩3天...        │              │           │
 │                     │                  │                  │              │           │
 │                     │                  │ ⑧ 调用 LLM       │              │           │
 │                     │                  │ ────────────────>│              │           │
 │                     │                  │ POST /v1/chat    │              │           │
 │                     │                  │   /completions   │              │           │
 │                     │                  │                  │              │           │
 │                     │                  │                  │ ⑨ 千问生成    │           │
 │                     │                  │                  │ 旅行方案      │           │
 │                     │                  │                  │ (JSON格式)   │           │
 │                     │                  │ <────────────────│              │           │
 │                     │                  │                  │              │           │
 │                     │                  │ ⑩ 解析 AI 结果   │              │           │
 │                     │                  │ 提取景点名       │              │           │
 │                     │                  │ 迪士尼、维港...  │              │           │
 │                     │                  │                  │              │           │
 │                     │                  │ ⑪ 查景点坐标     │              │           │
 │                     │                  │ （可选优化）     │              │           │
 │                     │                  │ ────────────────────────────────>│           │
 │                     │                  │                  │              │ POI搜索    │
 │                     │                  │ <───────────────────────────────│ 返回经纬度 │
 │                     │                  │                  │              │           │
 │                     │                  │ ⑫ 存入数据库     │              │           │
 │                     │                  │ - TravelPlan     │              │           │
 │                     │                  │ - ItineraryDay   │              │           │
 │                     │                  │ - ItineraryPoi   │              │           │
 │                     │                  │ ───────────────────────────────────────────>│
 │                     │                  │                  │              │           │ 写入
 │                     │                  │ <───────────────────────────────────────────│
 │                     │                  │ plan_id=42       │              │           │
 │                     │                  │                  │              │           │
 │                     │ <─────────────────│                  │              │           │
 │                     │ 返回结构化方案     │                  │              │           │
 │                     │                  │                  │              │           │
 │ <───────────────────│                  │                  │              │           │
 │ ⑬ JSON 响应         │                  │                │              │           │
 │ {                   │                  │                │              │           │
 │   "plan_id": 42,    │                  │                │              │           │
 │   "title": "香港...",│                  │                │              │           │
 │   "days": [         │                  │                │              │           │
 │     {day:1,         │                  │                │              │           │
 │      morning:"迪士尼",│                  │                │              │           │
 │      pois:[{        │                  │                │              │           │
 │        name:"迪士尼",│                  │                │              │           │
 │        lat:22.31,    │                  │                │              │           │
 │        lng:114.04    │                  │                │              │           │
 │      }]             │                  │                │              │           │
 │     }...            │                  │                │              │           │
 │   ]                 │                  │                │              │           │
 │ }                   │                  │                │              │           │
 │                     │                  │                │              │           │
 │ ⑭ 前端渲染          │                  │                │              │           │
 │ - 显示行程列表       │                  │                │              │           │
 │ - 地图标点          │                  │                │              │           │
 │ - 画路线            │                  │                │              │           │
 │                     │                  │                │              │           │
```

## D.2 AI 生成的数据流（特殊之处）

AI 生成与普通 CRUD 的最大区别：**数据不是用户直接传的，而是 AI 生成的**。

```
用户输入（少量）          AI 生成（大量）
┌──────────────┐        ┌──────────────────────┐
│ 目的地:香港   │        │ Day1 上午:迪士尼乐园   │
│ 天数:3       │  ───>  │ Day1 下午:维多利亚港   │
│ 预算:3000    │  LLM   │ Day1 晚上:尖沙咀美食   │
│ 偏好:美食    │  生成   │ Day2 上午:海洋公园     │
└──────────────┘        │ ...                  │
   4 个字段              │ 几十个字段            │
                        └──────────────────────┘
```

**关键挑战**：
1. **AI 输出不可控**：可能返回不合法 JSON → 需要解析容错
2. **AI 输出无坐标**：AI 只给景点名，经纬度要查地图 API 补全
3. **需要持久化**：AI 生成结果要存 3 张表（plan + days + pois）

## D.3 为什么 AI 生成要拆成 Service 层？

对比普通 CRUD 和 AI 生成的复杂度：

| 维度 | 普通 CRUD（当前） | AI 生成（未来） |
|-|-|-|
| 步骤数 | 1 步（直接存库） | 6+ 步（验证→Prompt→调 LLM→解析→查坐标→存库） |
| 外部依赖 | 无 | LLM API + 地图 API |
| 失败可能 | 数据库错误 | LLM 超时、返回格式错、景点查不到 |
| 代码行数 | ~20 行 | ~100+ 行 |

**结论**：如果把这 100+ 行全写在 `api/ai.py` 里，文件会非常臃肿。拆出 `services/ai_service.py` 让 API 保持简洁。

---

# 附录 E：每个文件夹存在原因汇总

> 一张表回答：**为什么要有这个文件夹？不要行不行？**

## E.1 文件夹存在原因汇总表

| 文件夹 | 存在原因 | 不要会怎样 | 类比 |
|-|-|-|-|
| `app/` | 应用主目录，所有 Python 代码的根 | 代码散落各处，无法统一管理 | 公司大门 |
| `app/api/` | 接收 HTTP 请求，是网络入口 | 业务逻辑和 HTTP 耦合，难测试 | 前台接待 |
| `app/api/auth/` | 认证接口单独分组 | 认证接口和业务接口混一起，难找 | 保安科 |
| `app/core/` | 通用工具（加密、JWT），与业务无关 | 加密逻辑散落在各处，改一处忘一处 | 后勤部 |
| `app/db/` | 数据库连接管理 | 每个文件各自连数据库，连接泄漏 | 水电供应 |
| `app/models/` | 定义数据库表结构（ORM） | 写裸 SQL 字符串，易错难维护 | 仓库货架 |
| `app/schemas/` | 定义 API 输入输出格式 | 不验证用户输入，脏数据直接入库 | 质检部 |
| `app/services/`（未来） | 复杂业务逻辑（AI、地图） | API 文件臃肿，逻辑无法复用 | 生产车间 |
| `app/prompts/`（未来） | AI 提示词模板管理 | Prompt 散落代码中，难调试难复用 | 剧本库 |
| `database/` | SQL 建表脚本 | 表结构只在代码里，无法直接看 DDL | 建筑图纸 |
| `docs/` | 所有文档（PRD、API、架构） | 没文档，新人无法理解项目 | 档案室 |
| `frontend/`（未来） | 前端代码 | 无界面，用户无法使用 | 展厅 |
| `scripts/` | 工具脚本（部署、迁移） | 手动操作，易错 | 工具箱 |

## E.2 分层架构的"为什么"——一张图理解

```
为什么分这么多层？

┌──────────────────────────────────────────────────┐
│ 如果不分层（全部写在一起）：                        │
│                                                  │
│  main.py 里：                                     │
│  - 接收 HTTP 请求                                 │
│  - 验证数据格式                                   │
│  - 加密密码                                       │
│  - 生成 JWT                                      │
│  - 写 SQL 语句                                    │
│  - 连接数据库                                     │
│  - 返回 JSON                                     │
│                                                  │
│  问题：                                          │
│  ① 文件几千行，改一处可能影响全部                    │
│  ② 无法复用（加密函数想给别处用，得复制）             │
│  ③ 无法测试（要测加密逻辑，得启动整个 HTTP 服务）     │
│  ④ 团队协作冲突（多人改同一文件）                    │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│ 分层后：                                          │
│                                                  │
│  api/      只管"接收请求、返回响应"                 │
│  schemas/  只管"数据格式对不对"                     │
│  core/     只管"加密、Token"                       │
│  models/   只管"数据库表结构"                       │
│  db/       只管"数据库连接"                         │
│                                                  │
│  好处：                                          │
│  ① 每个文件职责单一，改一处不影响其他                │
│  ② core/security.py 可被任何 api 复用              │
│  ③ 可单独测试每个模块                              │
│  ④ 团队分模块开发，不冲突                          │
└──────────────────────────────────────────────────┘
```

**一句话总结**：分层不是为了"显得专业"，而是为了**可维护、可复用、可测试、可协作**。

## E.3 文件夹间的"依赖方向"（重要规则）

```
api/  ──依赖──>  schemas/    （api 用 schemas 验证输入输出）
api/  ──依赖──>  core/       （api 用 core 的加密/JWT）
api/  ──依赖──>  db/         （api 用 db 的 get_db）
api/  ──依赖──>  models/     （api 用 models 操作数据）
core/ ──依赖──>  db/         （jwt.py 用 db 的 get_db）
core/ ──依赖──>  models/     （jwt.py 用 models 的 User）
db/   ──依赖──>  无           （db 是最底层，不依赖别人）
models/ ──依赖──> db/base.py （models 依赖 Base 基类）
schemas/ ──依赖──> 无         （schemas 只依赖 pydantic）
```

**黄金法则：依赖只能"向下"（向底层），不能"向上"（向业务）。**

```
✓ 正确：api → core → db
✗ 错误：db → core → api  （db 不该知道业务逻辑）
✗ 错误：models → api     （模型不该知道接口存在）
```

为什么？如果 db 依赖 api，那改 api 就要改 db，底层动荡，整个项目崩溃。底层稳定，上层多变，才是好架构。

---

# 附录 F：初学者必读基础概念补充

> 这些概念在正文里提到了但没展开。如果你第一次接触 FastAPI/Python Web，这一节补齐你的知识盲区。

## F.1 FastAPI 是什么？

**FastAPI 是一个 Python Web 框架**，用来写后端 API（接口）。

### Web 框架解决什么问题？

没有框架，你要自己处理：
- 监听网络端口
- 解析 HTTP 请求（方法、路径、Header、Body）
- 路由分发（哪个 URL 对应哪个函数）
- 序列化 JSON 响应
- 处理并发

框架把这些"脏活累活"包了，你只写业务逻辑：

```python
# 没有 framework，你要写几百行 socket 代码
# 有 FastAPI，只需：
@app.get("/hello")
def hello():
    return {"msg": "hi"}
```

### FastAPI vs Flask vs Django

| 框架 | 特点 | 适合 |
|-|-|-|
| Flask | 轻量，灵活 | 小项目 |
| Django | 重型，自带 admin/ORM/认证 | 全功能网站 |
| **FastAPI** | 现代，异步，自动文档，类型安全 | **API 服务、AI 应用** |

TripMind-AI 选 FastAPI 因为：Python 生态对 AI 最友好 + 自动生成 Swagger 文档。

## F.2 uvicorn 和 ASGI 是什么？

**问题**：FastAPI 写好了，怎么让它"跑起来"接收请求？

**答案**：需要一个"服务器程序"来运行它。这个程序就是 **uvicorn**。

```
uvicorn app.main:app --reload
       │      │    │
       │      │    └── 自动重启（改代码自动生效，开发用）
       │      └────── app 变量（main.py 里的 app = FastAPI()）
       └───────────── app.main 模块（app/main.py）
```

**ASGI**（Asynchronous Server Gateway Interface）是 Python 异步 Web 的标准协议。FastAPI 基于 ASGI，uvicorn 是 ASGI 的实现。

**类比**：
- FastAPI = 你的业务代码
- uvicorn = 跑代码的服务器
- ASGI = 两者之间的"接口标准"

## F.3 `__init__.py` 是什么？为什么每个文件夹都有？

```python
# app/__init__.py      ← 空文件或导出语句
# app/api/__init__.py
# app/models/__init__.py
```

**作用**：告诉 Python "这个文件夹是一个包（package）"，可以被 import。

**没有它会怎样？**
```python
# 没有 __init__.py
from app.models.user import User  # ❌ 报错：找不到模块

# 有 __init__.py
from app.models.user import User  # ✓ 正常
```

**`models/__init__.py` 的特殊作用**：
```python
# models/__init__.py
from app.models.user import User
from app.models.travel_plan import TravelPlan
...

# 这样别处就能简写：
from app.models import User, TravelPlan  # 一行导入所有模型
# 而不用：
from app.models.user import User
from app.models.travel_plan import TravelPlan  # 逐个导入
```

## F.4 `Mapped` 和 `mapped_column` 是什么？（SQLAlchemy 2.0 语法）

在 `models/user.py` 里看到的：

```python
class User(Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
```

**解释**：
- `Mapped[int]`：类型提示，告诉 IDE "这个字段是 int"，能自动补全
- `mapped_column(...)`：实际定义数据库列（类型、约束）

**这是 SQLAlchemy 2.0 的新语法**。旧版写法是：

```python
# 旧写法（1.x）
id = Column(BigInteger, primary_key=True)
username = Column(String(50), unique=True)
```

新版用 `Mapped` 的好处：IDE 能识别类型，写 `user.username` 时提示是 str。

## F.5 `OAuth2PasswordBearer` 是什么？

在 `core/jwt.py` 里：

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
```

**作用**：告诉 FastAPI "需要认证的接口，要从请求 Header 里读 Token"。

**工作过程**：
```
请求进来，带 Header: Authorization: Bearer eyJhbGc...
                                    ↓
oauth2_scheme 自动提取 "eyJhbGc..."
                                    ↓
交给 get_current_user(token) 处理
```

**`tokenUrl="/api/v1/auth/login"`**：告诉 Swagger UI "登录接口是哪个"，这样文档页面会出现"Authorize"按钮。

## F.6 `yield` 是什么？（get_db 里的关键语法）

```python
def get_db():
    db = SessionLocal()
    try:
        yield db    # ← 这个 yield 是什么？
    finally:
        db.close()
```

**`yield` 和 `return` 的区别**：

```python
# return：函数结束，返回值
def get_db():
    db = SessionLocal()
    return db      # 返回后，函数结束
    db.close()     # ❌ 永远不会执行！

# yield：函数"暂停"，返回值，但还没结束
def get_db():
    db = SessionLocal()
    yield db       # 把 db 给调用者，函数暂停
    db.close()     # ✓ 调用者用完后，这里继续执行
```

**FastAPI 配合 yield 的魔法**：
```
请求来 → 调 get_db() → yield db → 暂停 → 接口用 db → 接口返回
→ FastAPI 让 get_db() 继续 → 执行 finally: db.close()
```

这就是为什么 `Depends(get_db)` 能自动关闭连接——`yield` 让函数能"暂停"和"恢复"。

## F.7 HTTP 状态码速查

| 状态码 | 含义 | 本项目何时出现 |
|-|-|-|
| **200** | OK，成功 | GET 查询成功 |
| **201** | Created，创建成功 | POST 创建成功 |
| **400** | Bad Request，请求错误 | 用户名不存在、密码错误 |
| **401** | Unauthorized，未认证 | Token 无效或过期 |
| **404** | Not Found，找不到 | 旅行计划不存在 |
| **422** | Unprocessable Entity，验证失败 | Pydantic 验证不通过（字段类型错） |
| **500** | Internal Server Error | 服务器内部错误 |

**记忆口诀**：
- 2xx = 成功
- 4xx = 客户端的错（你传错了）
- 5xx = 服务器的错（后端崩了）

## F.8 为什么有些接口用 JSON，有些用表单？

| 接口 | 数据格式 | 代码体现 | 原因 |
|-|-|-|-|
| 注册 | JSON | `user: UserCreate` | 自定义接口，JSON 更灵活 |
| 登录 | 表单 | `user: OAuth2PasswordRequestForm = Depends()` | 遵循 OAuth2 国际标准 |
| 创建计划 | JSON | `plan: TravelPlanCreate` | 自定义接口 |

**JSON 格式**：
```
Content-Type: application/json
Body: {"username":"alice","password":"123456"}
```

**表单格式**：
```
Content-Type: application/x-www-form-urlencoded
Body: username=alice&password=123456
```

**为什么登录用表单？** OAuth2 标准规定登录用表单格式。FastAPI 的 `OAuth2PasswordRequestForm` 自动解析表单。好处：Swagger UI 的"Authorize"按钮能直接用。

## F.9 CORS 是什么？为什么前后端分离要配？

**CORS**（Cross-Origin Resource Sharing）：跨域资源共享。

**问题**：浏览器有安全限制——前端在 `localhost:5173`（Vue），后端在 `localhost:8000`（FastAPI），端口不同算"跨域"，浏览器默认拦截。

**解决**：后端告诉浏览器"我允许 localhost:5173 访问"：

```python
# 未来 main.py 会加这段
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 允许前端地址
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**当前项目还没加 CORS**，因为前端还没开发。等 Vue3 起来后必须加，否则前端调不通后端。

## F.10 `BaseModel` 是什么？（Pydantic 基类）

```python
from pydantic import BaseModel

class UserCreate(BaseModel):   # ← 继承 BaseModel
    username: str
    email: str
    password: str
```

**`BaseModel` 是 Pydantic 的核心类**。继承它后，你的类就拥有了：
1. **自动验证**：传错类型自动报错
2. **自动序列化**：对象 → JSON
3. **自动反序列化**：JSON → 对象
4. **类型提示**：IDE 能补全 `.username`

**对比普通类**：
```python
# 普通类，不验证
class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email

User(username=123, email=None)  # 不报错，但数据是脏的

# Pydantic 类，自动验证
class UserCreate(BaseModel):
    username: str
    email: str

UserCreate(username=123, email=None)  # ❌ 报错：类型不对
```

## F.11 什么是"声明式"编程？（FastAPI 的核心哲学）

**命令式**（告诉计算机"怎么做"）：
```python
# 手动验证、手动转换、手动返回
def create_user(request):
    data = request.json()
    if "username" not in data:
        return error("缺少 username")
    if not isinstance(data["username"], str):
        return error("username 必须是字符串")
    # ... 几十行验证代码
    user = User(username=data["username"], ...)
    db.save(user)
    return json.dumps({"id": user.id, ...})
```

**声明式**（告诉框架"我要什么"，框架自动做）：
```python
# 声明数据格式
class UserCreate(BaseModel):
    username: str
    email: str

# 声明接口
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(...)
    db.add(new_user)
    db.commit()
    return new_user
# 框架自动：解析 JSON、验证类型、注入 db、序列化响应
```

**FastAPI 的核心哲学就是声明式**：你声明数据格式（Schema）、声明依赖（Depends）、声明响应模型（response_model），框架自动处理所有"怎么做"的细节。

这也是为什么 FastAPI 代码特别短——你写的是"声明"，不是"步骤"。

---

## 结语

TripMind-AI 不是一个简单的 CRUD 练手项目，它从第一天就按**企业级架构**组织：

- **分层清晰**：api / schemas / models / db / core 各司其职
- **文档先行**：PRD → MVP → API 设计 → 数据库设计 → 代码
- **面向未来**：数据库和架构都为 AI Agent 演进预留了空间

理解这个项目，你学的不仅是 FastAPI 语法，更是**"一个 AI 应用如何从需求到代码"的完整工程思维**。

记住核心设计思想：

> **分离关注点** —— 每一层、每一个文件只做一件事。
>
> **声明优于命令** —— 用类型提示和 Schema 声明数据格式，让框架自动处理。
>
> **依赖注入** —— 把资源管理的脏活累活交给框架，专注业务逻辑。
>
> **文档驱动开发** —— 先想清楚要做什么（PRD），再想怎么做（架构），最后才写代码。

这些思想，比任何具体语法都重要，它们适用于任何语言、任何项目。
