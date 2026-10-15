from enum import StrEnum


class CustomerStatus(StrEnum):
    ACTIVE = "ACTIVE"
    PENDING = "PENDING"
    BLOCKED = "BLOCKED"


class CustomerNotFoundError(Exception):
    def __init__(self, customer_id: int) -> None:
        self.customer_id = customer_id
        super().__init__(f"Customer {customer_id} was not found")


class DuplicateCustomerEmailError(Exception):
    def __init__(self, email: str) -> None:
        self.email = email
        super().__init__(f"Customer email {email} already exists")
