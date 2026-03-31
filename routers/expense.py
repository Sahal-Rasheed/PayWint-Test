from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query, Response, status

from database import SessionDep
from schemas.expense import ExpenseCreate, ExpenseRead, ExpenseUpdate, TotalResponse
from services.expense import (
    create_expense,
    delete_expense,
    expense_total,
    filter_expenses,
    get_expense,
    list_expenses,
    update_expense,
)

expense_router = APIRouter()


@expense_router.post(
    "/expenses/",
    status_code=status.HTTP_201_CREATED,
    response_model=ExpenseRead,
    summary="Create expense",
    description="Create a new expense entry.",
)
def create_expense_api(expense: ExpenseCreate, session: SessionDep) -> ExpenseRead:
    return create_expense(session=session, expense=expense)


@expense_router.get(
    "/expenses/",
    status_code=status.HTTP_200_OK,
    response_model=list[ExpenseRead],
    summary="List expenses",
    description="List expenses with pagination.",
)
def list_expenses_api(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[ExpenseRead]:
    return list_expenses(session=session, offset=offset, limit=limit)


@expense_router.get(
    "/expenses/{expense_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ExpenseRead,
    summary="Get expense",
    description="Get a single expense by id.",
)
def get_expense_api(session: SessionDep, expense_id: int) -> ExpenseRead:
    expense = get_expense(session=session, expense_id=expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@expense_router.put(
    "/expenses/{expense_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ExpenseRead,
    summary="Update expense",
    description="Partially update an expense by id.",
)
def update_expense_api(
    session: SessionDep, expense: ExpenseUpdate, expense_id: int
) -> ExpenseRead:
    expense = update_expense(session=session, expense=expense, expense_id=expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@expense_router.delete(
    "/expenses/{expense_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete expense",
    description="Delete an expense by id.",
)
def delete_expense_api(session: SessionDep, expense_id: int) -> Response:
    delete_expense(session=session, expense_id=expense_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@expense_router.get(
    "/expenses/month/{year}/{month}/",
    response_model=list[ExpenseRead],
    summary="Filter expenses by month",
    description="Return expenses for a given year and month.",
)
def filter_expenses_api(
    session: SessionDep,
    year: Annotated[int, Path(ge=1900, le=3000)],
    month: Annotated[int, Path(ge=1, le=12)],
) -> list[ExpenseRead]:
    expenses = filter_expenses(session=session, year=year, month=month)
    return expenses


@expense_router.get(
    "/total/",
    response_model=TotalResponse,
    summary="Expense totals",
    description="Get total expense, salary total, and remaining amount.",
)
def expense_total_api(session: SessionDep) -> TotalResponse:
    return expense_total(session=session)
