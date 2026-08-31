from enum import Enum


class BookingType(str, Enum):
    HOTEL = "hotel"
    RESTAURANT = "restaurant"

    FLIGHT = "flight"
    TRAIN = "train"
    BUS = "bus"
    FERRY = "ferry"