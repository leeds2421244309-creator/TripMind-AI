from enum import Enum

class PaymentStatus(str, Enum):
    PAID = "PAID"
    PENDING = "PENDING"
    UNDECIDED = "UNDECIDED"
    CANCELLED = "CANCELLED"