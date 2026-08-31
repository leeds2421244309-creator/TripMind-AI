# TripMind-AI

## AI Travel Decision & Execution Assistant

面向18-25岁大学生用户的智能旅行规划助手。

不同于传统AI聊天式旅行规划，TripMind-AI通过「需求分析 + 预算决策 + 可行性检测 + AI规划 + 执行管理」帮助用户完成从旅行想法到真实出行的全过程。

---

# 项目背景

目前市场上的旅行AI主要解决：

* 根据地点生成旅行攻略
* 推荐景点
* 自动生成行程

但真实旅行过程中，用户面对的问题更加复杂：

* 预算是否足够？
* 景点是否合理？
* 酒店位置是否适合？
* 演唱会结束是否有交通？
* 是否需要提前办理证件？
* 是否遗漏重要物品？
* 计划变化后如何重新调整？

TripMind-AI希望解决的是：

> 从“我要去哪里”到“我安全顺利完成旅行”的完整流程。

---

# 核心理念

## AI不是替用户决定旅行

而是：

```
用户做决策
+
系统提供分析
+
AI辅助优化
+
程序保障执行
```

---

# 产品流程

## Step1 用户旅行目标

用户输入：

* 目的地
* 出发地
* 时间
* 人数
* 旅行目的

例如：

```
深圳 → 香港

目标：
观看TXT演唱会
体验香港旅游
预算5000元
```

---

# Step2 大开支决策

用户优先确定：

## 预算模块 Budget Engine

包括：

* 交通预算
* 酒店预算
* 餐饮预算
* 景点预算
* 购物预算

系统自动计算：

* 当前预算是否合理
* 是否存在明显冲突

例如：

```
预算3000

已选择：

香港迪士尼 600
演唱会VR 300
酒店1000
交通500

剩余预算不足

建议：
A 删除非核心项目
B 增加预算
C 调整住宿
```

---

# Step3 吃住行偏好确定

## 住宿分析

用户可以：

方式1：
AI推荐酒店

方式2：
用户填写酒店

方式3：
上传酒店截图

AI分析：

* 地址
* 距离景点
* 交通便利程度
* 是否适合晚归
* 是否支持寄存

输出提醒：

```
演唱会预计22:30结束

酒店距离场馆45分钟

建议确认：
最后一班交通时间
```

---

# Step4 交通规划

交通分为：

## 大交通

城市之间：

* 飞机
* 高铁
* 火车
* 船

## 小交通

城市内部：

* 地铁
* 公交
* 步行

系统结合：

* 地图API
* 交通规则
* 用户偏好

生成：

* 推荐路线
* 时间
* 费用
* 换乘信息

---

# Step5 AI生成旅行计划

AI输入：

不是简单地点。

而是：

```
用户目标
+
预算约束
+
酒店信息
+
交通方式
+
已确定项目
+
个人偏好
```

生成：

* 每日路线
* 时间安排
* 景点顺序
* 费用估算

---

# Step6 行前执行清单

旅行计划生成后：

自动生成：

## Day-15

* 港澳通行证检查
* 签注提醒

## Day-7

* 检查酒店订单
* 下载地图
* 准备证件

## Day-1

* 收拾行李
* 手机充电
* 现金准备

支持：

* Todo List
* 分类管理
* 添加提醒

---

# Step7 行程执行

旅行过程中：

提供：

* 地图展示
* 实时位置
* 当前任务
* 下一站提醒

例如：

```
14:00

前往香港迪士尼

预计:
地铁35分钟

提醒:
建议提前购买门票
```

---

# AI能力模块

## Travel Planner

旅行计划生成

## Travel QA

旅行问答

## Route Optimizer

路线优化

## Diary Writer

旅行日记生成

---

# 系统架构

## Backend

FastAPI

负责：

* 用户系统
* AI接口
* 业务逻辑
* 数据管理

## AI Layer

负责：

* Prompt Engineering
* 旅行规划
* 信息理解

## Rule Engine

负责：

* 预算计算
* 冲突检测
* 时间检查
* 提醒生成

## Map Layer

负责：

* POI搜索
* 路线展示
* 距离计算

---

# 技术栈

Frontend:

* Vue3
* TypeScript
* Vite
* Pinia

Backend:

* FastAPI
* SQLAlchemy
* MySQL

AI:

* Qwen API
* Prompt Engineering

Map:

* 高德地图API

---

# 核心创新

1. 从AI生成旅行转向旅行执行管理

2. AI与规则引擎结合

3. 针对大学生场景优化：

* 学生优惠
* 预算限制
* 证件提醒
* 演唱会旅行
* 港澳日韩东南亚出行

---

# Development Progress

Day1-Day10:

完成：

* 项目架构
* 用户系统
* JWT认证
* AI旅行生成
* Prompt设计

Day11-Day13:

开发：

* 高德地图接入
* POI搜索
* 路线能力

后续：

* Budget Engine
* 行程可行性检测
* Todo系统
* 行程执行模式
* AI Agent升级


# 🌍 TripMind AI

> An AI-powered travel companion for university students.

TripMind AI is an enterprise-level AI Travel Companion designed for university students.

TripMind AI is an educational and portfolio project designed to explore how modern AI technologies can be integrated into a complete travel assistant through an enterprise-level software engineering workflow.

It accompanies users throughout the entire travel lifecycle—from travel planning and itinerary generation to real-time travel assistance and travel memory management.

The long-term vision of TripMind AI is to evolve into an AI Travel Agent capable of completing real travel tasks on behalf of users.

Unlike traditional itinerary generators, TripMind AI focuses on the complete travel experience rather than simply generating itineraries.

It helps users before traveling, supports them during the journey, and preserves valuable memories after the trip.
---

## 📌 Project Background

Nowadays, travelers often need to search information across multiple platforms:

- Xiaohongshu
- Zhihu
- Bilibili
- Google
- Map applications
- Hotel platforms

Users spend a lot of time collecting and organizing information.

TripMind AI aims to simplify this process by using AI technology to provide personalized travel planning and intelligent travel assistance.

---

## ✨ Core Features

### AI Travel Planning

Generate personalized travel plans based on:

- Destination
- Travel dates
- Budget
- Interests
- Transportation preferences


### Smart Route Planning

Provide:

- Daily itinerary
- Attraction recommendations
- Transportation suggestions
- Map visualization


### AI Travel Assistant

Future features:

- AI travel Q&A
- Image-based attraction recognition
- AI translation
- Travel guide


### Travel Records

Users can:

- Save travel plans
- Review previous trips
- Edit and regenerate itineraries


---

## 🛠 Tech Stack

### Frontend

- Vue3
- TypeScript
- Vite
- Pinia


### Backend

- FastAPI
- SQLAlchemy
- MySQL


### AI

- LLM API
- Prompt Engineering


### Map

- AMap SDK


---
## 🎯 Product Vision

TripMind AI is built around three development stages:

### AI Travel Planner (Version 1.0)

Generate personalized travel itineraries.

### AI Travel Companion (Version 1.x)

Accompany users before, during, and after every journey.

### AI Travel Agent (Version 2.0)

Help users complete real travel tasks such as hotel booking, flight booking, ticket purchasing, and itinerary management.


## 📂 Project Structure

```text
TripMind-AI

├── frontend
├── backend
├── docs
├── prompt
├── scripts
└── README.md
