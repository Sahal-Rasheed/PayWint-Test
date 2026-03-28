from datetime import date

from sqlmodel import Field, SQLModel


class ExpenseBase(SQLModel):
    name: str = Field(index=True)
    amount: float = Field(index=True)
    category: str


class Expense(ExpenseBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_date: date = Field(default_factory=date.today)


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseRead(ExpenseBase):
    id: int
    created_date: date
