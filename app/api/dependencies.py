from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.repositories.customer import CustomerRepository
from app.services.customer import CustomerService

SessionDep = Annotated[Session, Depends(get_db_session)]


def get_customer_service(session: SessionDep) -> CustomerService:
    return CustomerService(CustomerRepository(session))


CustomerServiceDep = Annotated[CustomerService, Depends(get_customer_service)]
