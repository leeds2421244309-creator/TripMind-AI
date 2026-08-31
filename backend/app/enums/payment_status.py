from enum import Enum

class PaymentStatus(str, Enum):
    PAID = "paid"
    PENDING = "pending"
    UNDECIDED = "undecided"
    CANCELLED = "cancelled"