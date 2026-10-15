from typing import Annotated

from fastapi import APIRouter, Path, Query, status

from app.api.dependencies import CustomerServiceDep
from app.domain.customer import CustomerStatus
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerRead, CustomerStatusUpdate

router = APIRouter(prefix="/customers", tags=["customers"])


def to_customer_read(customer: Customer) -> CustomerRead:
    return CustomerRead.model_validate(customer)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create a customer",
    responses={status.HTTP_409_CONFLICT: {"description": "Email already registered"}},
)
def create_customer(payload: CustomerCreate, service: CustomerServiceDep) -> CustomerRead:
    return to_customer_read(service.create(payload))


@router.get("", summary="List customers")
def list_customers(
    service: CustomerServiceDep,
    customer_status: Annotated[
        CustomerStatus | None,
        Query(alias="status", description="Filter customers by their current status"),
    ] = None,
) -> list[CustomerRead]:
    return [to_customer_read(customer) for customer in service.list(customer_status)]


@router.get(
    "/{customer_id}",
    summary="Get a customer",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Customer not found"}},
)
def get_customer(
    customer_id: Annotated[int, Path(ge=1)],
    service: CustomerServiceDep,
) -> CustomerRead:
    return to_customer_read(service.get(customer_id))


@router.patch(
    "/{customer_id}/status",
    summary="Update customer status",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Customer not found"}},
)
def update_customer_status(
    customer_id: Annotated[int, Path(ge=1)],
    payload: CustomerStatusUpdate,
    service: CustomerServiceDep,
) -> CustomerRead:
    return to_customer_read(service.update_status(customer_id, payload.status))
