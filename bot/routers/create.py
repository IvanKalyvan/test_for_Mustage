from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from api import post_expenses
from states.main import ExpenseForm

router = Router()

@router.message(F.text == "Додати статтю витрат")
async def create_expense(message: Message, state: FSMContext):

    await message.answer("Enter expense title")
    await state.set_state(ExpenseForm.title)

@router.message(ExpenseForm.title)
async def create_expense_title(message: Message, state: FSMContext):

    await state.update_data(title=message.text)
    await message.answer("Enter expense in UAH")
    await state.set_state(ExpenseForm.expensesUAH)

@router.message(ExpenseForm.expensesUAH)
async def create_expense_amount(message: Message, state: FSMContext):
    await state.update_data(expensesUAH=message.text)
    data_for_mailing = await state.get_data()
    response = await post_expenses("/expenses", data_for_mailing)
    if response.status == 200:
        await message.answer("Recorded!")
        await state.clear()