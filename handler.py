from typing import Annotated

from sqlmodel import select, func, extract
from fastapi import Query, APIRouter

from model import Expense
from db import SessionDep
from model import ExpenseCreate, ExpenseRead

expense_router = APIRouter()


@expense_router.post("/expenses/", response_model=ExpenseRead)
def create_expense(expense: ExpenseCreate, session: SessionDep):
    db_expense = Expense.model_validate(expense)
    session.add(db_expense)
    session.commit()
    session.refresh(db_expense)
    return db_expense


@expense_router.get("/expenses/", response_model=list[ExpenseRead])
def list_expenses(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    expenses = session.exec(select(Expense).offset(offset).limit(limit)).all()
    return expenses


@expense_router.get("/expenses/month/{year}/{month}/", response_model=list[ExpenseRead])
def filter_expenses(session: SessionDep, year: int, month: int):
    expenses = session.exec(
        select(Expense).where(
            extract("year", Expense.created_date) == year,
            extract("month", Expense.created_date) == month,
        )
    ).all()

    return expenses


@expense_router.get("/total/")
def expense_total(session: SessionDep):
    total_exp = session.exec(select(func.sum(Expense.amount))).one() or 0

    total_sal = (
        session.exec(
            select(func.sum(Expense.amount)).where(Expense.category == "salary")
        ).one()
        or 0
    )

    rem_amt = total_exp - total_sal

    return {
        "total_expense": total_exp,
        "total_salary": total_sal,
        "remaining_amt": rem_amt,
    }
