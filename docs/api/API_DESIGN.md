# TripMind AI API Design

> Version: v1.0  
> Last Update: 2026-07-XX  
> Project: TripMind AI - AI Travel Agent

---

# 1. API Overview

TripMind AI 采用前后端分离架构：

- Frontend：Vue3 + TypeScript
- Backend：FastAPI
- AI Service：LLM API（通义千问）
- Map Service：高德地图 Web API
- Database：MySQL

系统主要接口：

| Module | Description |
|-|-|
| AI Planning API | AI生成旅行计划 |
| AI Chat API | 旅行智能问答 |
| POI Search API | 景点/酒店/餐厅搜索 |
| Route Planning API | 路线规划 |
| User API | 用户数据管理 |
| Favorite API | 收藏管理 |

---

# 2. API Architecture


```
Frontend(Vue3)
        |
        |
        ↓
Backend(FastAPI)
        |
        |
 ┌───────────────┐
 │               │
 ↓               ↓
LLM Service   Map Service

Qwen API      AMap API

```

---

# 3. AI Travel Planning API

## 3.1 Generate Trip Plan

根据用户输入生成完整旅行方案。


### Endpoint

```
POST /api/v1/travel/generate
```


### Request


```json
{
  "destination": "香港",
  "days": 3,
  "budget": 3000,
  "travelers": "情侣",
  "preferences": [
    "美食",
    "购物",
    "景点"
  ]
}
```


### Response


```json
{
  "success": true,
  "data": {
    "title": "香港三日旅行计划",
    "days": [
      {
        "day":1,
        "places":[
          {
            "name":"香港迪士尼",
            "description":"主题乐园游玩",
            "location":"114.0419,22.3129"
          }
        ]
      }
    ]
  }
}
```


---

# 4. AI Chat API

旅行过程中提供智能问答。


## Endpoint

```
POST /api/v1/chat
```


## Request


```json
{
  "message":"香港晚上有什么地方适合拍照？",
  "context":{
    "destination":"香港"
  }
}
```


## Response


```json
{
  "answer":
  "推荐维多利亚港、尖沙咀海滨..."
}
```

---

# 5. AMap POI Search API

用于搜索：

- 景点
- 酒店
- 餐厅
- 商场


## 5.1 Keyword Search


### Endpoint

```
GET /api/v1/map/poi/search
```


### Backend Request


```
keyword=迪士尼
city=香港
```


### Backend Call


```
GET

https://restapi.amap.com/v5/place/text

```


### Parameters


|参数|说明|
|-|-|
|key|高德API Key|
|keywords|搜索关键词|
|region|区域|
|page_size|返回数量|


### Response


```json
{
 "name":"香港迪士尼乐园",
 "location":
 "114.0419,22.3129",
 "address":
 "香港大屿山"
}
```


---

# 6. AMap Nearby Search API


用于推荐附近地点。


## Endpoint

```
GET /api/v1/map/poi/around
```


Example:


```
location=114.0419,22.3129

radius=3000

types=餐饮
```


返回：

```json
{
 "pois":[
  {
   "name":"附近餐厅",
   "distance":"500m"
  }
 ]
}
```


---

# 7. Route Planning API

用于生成旅行路线。


支持：

- 步行
- 驾车
- 公交
- 骑行


---

## 7.1 Driving Route


### Endpoint

```
GET /api/v1/map/route/driving
```


### Parameters


|参数|说明|
|-|-|
|origin|起点坐标|
|destination|终点坐标|
|strategy|路线策略|


Example:


```json
{
"origin":
"114.0419,22.3129",

"destination":
"114.1694,22.3193"
}
```


Response:


```json
{
"distance":"15000",
"duration":"1800",
"steps":[
 {
  "instruction":
  "沿道路行驶"
 }
]
}
```


---

# 8. Distance Calculation API


计算两个地点距离。


## Endpoint


```
GET /api/v1/map/distance
```


Request:


```json
{
"origin":
"114.0419,22.3129",

"destination":
"114.1694,22.3193"
}
```


Response:


```json
{
"distance":"12.5km",
"time":"30min"
}
```

---

# 9. User API


## User Login


```
POST /api/v1/user/login
```


Request:


```json
{
"email":"example@test.com",
"password":"******"
}
```


Response:


```json
{
"token":"xxxxx"
}
```


---

# 10. Favorite API


用户收藏旅行计划。


## Add Favorite


```
POST /api/v1/favorite
```


Request:


```json
{
"plan_id":10001
}
```


---

## Get Favorites


```
GET /api/v1/favorite/list
```


---

# 11. External API Integration


## 11.1 Qwen LLM API


Purpose:

AI旅行规划与问答。


Flow:


```
User Input

↓

Backend Prompt Assembly

↓

Qwen API

↓

JSON Travel Plan

↓

Frontend Display

```



---

## 11.2 AMap API


Purpose:

地图能力支持。


Used APIs:


|API|Function|
|-|-|
|POI Search|地点搜索|
|Around Search|周边推荐|
|Route Planning|路线规划|
|Distance API|距离计算|


---

# 12. Error Response


统一错误格式：


```json
{
 "success":false,
 "code":40001,
 "message":
 "Invalid parameter"
}
```


Error Code:


|Code|Description|
|-|-|
|40001|参数错误|
|40100|未授权|
|50000|服务器异常|
|50001|AI服务异常|
|50002|地图服务异常|

---

# 13. Future API Plan


- AI Agent 多步骤规划
- 实时天气接口
- 机票酒店接口
- 图片识别景点接口
- 多用户旅行协作
- 个性化推荐模型


---

# Summary

TripMind AI API 通过整合：

- LLM智能生成
- 高德地图服务
- POI搜索
- 路径规划

实现从：

> 用户需求输入 → AI旅行规划 → 地图路线 → 行程管理

的一站式智能旅行助手。
