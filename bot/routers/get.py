import io

from aiogram import F, Router
from aiogram.types import Message, BufferedInputFile
from aiogram.types.input_file import BufferedInputFile
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
    file_bytes = await response.read()
    file_data = io.BytesIO(file_bytes)

    file_data.seek(0)

    document = BufferedInputFile(file_data.getvalue(), filename="expenses.xlsx")
    await message.answer_document(document, caption="Here is your expense report")

    await state.clear()