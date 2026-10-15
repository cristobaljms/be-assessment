from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.domain.customer import CustomerNotFoundError, DuplicateCustomerEmailError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(CustomerNotFoundError)
    def handle_customer_not_found(
        _request: Request,
        error: CustomerNotFoundError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": f"Customer {error.customer_id} was not found."},
        )

    @app.exception_handler(DuplicateCustomerEmailError)
    def handle_duplicate_customer_email(
        _request: Request,
        _error: DuplicateCustomerEmailError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "A customer with this email already exists."},
        )
