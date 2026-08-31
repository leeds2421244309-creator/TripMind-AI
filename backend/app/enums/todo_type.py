from enum import Enum


class TodoType(str, Enum):
    PREPARE = "prepare"        # 出发前准备
    TRAVEL_DAY = "travel_day"  # 出发当天事项
    REMINDER = "reminder"      # 行程提醒
    CUSTOM = "custom"          # 用户自定义事项