import os
import sys

from fastapi import Depends, APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.database import get_session
from expenses.schemas import ExpenseCreate, ExpenseUpdate
from expenses.service import create_expense, get_expenses, delete_expense, update_expense

expenses = APIRouter(
    prefix="/expenses",
    tags=["expenses"]
)

@expenses.get("/")
async def read_expenses(start_date: str, end_date: str, db_session: AsyncSession = Depends(get_session)):

    excel_file = await get_expenses(start_date, end_date, db_session)

    return StreamingResponse(excel_file, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=expenses.xlsx"})

@expenses.post("/")
async def add_expense(expense: ExpenseCreate, db_session: AsyncSession = Depends(get_session)):
    db_expense = await create_expense(db_session, expense)
    return db_expense

@expenses.delete("/")
async def remove_expense(id: int, db_session: AsyncSession = Depends(get_session)):

    db_expense = await delete_expense(db_session, id)

    return db_expense

@expenses.patch("/")
async def edit_expense(expense: ExpenseUpdate, db_session: AsyncSession = Depends(get_session)):
    db_expense = await update_expense(expense, db_session)

    return db_expense