from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.domain.customer import CustomerStatus, DuplicateCustomerEmailError
from app.models.customer import Customer


class CustomerRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, customer_id: int) -> Customer | None:
        return self._session.get(Customer, customer_id)

    def get_by_email(self, email: str) -> Customer | None:
        statement = select(Customer).where(Customer.email == email)
        return self._session.scalar(statement)

    def list(self, status: CustomerStatus | None = None) -> list[Customer]:
        statement = select(Customer)
        if status is not None:
            statement = statement.where(Customer.status == status)

        statement = statement.order_by(Customer.created_at.desc(), Customer.id.desc())
        return list(self._session.execute(statement).scalars().all())

    def create(self, *, name: str, email: str) -> Customer:
        customer = Customer(name=name, email=email, status=CustomerStatus.PENDING)
        self._session.add(customer)

        try:
            self._session.commit()
        except IntegrityError as error:
            self._session.rollback()
            raise DuplicateCustomerEmailError(email) from error

        self._session.refresh(customer)
        return customer

    def update_status(self, customer: Customer, status: CustomerStatus) -> Customer:
        customer.status = status
        self._session.commit()
        self._session.refresh(customer)
        return customer
