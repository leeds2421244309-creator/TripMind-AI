# TripMind AI 数据库设计文档

> 项目名称：TripMind AI  
> 项目定位：面向大学生的 AI 全流程旅行助手（AI Travel Agent）  
> 文档版本：v1.0  
> 更新时间：2026-08

---

# 1. 数据库设计目标

TripMind AI 不只是一个 AI 行程生成工具，而是一个完整的旅行智能助手。

数据库需要支持：

- 用户管理
- 旅行计划保存
- AI生成结果存储
- 行程管理
- 景点信息管理
- 用户收藏
- AI对话历史
- 后续 AI Agent 用户记忆


核心数据流：


用户输入旅行需求

    ↓

AI分析用户需求

    ↓

生成旅行计划

    ↓

保存旅行方案

    ↓

旅行过程中持续使用

    ↓

形成用户旅行数据资产


---

# 2. 数据库技术选型

## 数据库

MySQL 8.0


原因：

- 开源稳定
- 企业使用广泛
- 支持事务
- 支持索引优化
- 与 Python FastAPI 生态成熟


## ORM

SQLAlchemy


原因：

- Python 主流 ORM 框架
- 支持对象关系映射
- 提升开发效率
- 方便后期数据库迁移


---

# 3. 数据库整体架构


                users
                  |
      ------------------------
      |                      |
      |                      |

travel_plans chat_history
|
|
itineraries
|
|
|
pois

users
|
|
favorites
|
|
travel_plans



---

# 4. 数据表设计


## 4.1 用户表 users


作用：

保存用户基础信息。


| 字段 | 类型 | 说明 |
|----|----|----|
| id | BIGINT | 用户唯一ID |
| username | VARCHAR(50) | 用户名 |
| email | VARCHAR(100) | 邮箱 |
| password_hash | VARCHAR(255) | 加密密码 |
| avatar | VARCHAR(255) | 用户头像 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |


设计说明：

密码不直接保存明文。

错误：


password = 123456



正确：


password_hash = bcrypt(password)



---

# 4.2 旅行计划表 travel_plans


作用：

保存用户生成的一次完整旅行方案。


| 字段 | 类型 | 说明 |
|-|-|-|
| id | BIGINT | 计划ID |
| user_id | BIGINT | 用户ID |
| title | VARCHAR(100) | 计划标题 |
| destination | VARCHAR(100) | 目的地 |
| start_date | DATE | 开始日期 |
| end_date | DATE | 结束日期 |
| days | INT | 旅行天数 |
| budget | DECIMAL | 预算 |
| people_count | INT | 出行人数 |
| transport | VARCHAR(50) | 出行方式 |
| interest_tags | JSON | 兴趣标签 |
| ai_result | JSON | AI生成结果 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |


设计说明：

AI输出结构具有不确定性。


例如：

未来可能增加：

- 天气分析
- 费用分析
- 推荐理由
- 风险提示


因此使用 JSON 保存 AI 扩展数据。


---

# 4.3 行程详情表 itineraries


作用：

保存每天具体旅行安排。


|字段|类型|说明|
|-|-|-|
|id|BIGINT|行程ID|
|plan_id|BIGINT|旅行计划ID|
|day_number|INT|第几天|
|time_period|VARCHAR(20)|时间段|
|poi_id|BIGINT|地点ID|
|description|TEXT|行程描述|
|transport_info|TEXT|交通信息|
|estimated_cost|DECIMAL|预计费用|


示例：


Day1

上午：
景福宫

下午：
明洞购物

晚上：
弘大夜市



---

# 4.4 地点信息表 pois


作用：

保存景点、餐厅、酒店等 POI 信息。


POI：

Point Of Interest


|字段|类型|说明|
|-|-|-|
|id|BIGINT|地点ID|
|name|VARCHAR(100)|名称|
|type|VARCHAR(50)|类型|
|address|VARCHAR(255)|地址|
|city|VARCHAR(50)|城市|
|latitude|DECIMAL(10,7)|纬度|
|longitude|DECIMAL(10,7)|经度|
|description|TEXT|介绍|
|image_url|VARCHAR(255)|图片地址|
|created_at|DATETIME|创建时间|


设计原因：

避免数据重复。


错误设计：


计划A:
景福宫
地址
经纬度

计划B:
景福宫
地址
经纬度



正确设计：

          POI数据库

             |
    ----------------

计划A引用

计划B引用



---

# 4.5 收藏表 favorites


作用：

保存用户收藏的旅行方案。


|字段|类型|说明|
|-|-|-|
|id|BIGINT|收藏ID|
|user_id|BIGINT|用户ID|
|plan_id|BIGINT|旅行计划ID|
|created_at|DATETIME|收藏时间|


设计说明：

TripMind 是旅行计划软件。

用户收藏的是：


完整旅行计划


而不是：


单独景点



---

# 4.6 AI聊天记录表 chat_history


作用：

保存用户和 AI 的历史对话。


|字段|类型|说明|
|-|-|-|
|id|BIGINT|聊天ID|
|user_id|BIGINT|用户ID|
|role|VARCHAR(20)|角色|
|content|TEXT|聊天内容|
|created_at|DATETIME|创建时间|


示例：

用户：


帮我修改第三天路线



AI：


已经调整第三天行程



保存后：

未来 AI Agent 可以基于历史记录优化推荐。


---

# 5. 数据库关系说明


## User 与 TravelPlan

关系：


User 1 : N TravelPlan



一个用户可以创建多个旅行计划。


---

## TravelPlan 与 Itinerary


关系：


TravelPlan 1 : N Itinerary



一个旅行计划包含多个行程。


---

## Itinerary 与 POI


关系：


Itinerary N : 1 POI



多个行程可以引用同一个地点。


---

## User 与 Favorite


关系：


User 1 : N Favorite



用户可以收藏多个旅行方案。


---

# 6. 索引设计规划


后续开发增加：

## 用户邮箱索引


users.email



用途：

快速登录查询。


---

## 旅行计划用户索引


travel_plans.user_id



用途：

快速查询用户旅行记录。


---

## POI城市索引


pois.city



用途：

快速搜索城市景点。


---

# 7. 后续扩展设计


## AI Agent 用户画像


新增：


user_preferences



保存：

- 喜欢城市
- 喜欢美食类型
- 消费水平
- 旅行习惯


---

## 酒店系统


新增：


hotels



保存：

- 酒店信息
- 价格
- 评分


---

## 订单系统


未来接入：

- 机票
- 酒店
- 门票


形成：

AI Travel Agent 商业闭环。


---

# 8. 当前版本总结


当前数据库版本：

v1.0


支持功能：

✅ 用户系统

✅ AI旅行计划保存

✅ 行程管理

✅ POI管理

✅ 收藏旅行方案

✅ AI聊天记录


未来支持：

✅ AI Agent

✅ 用户长期记忆

✅ 酒店/机票服务

✅ 商业化旅行服务


---
