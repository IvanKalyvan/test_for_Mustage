from datetime import datetime
from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from expenses.models import Expenses
from expenses.schemas import ExpenseCreate
from expenses.utils import get_usd_uah_rate, create_excel_file

async def create_expense(session, expense: ExpenseCreate):

    try:

        usd = await get_usd_uah_rate()

        data = expense.dict()

        data["expensesUSD"] = round(data["expensesUAH"] / usd, 2)

        stmt = insert(Expenses).values(
            title=data["title"],
            inUAH=data["expensesUAH"],
            inUSD=data["expensesUSD"],
        )

        await session.execute(stmt)
        await session.commit()

        return {"status": "success", "message": "Expense successfully added!"}

    except SQLAlchemyError as e:

        await session.rollback()
        return {"status": "error", "message": f"Database error: {str(e)}"}

    except Exception as e:

        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


async def get_expenses(start_date: str, end_date: str, session):
    try:

        start_date = datetime.strptime(start_date, "%d.%m.%Y")
        end_date = datetime.strptime(end_date, "%d.%m.%Y")

        query = select(Expenses).where(Expenses.c.createdAt.between(start_date, end_date))
        result = await session.execute(query)
        expenses = result.mappings()

        excel_file = create_excel_file(expenses)

        return excel_file

    except SQLAlchemyError as e:

        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:

        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


async def delete_expense(session, expense_id: int):
    try:

        stmt = delete(Expenses).where(Expenses.c.id == expense_id)
        result = await session.execute(stmt)
        await session.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Expense not found")

        return {"status": "success", "message": "Expense successfully deleted!"}

    except SQLAlchemyError as e:

        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:

        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

async def update_expense(expense_data, session):
    try:

        expense_data_id = expense_data.id
        expense_data = expense_data.dict()
        update_data = expense_data.copy()

        for item in expense_data:
            if expense_data[item] is None:
                del update_data[item]

        if update_data.get("inUAH"):
            update_data["inUSD"] = round(update_data["inUAH"] / await get_usd_uah_rate(), 2)

        stmt = update(Expenses).where(Expenses.c.id == expense_data_id).values(update_data)
        await session.execute(stmt)
        await session.commit()

        return {"status": "success", "message": "Expense successfully updated!"}

    except Exception as e:

        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")