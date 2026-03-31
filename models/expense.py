from datetime import UTC, date, datetime

from sqlmodel import Field, SQLModel

from schemas.expense import CategoryEnum


class Expense(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    amount: float = Field(index=True)
    category: CategoryEnum
    expense_date: date = Field(default_factory=date.today)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
