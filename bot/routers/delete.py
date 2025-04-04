from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from api import delete_expenses
from states.main import DeleteExpenseForm

router = Router()

@router.message(F.text == "Видалити статтю")
async def create_expense(message: Message, state: FSMContext):

    await state.clear()

    await message.answer("Enter expense id, which you want to delete")
    await state.set_state(DeleteExpenseForm.id)

@router.message(DeleteExpenseForm.id)
async def create_expense_title(message: Message, state: FSMContext):

    await state.update_data(id=message.text)
    data_for_mailing = await state.get_data()
    response = await delete_expenses("/expenses", data_for_mailing)

    if response.status == 200:

        await message.answer("The expense has been deleted")
        await state.clear()

    else:

        await message.answer("No recording with this id")