-- ==========================================
-- TripMind AI
-- schema.sql
-- 数据库表结构
-- ==========================================

USE tripmind;

-- ===========================
-- 1. 用户表
-- ===========================

CREATE TABLE IF NOT EXISTS users (

    id BIGINT PRIMARY KEY AUTO_INCREMENT,

    username VARCHAR(50) NOT NULL,

    email VARCHAR(100) NOT NULL UNIQUE,

    password_hash VARCHAR(255) NOT NULL,

    avatar VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ===========================
-- 2. 旅行计划
-- ===========================

CREATE TABLE IF NOT EXISTS travel_plans (

    id BIGINT PRIMARY KEY AUTO_INCREMENT,

    user_id BIGINT NOT NULL,

    title VARCHAR(100) NOT NULL,

    destination VARCHAR(100) NOT NULL,

    departure_city VARCHAR(100),

    start_date DATE,

    days INT NOT NULL,

    budget DECIMAL(10,2),

    travelers INT DEFAULT 1,

    interests TEXT,

    transportation VARCHAR(50),

    status ENUM('draft','generated','completed')
        DEFAULT 'draft',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_plan_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ===========================
-- 3. 每日行程
-- ===========================

CREATE TABLE IF NOT EXISTS itinerary_days (

    id BIGINT PRIMARY KEY AUTO_INCREMENT,

    plan_id BIGINT NOT NULL,

    day_number INT NOT NULL,

    morning TEXT,

    afternoon TEXT,

    evening TEXT,

    estimated_cost DECIMAL(10,2),

    transportation VARCHAR(100),

    notes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_day_plan
        FOREIGN KEY (plan_id)
        REFERENCES travel_plans(id)
        ON DELETE CASCADE

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ===========================
-- 4. 景点
-- ===========================

CREATE TABLE IF NOT EXISTS itinerary_pois (

    id BIGINT PRIMARY KEY AUTO_INCREMENT,

    day_id BIGINT NOT NULL,

    poi_name VARCHAR(200) NOT NULL,

    latitude DECIMAL(10,7),

    longitude DECIMAL(10,7),

    address VARCHAR(255),

    visit_order INT,

    stay_minutes INT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_poi_day
        FOREIGN KEY (day_id)
        REFERENCES itinerary_days(id)
        ON DELETE CASCADE

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ===========================
-- 5. 收藏
-- ===========================

CREATE TABLE IF NOT EXISTS favorites (

    id BIGINT PRIMARY KEY AUTO_INCREMENT,

    user_id BIGINT NOT NULL,

    plan_id BIGINT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_favorite_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_favorite_plan
        FOREIGN KEY (plan_id)
        REFERENCES travel_plans(id)
        ON DELETE CASCADE,

    UNIQUE KEY uk_favorite(user_id, plan_id)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ===========================
-- 6. AI聊天记录
-- ===========================

CREATE TABLE IF NOT EXISTS chat_history (

    id BIGINT PRIMARY KEY AUTO_INCREMENT,

    user_id BIGINT NOT NULL,

    role ENUM('user','assistant') NOT NULL,

    message TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_chat_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ===========================
-- 索引
-- ===========================

CREATE INDEX idx_plan_user
ON travel_plans(user_id);

CREATE INDEX idx_plan_destination
ON travel_plans(destination);

CREATE INDEX idx_day_plan
ON itinerary_days(plan_id);

CREATE INDEX idx_poi_day
ON itinerary_pois(day_id);

CREATE INDEX idx_chat_user
ON chat_history(user_id);