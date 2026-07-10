from enum import Enum


class DisputeStatus(str, Enum):
    NEW = "new"
    INVESTIGATING = "investigating"
    APPROVED = "approved"
    DENIED = "denied"
    ERROR = "error"


class ShippingStatus(str, Enum):
    NO_TRACKING_NUMBER = "NO_TRACKING_NUMBER"
    DELIVERED = "DELIVERED"
    IN_TRANSIT = "IN_TRANSIT"
