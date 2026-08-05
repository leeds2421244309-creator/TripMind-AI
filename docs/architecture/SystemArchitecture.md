# TripMind AI System Architecture


## 1. Overview


TripMind AI adopts a modern full-stack architecture based on:

- Frontend
- Backend
- AI Service
- Database
- External Services


The system follows a frontend-backend separation architecture.


The overall architecture:


```
                    User

                      |

                      ↓


              Vue3 Web Application

                      |

                HTTP REST API

                      |

                      ↓


              FastAPI Backend

                      |

        --------------------------------

        |              |               |

        ↓              ↓               ↓


   AI Service      Database        External APIs

   LLM API          MySQL          AMap SDK


```

---

# 2. Architecture Layers


## 2.1 Frontend Layer


Technology:

- Vue3
- TypeScript
- Vite
- Pinia
- Axios


Responsibilities:

- User interface
- User interaction
- Travel plan visualization
- Map display
- Data management


Main Modules:


```
frontend/

├── views/

│   ├── Home

│   ├── GeneratePlan

│   ├── TravelDetail

│   ├── Map

│   └── Profile


├── components/

├── stores/

└── api/

```


---

# 2.2 Backend Layer


Technology:

- Python
- FastAPI
- SQLAlchemy


Responsibilities:


- Business logic
- User management
- Travel plan management
- AI service integration
- Data processing


Main Modules:


```
backend/


├── api/

├── services/

├── models/

├── schemas/

├── database/

└── utils/

```


---

# 2.3 AI Service Layer


Technology:

- LLM API
- Prompt Engineering


Responsibilities:


## Requirement Analysis


Analyze user input:


Example:


```
"I want a cheap Seoul trip during winter vacation"

```


Extract:


- Destination
- Budget
- Travel style
- Preferences



---


## Travel Plan Generation


Generate:


- Daily itinerary
- Attractions
- Transportation
- Budget estimation



---


## AI Plan Validation


After generation:


Check:


- Whether requirements are satisfied
- Whether conflicts exist
- Optimization suggestions



Workflow:


```
User Requirement

↓

Requirement Analyzer

↓

Plan Generator

↓

Plan Validator

↓

Final Result

```


---

# 2.4 Database Layer


Technology:


MySQL


Responsibilities:


Store:


- User information
- Travel plans
- Travel records
- AI validation results



---

# 2.5 External Service Layer


## AMap SDK


Used for:


- Location search
- Map display
- Route visualization
- Marker rendering



## LLM API


Used for:


- AI generation
- AI assistant
- Requirement validation



---

# 3. System Data Flow


## Travel Plan Generation Flow


```
User

↓

Frontend

↓

FastAPI API

↓

Requirement Analyzer

↓

LLM API

↓

Travel Plan Generator

↓

Database Storage

↓

Frontend Display

```



---

## AI Validation Flow


```
Generated Travel Plan

↓

Validation Service

↓

Compare User Requirements

↓

Generate Evaluation Report

↓

Display Results

```


---

# 4. Future Architecture Expansion


Future versions may introduce:


## AI Agent Layer


Responsible for:


- Hotel searching
- Flight recommendation
- Ticket services
- Automatic itinerary adjustment



Architecture evolution:


```

Current:


User

↓

AI Assistant

↓

Generate Plan



Future:


User

↓

AI Travel Agent

↓

Planning

↓

Booking

↓

Adjustment


```


---

# 5. Design Principles


## Separation of Concerns


Each module has independent responsibilities.


Frontend:

Focus on user experience.


Backend:

Focus on business logic.


AI:

Focus on intelligent processing.


Database:

Focus on data persistence.



---

## Scalability


The architecture supports future expansion:


- Multiple AI models
- More travel services
- More external APIs
- Mobile applications


---

# Summary


TripMind AI uses a modern full-stack architecture combining:

- Vue3 frontend
- FastAPI backend
- MySQL database
- LLM AI services
- AMap SDK


The architecture is designed not only for MVP development but also for future AI Travel Agent expansion.
