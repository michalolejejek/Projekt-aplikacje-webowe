from fastapi import APIRouter, HTTPException

from customers.storage import get_customers_storage
from customers.schema import CustomerCreateSchema, CustomerUpdateSchema, Customer

router = APIRouter()

CUSTOMERS_STORAGE = get_customers_storage()


@router.get("/")
async def get_customers() -> list[Customer]:
    return list(CUSTOMERS_STORAGE.values())


@router.get("/{customer_id}")
async def get_customer(customer_id: int) -> Customer:
    try:
        return CUSTOMERS_STORAGE[customer_id]
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f"Customer with ID={customer_id} does not exist."
        )


@router.post("/")
async def create_customer(customer: CustomerCreateSchema) -> Customer:
    customer_id = len(CUSTOMERS_STORAGE) + 1
    new_customer = Customer(id=customer_id, **customer.dict())
    CUSTOMERS_STORAGE[customer_id] = new_customer
    return new_customer


@router.put("/{customer_id}")
async def update_customer(
    customer_id: int, updated_customer: CustomerUpdateSchema
) -> Customer:
    if customer_id not in CUSTOMERS_STORAGE:
        raise HTTPException(
            status_code=404, detail=f"Customer with ID={customer_id} does not exist."
        )
    customer = CUSTOMERS_STORAGE[customer_id]
    update_data = updated_customer.dict(exclude_unset=True)
    updated_customer = customer.copy(update=update_data)
    CUSTOMERS_STORAGE[customer_id] = updated_customer
    return updated_customer


@router.delete("/{customer_id}")
async def delete_customer(customer_id: int) -> None:
    if customer_id not in CUSTOMERS_STORAGE:
        raise HTTPException(
            status_code=404, detail=f"Customer with ID={customer_id} does not exist."
        )
    del CUSTOMERS_STORAGE[customer_id]
