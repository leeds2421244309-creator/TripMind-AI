# TripMind AI Database Design


## 1. Database Overview


Database:

MySQL


ORM:

SQLAlchemy


The database is designed to support:

- User management
- AI travel plan generation
- Itinerary management
- Map location data
- AI plan validation
- Travel memories


---

# 2. Entity Relationship Overview


```
User

 |

 |

 └── TravelPlan

          |

          |

          ├── Itinerary

          |

          ├── ValidationResult

          |

          └── TravelMemory


Place

 |

 |

Itinerary

```


---

# 3. Database Tables


# 3.1 User Table


Table:

```
users
```


Purpose:

Store user basic information.



| Field | Type | Description |
|-|-|-|
| id | BIGINT | Primary Key |
| username | VARCHAR | Username |
| email | VARCHAR | Email |
| password_hash | VARCHAR | Password |
| avatar | VARCHAR | Avatar URL |
| created_at | DATETIME | Creation time |


---

# 3.2 Travel Plan Table


Table:

```
travel_plans
```


Purpose:

Store AI generated travel plans.


| Field | Type | Description |
|-|-|-|
| id | BIGINT | Primary Key |
| user_id | BIGINT | User ID |
| title | VARCHAR | Plan title |
| destination | VARCHAR | Destination |
| start_date | DATE | Start date |
| days | INT | Travel days |
| budget | DECIMAL | Budget |
| travel_style | VARCHAR | Travel style |
| status | VARCHAR | Plan status |
| created_at | DATETIME | Creation time |



Example:


```
Seoul 7 Days Student Trip

Budget: 4000 RMB

Style: Photography + Food

```


---

# 3.3 Itinerary Table


Table:

```
itineraries
```


Purpose:

Store daily travel schedules.


| Field | Type | Description |
|-|-|-|
| id | BIGINT | Primary Key |
| plan_id | BIGINT | Travel plan ID |
| day_number | INT | Day |
| time_period | VARCHAR | Morning/Afternoon/Evening |
| place_id | BIGINT | Place ID |
| activity | TEXT | Activity description |
| transportation | VARCHAR | Transportation |
| estimated_cost | DECIMAL | Cost |



Example:


```
Day 1

Morning:

Visit Gyeongbokgung Palace


Transportation:

Subway


Cost:

100 RMB

```


---

# 3.4 Place Table


Table:

```
places
```


Purpose:

Store location information for maps.



| Field | Type | Description |
|-|-|-|
| id | BIGINT | Primary Key |
| name | VARCHAR | Place name |
| address | VARCHAR | Address |
| latitude | DECIMAL | Latitude |
| longitude | DECIMAL | Longitude |
| category | VARCHAR | Attraction/Food/Hotel |



Used for:

- AMap Marker
- Route display
- Location search


---

# 3.5 Validation Result Table


Table:

```
validation_results
```


Purpose:

Store AI Plan Validation results.


| Field | Type | Description |
|-|-|-|
| id | BIGINT | Primary Key |
| plan_id | BIGINT | Travel plan ID |
| match_score | INT | Matching score |
| satisfied_items | JSON | Satisfied requirements |
| partial_items | JSON | Partial matches |
| failed_items | JSON | Failed requirements |
| suggestions | TEXT | AI suggestions |
| created_at | DATETIME | Creation time |



Example:


```
Match Score:

85%


Failed:

Luxury hotel under 300 RMB


Suggestion:

Increase hotel budget


```


---

# 3.6 Travel Memory Table


Table:

```
travel_memories
```


Purpose:

Store travel records after completion.


| Field | Type | Description |
|-|-|-|
| id | BIGINT | Primary Key |
| user_id | BIGINT | User ID |
| plan_id | BIGINT | Related plan |
| content | TEXT | Diary content |
| media_url | VARCHAR | Photo/video |
| location | VARCHAR | Location |
| weather | VARCHAR | Weather |
| created_at | DATETIME | Creation time |



---

# 4. Database Relationships


## User - TravelPlan


One user can create multiple travel plans.


```
User 1 ---- N TravelPlan

```


---

## TravelPlan - Itinerary


One travel plan contains multiple daily schedules.


```
TravelPlan 1 ---- N Itinerary

```


---

## TravelPlan - ValidationResult


One travel plan has validation results.


```
TravelPlan 1 ---- 1 ValidationResult

```


---

## TravelPlan - TravelMemory


One travel plan can generate travel memories.


```
TravelPlan 1 ---- N TravelMemory

```


---

# 5. Future Database Expansion


Future AI Travel Agent version may add:


## Hotel Table


Store:

- Hotel information
- Price
- Rating
- Location


---

## Flight Table


Store:

- Flight information
- Price
- Schedule


---

## User Preference Table


Store:

- Travel habits
- Favorite destinations
- Budget preference


---

# 6. Database Design Principles


## Data Normalization


Separate different entities:

- User
- Plan
- Place
- Memory


Avoid duplicate data.


---

## Scalability


Database design supports future expansion:

- Booking system
- Recommendation system
- AI preference learning


---

# Summary


TripMind AI database is designed around the complete travel lifecycle:


```
Travel Idea

↓

Travel Plan

↓

Daily Itinerary

↓

Travel Execution

↓

Travel Memory

```


The database structure supports the current MVP and future AI Travel Agent development.
