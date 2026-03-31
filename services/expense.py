from fastapi import HTTPException
from sqlmodel import Session, func, select, update

from models.expense import Expense
from schemas.expense import ExpenseCreate, ExpenseUpdate


def create_expense(session: Session, expense: ExpenseCreate) -> Expense:
    try:
        expense_obj = Expense(**expense.model_dump())
        session.add(expense_obj)
        session.commit()
        session.refresh(expense_obj)
        return expense_obj
    except Exception:
        session.rollback()
        raise


def get_expense(session: Session, expense_id: int) -> Expense:
    expense = session.exec(
        select(Expense).where(Expense.id == expense_id)
    ).one_or_none()
    return expense


def list_expenses(session: Session, offset: int = 0, limit: int = 10) -> list[Expense]:
    expenses = session.exec(select(Expense).offset(offset).limit(limit)).all()
    return expenses


def update_expense(
    session: Session, expense: ExpenseUpdate, expense_id: int
) -> Expense:
    try:
        is_valid = get_expense(session, expense_id)
        if not is_valid:
            return None

        expense_obj = expense.model_dump(exclude_unset=True)

        expense = session.exec(
            update(Expense)
            .where(Expense.id == expense_id)
            .values(**expense_obj)
            .returning(Expense)
        )
        session.commit()
        return expense.scalar_one_or_none()
    except Exception:
        session.rollback()
        raise


def delete_expense(session: Session, expense_id: int) -> int:
    expense_obj = get_expense(session=session, expense_id=expense_id)
    if not expense_obj:
        raise HTTPException(status_code=404, detail="Expense not found")

    session.delete(expense_obj)
    session.commit()
    return 1


def filter_expenses(session: Session, year: int, month: int) -> list[Expense]:
    expenses = session.exec(
        select(Expense).where(
            func.extract("year", Expense.expense_date) == year,
            func.extract("month", Expense.expense_date) == month,
        )
    ).all()

    return expenses


def expense_total(session: Session) -> dict:
    total_exp = session.exec(select(func.sum(Expense.amount))).one() or 0
    total_sal = (
        session.exec(
            select(func.sum(Expense.amount)).where(Expense.category == "salary")
        ).one()
        or 0
    )
    rem_amt = total_exp - total_sal
    return {
        "total_expense": float(total_exp),
        "total_salary": float(total_sal),
        "remaining_amt": float(rem_amt),
    }
