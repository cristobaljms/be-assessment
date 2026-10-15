from app.domain.customer import (
    CustomerNotFoundError,
    CustomerStatus,
    DuplicateCustomerEmailError,
)
from app.models.customer import Customer
from app.repositories.customer import CustomerRepository
from app.schemas.customer import CustomerCreate


class CustomerService:
    def __init__(self, repository: CustomerRepository) -> None:
        self._repository = repository

    def create(self, customer_data: CustomerCreate) -> Customer:
        normalized_email = str(customer_data.email).lower()
        if self._repository.get_by_email(normalized_email) is not None:
            raise DuplicateCustomerEmailError(normalized_email)

        return self._repository.create(name=customer_data.name, email=normalized_email)

    def list(self, status: CustomerStatus | None = None) -> list[Customer]:
        return self._repository.list(status)

    def get(self, customer_id: int) -> Customer:
        customer = self._repository.get_by_id(customer_id)
        if customer is None:
            raise CustomerNotFoundError(customer_id)
        return customer

    def update_status(self, customer_id: int, status: CustomerStatus) -> Customer:
        customer = self.get(customer_id)
        return self._repository.update_status(customer, status)
