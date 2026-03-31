from enum import StrEnum
from datetime import date, datetime

from sqlmodel import Field, SQLModel
from pydantic import StrictStr


class CategoryEnum(StrEnum):
    SALARY = "salary"
    FOOD = "food"
    TRANSPORT = "transport"
    RENT = "rent"
    UTILITIES = "utilities"
    OTHER = "other"


class ExpenseBase(SQLModel):
    name: StrictStr = Field(min_length=1)
    amount: float = Field(gt=0)
    category: CategoryEnum


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(ExpenseBase):
    name: StrictStr | None = None
    amount: float | None = Field(default=None, gt=0)
    category: CategoryEnum | None = None


class ExpenseRead(ExpenseBase):
    id: int
    expense_date: date
    created_at: datetime
    updated_at: datetime


class TotalResponse(SQLModel):
    total_expense: float
    total_salary: float
    remaining_amt: float
