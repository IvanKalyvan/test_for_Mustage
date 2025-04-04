import io

from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from api import get_expenses
from states.main import StatementOfExpenses

router = Router()

@router.message(F.text == "Отримати звіт витрат")
async def get_expense(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Enter the date from which to issue expenses")
    await state.set_state(StatementOfExpenses.start_date)

@router.message(StatementOfExpenses.start_date)
async def start_expense(message: Message, state: FSMContext):
    await state.update_data(start_date=message.text)
    await message.answer("Enter the date until which the expenses should be issued")
    await state.set_state(StatementOfExpenses.end_date)

@router.message(StatementOfExpenses.end_date)
async def end_expense(message: Message, state: FSMContext):
    await state.update_data(end_date=message.text)
    data_for_mailing = await state.get_data()
    response = await get_expenses("/expenses", data_for_mailing)
    print(response)
    file_bytes = await response.read()
    print(file_bytes)
    file_data = io.BytesIO(file_bytes)

    file_data.seek(0)

    await message.answer("Recorded!")
    await message.answer_document(file_data, caption="Here is your expense report")

    await state.clear()